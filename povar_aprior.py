#!/usr/bin/env python3

import sys
import math
N=int(sys.argv[1])
K=3

pairs = [0, 0, 0]

# a < b < c
def twoPairs(a, b, c):
    return (a+1 == b and b+1 == c) or (b+1 == c and (c+1) % N == a) or ((c+1) % N == a and a+1 == b)

# a < b < c
def onePair(a, b, c):
    return (a+1 == b and b+1 != c) or (b+1 == c and (c+1) % N != a) or ((c+1) % N == a and a+1 != b)

common = 0
# i < j < k
for i in range(0, N-2):
    for j in range(i+1, N-1):
        for k in range(j+1, N):
            common += 1
            if twoPairs(i, j, k):
                pairs[2] += 1
            elif onePair(i, j, k):
                pairs[1] += 1
            else:
                pairs[0] += 1

print(f"Zero pairs: {pairs[0]} = {round(pairs[0]*100/common)}%")
print(f"One pair: {pairs[1]} = {round(pairs[1]*100/common)}%")
print(f"Two pairs: {pairs[2]} = {round(pairs[2]*100/common)}%")
print(f"Common: {common}")
