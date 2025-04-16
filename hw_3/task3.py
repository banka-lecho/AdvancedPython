import os
import numpy as np
from task1 import Matrix
from functools import cache


@cache
def cached_matrix_multiply(a, b):
    print('Вычисление произведения матриц...')
    return a @ b


def save_matrix_to_file(matrix, filepath):
    """Сохраняет матрицу в файл"""
    with open(filepath, "w") as f:
        f.write(str(matrix))


class MatrixHashable(Matrix):
    def __eq__(self, other):
        """Функция равенства"""
        return np.array_equal(self.matrix, other.matrix)

    def __hash__(self):
        """Хэш-функция"""
        hash_value = 0
        for i, row in enumerate(self.matrix):
            row_hash = 0
            for j, value in enumerate(row):
                # Учитываем и строку, и столбец для более уникального хеша
                row_hash += value * (2 ** (i + j))
            hash_value += row_hash
        # Ограничиваем размер хеша
        hash_value = int(hash_value % 1000)
        return hash_value


def find_matrix_collision(artifacts_dir):
    np.random.seed(0)

    # Инициализация матриц B и D, здесь они одинаковые поскольку постольку
    B = D = MatrixHashable(np.random.randint(0, 10, (10, 10)))

    attempt_count = 0
    while True:
        attempt_count += 1
        A = MatrixHashable(np.random.randint(0, 10, (10, 10)))
        C = MatrixHashable(np.random.randint(0, 10, (10, 10)))

        # Проверка условий коллизии
        if (hash(A) == hash(C)) and (A != C) and (B == D):
            AB = cached_matrix_multiply(A, B)
            CD = cached_matrix_multiply(C, D)

            if AB != CD:
                print(f'Коллизия найдена после {attempt_count} попыток')
                save_matrix_to_file(A, f'{artifacts_dir}A.txt')
                save_matrix_to_file(B, f'{artifacts_dir}B.txt')
                save_matrix_to_file(C, f'{artifacts_dir}C.txt')
                save_matrix_to_file(AB, f'{artifacts_dir}AB.txt')
                save_matrix_to_file(CD, f'{artifacts_dir}CD.txt')

                with open(f'{artifacts_dir}hash.txt', 'w') as f:
                    f.write(str(hash(A)))
                break


path_to_artifacts = os.path.join(os.getcwd(), "artifacts/task3/")
if not os.path.exists(path_to_artifacts):
    os.mkdir(path_to_artifacts)

find_matrix_collision(path_to_artifacts)
