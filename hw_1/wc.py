import sys


def wc(file):
    """ Считает строки, слова и байты в файле или stdin """
    if file == sys.stdin:
        content = file.read()
    else:
        with open(file, 'rb') as f:
            content = f.read()

    lines = content.count(b'\n')
    words = len(content.split())
    bytes_count = len(content)

    return lines, words, bytes_count


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        total_lines, total_words, total_bytes = 0, 0, 0

        for file in files:
            try:
                lines, words, bytes_count = wc(file)
                print(f"{lines:8}{words:8}{bytes_count:8} {file}")
                total_lines += lines
                total_words += words
                total_bytes += bytes_count
            except FileNotFoundError:
                print(f"wc: {file}: No such file or directory", file=sys.stderr)
            except IsADirectoryError:
                print(f"wc: {file}: It is not a file", file=sys.stderr)

        if len(files) > 1:
            print(f"{total_lines:8}{total_words:8}{total_bytes:8} total")
    else:
        lines, words, bytes_count = wc(sys.stdin)
        print(f"{lines:8}{words:8}{bytes_count:8}")


if __name__ == "__main__":
    main()
