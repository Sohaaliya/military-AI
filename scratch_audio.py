import sys
import numpy as np
from scipy.io import wavfile
import os

if os.path.exists('d:/command/input.wav'):
    fs, data = wavfile.read('d:/command/input.wav')
    print("Sample rate:", fs)
    print("Data type:", data.dtype)
    print("Shape:", data.shape)
    print("Max val:", np.max(data))
    print("Min val:", np.min(data))
    print("Mean abs:", np.mean(np.abs(data)))
    print("99th percentile:", np.percentile(np.abs(data), 99))
else:
    print("input.wav not found")
