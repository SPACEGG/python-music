import numpy as np
import scipy.stats as ss
from matplotlib import pyplot as plt

mean = 0
std = 1
num_samples = 100
samples = np.random.normal(mean, std, size=num_samples)
normal = (samples - samples.min()) / (samples.max() - samples.min())
result = np.heaviside(normal, 0)

plt.plot(result)
plt.show()