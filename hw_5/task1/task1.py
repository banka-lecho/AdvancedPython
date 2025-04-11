import os
import aiohttp
import asyncio
import argparse
from urllib.parse import urljoin


async def download_image(session, url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
            else:
                print(f"Не удалось скачать {url}: HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка скачивания {url}: {str(e)}")


async def download_images_async(num_images, output_dir):
    # Создаем директорию, если она не существует
    os.makedirs(output_dir, exist_ok=True)

    # Базовый URL для picsum.photos с параметрами для уникальных изображений
    base_url = "https://picsum.photos/"

    # Создаем список уникальных URL (добавляем seed для уникальности)
    urls = [urljoin(base_url, f"seed/{i}/2000/2000") for i in range(num_images)]

    # Создаем списак путей для сохранения
    save_paths = [os.path.join(output_dir, f"image_{i}.jpg") for i in range(num_images)]

    # Создаем сессию aiohttp и скачиваем пикчи
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, save_path in zip(urls, save_paths):
            task = asyncio.create_task(download_image(session, url, save_path))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(description="Async image downloader для picsum.photos")
    parser.add_argument("-n", "--num-images", type=int, required=True, help="Количество изображений для скачивания")
    parser.add_argument("-o", "--output-dir", type=str, default="downloaded_images",
                        help="Директория для сохранения изображений")

    args = parser.parse_args()
    asyncio.run(download_images_async(args.num_images, args.output_dir))
