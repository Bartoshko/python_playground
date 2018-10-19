import numpy as np

# input
x = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1],
    [1, 0, 0],
    [0, 1, 0]
])

# output
y = np.array([
    [0, 0, 1, 1, 1, 0, 0, 0]
])

# generate weights
np.random.seed(1)
w = 2 * np.random.random((3, 1)) - 1
print(w)
# set learning rate
learning_rate = 1e-6

counter = 200
while counter > 0:
    counter -= 1
    h = x.dot(w)
    y_pred = np.minimum(h, 0)

    loss = np.square(y_pred - y).sum()
    print(f'learning step: {counter}, loss: {loss}')

    # backpropagation
    grad_y_pred = 2.0 * (y_pred - y)
    grad_h = y_pred.T.dot(grad_y_pred)
    grad_h_relu = np.array([np.amax(grad_h.T.dot(w.T), 0)])
    w = learning_rate * grad_h_relu.T
    print(f'weights shape {w.shape}')
