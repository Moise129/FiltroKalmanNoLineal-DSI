#self.Xk = np.array([[1],[1],[1],[1]])  np.array([[x],[y],[vx],[vy]])
import numpy as np

a = np.array([
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8,9]
])
b = np.array([
    [2],
    [1],
    [3],
    [9]
])

resultado1 = np.matmul(a-b,np.transpose(a-b))
resultado2 = np.zeros((4,4),)


print(resultado1)

for i in range(0,9):
    resultado2 = resultado2 + (a[:,i] - b , np.transpose(a[:,i] - b)) /

print(resultado2)