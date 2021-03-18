import numpy as np
from matplotlib import pyplot as plt

# Setting
minimum = -1
maximum = 1
bit = 2

# Make noises
samples = np.random.uniform(minimum, maximum, 100)
steps = bit ** 2

# Quantization
distance = (maximum - minimum) / (steps - 1)
stairs = np.arange(minimum, maximum + distance, distance) 
quantized = np.array([stairs[np.abs(stairs - i).argmin()] for i in samples])

# Results
plt.title('random')
plt.plot(samples)
plt.plot(quantized)
plt.legend(['random', 'quantized'])
plt.show()
