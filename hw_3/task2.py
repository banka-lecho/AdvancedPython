import os
import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class MatrixWithMixin(NDArrayOperatorsMixin):
    def __init__(self, data):
        self._data = np.asarray(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = np.asarray(value)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        inputs = tuple(x.data if isinstance(x, MatrixWithMixin) else x for x in inputs)

        if out:
            kwargs['out'] = tuple(
                x.data if isinstance(x, MatrixWithMixin) else x
                for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if method == '__call__':
            return MatrixWithMixin(result)
        else:
            return result

    def __str__(self):
        return str(self._data)

    def save_to_file(self, filename):
        np.savetxt(filename, self._data, fmt='%g')

    # Генерация матриц с seed=0


np.random.seed(0)
matrix1 = MatrixWithMixin(np.random.randint(1, 10, (3, 3)))
matrix2 = MatrixWithMixin(np.random.randint(1, 10, (3, 3)))

path_to_artifacts = os.path.join(os.getcwd(), "artifacts/task2")
if not os.path.exists(path_to_artifacts):
    os.mkdir(path_to_artifacts)

matrix_add = matrix1 + matrix2
matrix_sub = matrix1 - matrix2
matrix_mul = matrix1 * matrix2
matrix_div = matrix1 / matrix2
matrix_matmul = matrix1 @ matrix2

matrix_add.save_to_file(os.path.join(path_to_artifacts, 'matrix+.txt'))
matrix_sub.save_to_file(os.path.join(path_to_artifacts, 'matrix-.txt'))
matrix_mul.save_to_file(os.path.join(path_to_artifacts, 'matrix*.txt'))
matrix_div.save_to_file(os.path.join(path_to_artifacts, 'matrix_div.txt'))
matrix_matmul.save_to_file(os.path.join(path_to_artifacts, 'matrix@.txt'))

print("\nРезультаты операций:")
print("\nСложение:")
print(matrix_add)

print("\nВычитание:")
print(matrix_sub)

print("\nПоэлементное умножение:")
print(matrix_mul)

print("\nПоэлементное деление:")
print(matrix_div)

print("\nМатричное умножение:")
print(matrix_matmul)
