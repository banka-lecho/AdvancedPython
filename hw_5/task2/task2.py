import os
import json
import asyncio
import aiohttp
import logging
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)


class AsyncRealtyScraper:
    def __init__(self, output_file_path: str):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.session = None
        self.data_file = output_file_path
        self.seen_ads = set()
        self.load_existing_data()

    def load_existing_data(self):
        """Загружает ранее собранные данные и идентификаторы объявлений"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    for item in data:
                        self.seen_ads.add(item['id'])
                except json.JSONDecodeError:
                    logging.warning("Что-то не так с файлом данных, начнем с пустого набора")
                    data = []
        else:
            data = []
        return data

    async def start(self):
        """Запускает скрапер"""
        async with aiohttp.ClientSession(headers=self.headers) as self.session:
            while True:
                try:
                    logging.info("Начало нового цикла сбора данных")

                    # Собираем данные со всех источников
                    cian_data = await self.scrape_cian()
                    yandex_data = await self.scrape_yandex_realty()
                    avito_data = await self.scrape_avito()

                    # Объединяем все данные
                    all_data = self.load_existing_data()
                    new_data = cian_data + yandex_data + avito_data

                    # Фильтруем только новые объявления
                    new_ads = [ad for ad in new_data if ad['id'] not in self.seen_ads]

                    if new_ads:
                        logging.info(f"Найдено {len(new_ads)} новых объявлений")
                        all_data.extend(new_ads)

                        # Сохраняем новые данные
                        with open(self.data_file, 'w', encoding='utf-8') as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)

                        # Обновляем список просмотренных объявлений
                        for ad in new_ads:
                            self.seen_ads.add(ad['id'])
                    else:
                        logging.info("Новых объявлений не найдено")

                    # Пауза между циклами (например, 10 сек)
                    logging.info("Ожидание следующего цикла...")
                    await asyncio.sleep(10)

                except Exception as e:
                    logging.error(f"Ошибка в основном цикле: {str(e)}")
                    await asyncio.sleep(60)

    async def scrape_cian(self) -> List[Dict]:
        """Скрапинг объявлений с Cian"""
        base_url = "https://cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room9=1&type=4"
        try:
            async with self.session.get(base_url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            ads = []

            for item in soup.select('article[data-name="CardComponent"]'):
                try:
                    ad_id = item.get('data-id') or item.get('id', '')
                    if not ad_id:
                        continue

                    title = item.select_one('span[data-mark="OfferTitle"]').get_text(strip=True)
                    price = item.select_one('span[data-mark="MainPrice"]').get_text(strip=True)
                    address = item.select_one('div[data-name="GeoLabel"]').get_text(strip=True)
                    url = item.select_one('a[data-name="LinkArea"]')['href']

                    # Получаем полный URL
                    if not url.startswith('http'):
                        url = f"https://cian.ru{url}"

                    # Извлекаем дополнительные параметры
                    params = {}
                    for param in item.select('div[data-name="Description"] > div'):
                        try:
                            key = param.select_one('div:nth-child(1)').get_text(strip=True)
                            value = param.select_one('div:nth-child(2)').get_text(strip=True)
                            params[key] = value
                        except:
                            continue

                    ads.append({
                        'id': f"cian_{ad_id}",
                        'source': 'cian',
                        'title': title,
                        'price': price,
                        'address': address,
                        'url': url,
                        'params': params,
                        'timestamp': datetime.now().isoformat()
                    })

                except Exception as e:
                    logging.error(f"Ошибка при парсинге объявления Cian: {str(e)}")
                    continue

            logging.info(f"С Cian получено {len(ads)} объявлений")
            return ads

        except Exception as e:
            logging.error(f"Ошибка при сканировании Cian: {str(e)}")
            return []

    async def scrape_yandex_realty(self) -> List[Dict]:
        """Скрапинг объявлений с Яндекс.Недвижимости"""
        base_url = "https://realty.yandex.ru/moskva_i_moskovskaya_oblast/snyat/kvartira/"
        try:
            async with self.session.get(base_url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            ads = []

            for item in soup.select('div[data-test="offer-card"]'):
                try:
                    ad_id = item.get('data-test-offer-id') or ''
                    if not ad_id:
                        continue

                    title = item.select_one('span[data-test="offer-title"]').get_text(strip=True)
                    price = item.select_one('div[data-test="offer-price"]').get_text(strip=True)
                    address = item.select_one('div[data-test="address"]').get_text(strip=True)
                    url = item.select_one('a[data-test="offer-link"]')['href']

                    # Получаем полный URL
                    if not url.startswith('http'):
                        url = f"https://realty.yandex.ru{url}"

                    # Извлекаем доп параметры
                    params = {}
                    for param in item.select('div[data-test="offer-spec"] > div'):
                        try:
                            parts = param.get_text(strip=True).split(':')
                            if len(parts) == 2:
                                params[parts[0].strip()] = parts[1].strip()
                        except:
                            continue

                    ads.append({
                        'id': f"yandex_{ad_id}",
                        'source': 'yandex',
                        'title': title,
                        'price': price,
                        'address': address,
                        'url': url,
                        'params': params,
                        'timestamp': datetime.now().isoformat()
                    })

                except Exception as e:
                    logging.error(f"Ошибка при парсинге объявления Яндекс.Недвижимости: {str(e)}")
                    continue

            logging.info(f"С Яндекс.Недвижимости получено {len(ads)} объявлений")
            return ads

        except Exception as e:
            logging.error(f"Ошибка при сканировании Яндекс.Недвижимости: {str(e)}")
            return []

    async def scrape_avito(self) -> List[Dict]:
        """Скрапинг объявлений с Авито"""
        base_url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&f=ASgBAQICAkSSA8gQ8AeQUgJYwA0UxNkHFLmWAdQBFbGWAUj2rAFQ9qwBVuasAVTmrAFU5qwB"
        try:
            async with self.session.get(base_url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            ads = []

            for item in soup.select('div[data-marker="item"]'):
                try:
                    ad_id = item.get('data-item-id') or ''
                    if not ad_id:
                        continue

                    title = item.select_one('h3[itemprop="name"]').get_text(strip=True)
                    price = item.select_one('meta[itemprop="price"]')['content']
                    address = item.select_one('div[data-marker="item-address"]').get_text(strip=True)
                    url = item.select_one('a[itemprop="url"]')['href']

                    # Получаем полный URL
                    if not url.startswith('http'):
                        url = f"https://www.avito.ru{url}"

                    # Извлекаем доп параметры
                    params = {}
                    for param in item.select('div[data-marker="item-specific-params"] > span'):
                        try:
                            params[param.get_text(strip=True)] = True
                        except:
                            continue

                    ads.append({
                        'id': f"avito_{ad_id}",
                        'source': 'avito',
                        'title': title,
                        'price': price,
                        'address': address,
                        'url': url,
                        'params': params,
                        'timestamp': datetime.now().isoformat()
                    })

                except Exception as e:
                    logging.error(f"Ошибка при парсинге объявления Авито: {str(e)}")
                    continue

            logging.info(f"С Авито получено {len(ads)} объявлений")
            return ads

        except Exception as e:
            logging.error(f"Ошибка при сканировании Авито: {str(e)}")
            return []


if __name__ == "__main__":
    output_file_path = 'realty_data.json'

    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Async scraper для avito/cian/yandex")
    parser.add_argument("-o", "--output-file-path", type=str, default="'realty_data.json",
                        help="Путь к итоговому файлу")

    args = parser.parse_args()
    scraper = AsyncRealtyScraper(args.output_file_path)
    asyncio.run(scraper.start())
