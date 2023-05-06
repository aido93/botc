#!/usr/bin/env python3

import numpy as np

# Define the matrices
A = np.array([[0.39, 0.48], [0.61, 0.52]])

# Multiply the matrices
C = np.dot(A, A)

# Print the result
print(C)
