import sys


def number_lines(input_file=None):
    """ Выводит строки с нумерацией """
    if input_file:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    for i, line in enumerate(lines, start=1):
        print(f"{i}\t{line}", end='')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        number_lines(sys.argv[1])
    else:
        number_lines()
