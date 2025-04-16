import os

import numpy as np


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0

    def __add__(self, other):
        """Сложение"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны быть одного размера для сложения")

        result = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        """Покомпонентное умножение"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны быть одного размера для покомпонентного умножения")

        result = [
            [self.matrix[i][j] * other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __matmul__(self, other):
        """Матричное умножение"""
        if self.cols != other.rows:
            raise ValueError(
                "Число столбцов первой матрицы должно быть равно числу строк второй для матричного умножения"
            )

        result = [
            [
                sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.matrix])


np.random.seed(0)
matrix1 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
matrix2 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

path_to_artifacts = os.path.join(os.getcwd(), "artifacts/task1")
if not os.path.exists(path_to_artifacts):
    os.mkdir(path_to_artifacts)

for op, filename in [
    (matrix1 + matrix2, "artifacts/task1/matrix+.txt"),
    (matrix1 @ matrix2, "artifacts/task1/matrix@.txt"),
    (matrix1 * matrix2, "artifacts/task1/matrix*.txt"),
]:
    with open(filename, "w") as f:
        f.write(str(op))
