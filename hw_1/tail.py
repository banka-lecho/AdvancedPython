import sys


def tail(file, lines=10):
    """ Выводит последние `lines` строк из файла или stdin """
    try:
        with file if file == sys.stdin else open(file, 'r') as f:
            content = f.readlines()
            for line in content[-lines:]:
                print(line, end='')
    except FileNotFoundError:
        print("Нет такого файла")
    except PermissionError:
        print("Нет прав")
    except IsADirectoryError:
        print("Переданный объект -- директория")


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else [sys.stdin]
    for i, file in enumerate(files):
        if len(files) > 1 and file != sys.stdin:
            print(f"==> {file} <==")
        tail(file, lines=17 if file == sys.stdin else 10)
        if i < len(files) - 1 and file != sys.stdin:
            print()


if __name__ == "__main__":
    main()
