import numpy as np

array = np.array([[1, 0, -1], [3, 4, 1]])
salida = np.sum(array, axis=1).reshape((2,))
print(salida)