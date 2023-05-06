#!/usr/bin/env python3

import re
import sys
import random
N=int(sys.argv[1])

p={0: 0, 1: 0, 2: 0}
pExcludePair={0: 0, 1: 0, 2: 0}
pExclude2Pairs={0: 0, 1: 0, 2: 0}
bads = 3
first = random.randint(0, N-1)
second = random.randint(0, N-1)
while second == first:
    second = random.randint(0, N-1)
third = random.randint(0, N-1)
fourth = random.randint(0, N-1)
while second == first:
    second = random.randint(0, N-1)
print(f"First: {first}")
print(f"Second: {second}")
for i in range(1, 2**N):
    s = bin(i)
    j = s.count('1')
    if j!=bads:
        continue
    pairs = len(re.findall('(?=11)', s))
    p[pairs]+=1
    if (i & (1 << first) == 0 or i & (1 << second) == 0):
        pExcludePair[pairs] += 1
        if (i & (1 << third) == 0 or i & (1 << fourth) == 0):
            pExclude2Pairs[pairs] += 1

print(p)
print(p[0]+p[1]+p[2])
print(pExcludePair)
print(pExcludePair[0]+pExcludePair[1]+pExcludePair[2])
print(pExclude2Pairs)
print(pExclude2Pairs[0]+pExclude2Pairs[1]+pExclude2Pairs[2])
