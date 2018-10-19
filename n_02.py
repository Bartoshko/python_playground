import numpy as np
import matplotlib.pyplot as plt


A = np.random.randint(10, size=(1, 4))
print(A)
B = np.random.randint(10, size=(4, 1))
print(B)
C = A + B
print(C)
D = np.random.randint(100, size=(100, 4))
print(D)

plt.plot(D[:99, :1])
plt.show()
