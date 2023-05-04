#!/usr/bin/env python3

import sys
N=int(sys.argv[1])
K=4

pairs = [0, 0, 0, 0]

# a < b < c
def threePairs(a, b, c, d):
    return ((a+1 == b      and b+1 == c       and c+1 == d) or
           ( b+1 == c      and c+1 == d       and (d+1) % N == a) or 
           ( c+1 == d      and (d+1) % N == a and a+1 == b) or
           ((d+1) % N == a and a+1 == b       and b+1 == c))

# a < b < c
def twoPairs(a, b, c, d):
    return ((a+1 == b      and b+1 == c       and c+1 != d) or
           (b+1 == c       and c+1 == d       and (d+1) % N != a) or 
           (c+1 == d       and (d+1) % N == a and a+1 != b) or
           ((d+1) % N == a and a+1 == b       and b+1 != c))

# a < b < c
def onePair(a, b, c, d):
    return ((a+1 == b      and b+1 != c       and c+1 != d) or
           (b+1 == c       and c+1 != d       and (d+1) % N != a) or 
           (c+1 == d       and (d+1) % N != a and a+1 != b) or
           ((d+1) % N == a and a+1 != b       and b+1 != c))

condProbCases = [0, 0, 0]
def anchoretHasAFriend(a, b, c):
    return (a+1 == b or b+1 == c)

common = 0
# i < j < k
for i in range(0, N-K+1):
    for j in range(i+1, N-K+2):
        for k in range(j+1, N-K+3):
            for l in range(k+1, N-K+4):
                common += 1
                if threePairs(i, j, k, l):
                    pairs[3] += 1
                    if anchoretHasAFriend(i, j, k):
                        condProbCases[2] += 1
                elif twoPairs(i, j, k, l):
                    pairs[2] += 1
                    if anchoretHasAFriend(i, j, k):
                        condProbCases[1] += 1
                elif onePair(i, j, k, l):
                    pairs[1] += 1
                    if anchoretHasAFriend(i, j, k):
                        condProbCases[0] += 1
                else:
                    pairs[0] += 1

print(f"Zero pairs: {pairs[0]} = {round(pairs[0]*100/common)}%")
print(f"One pair: {pairs[1]} = {round(pairs[1]*100/common)}% | {condProbCases[0]} anchoret = {round(condProbCases[0]*100/pairs[1])}%")
print(f"Two pairs: {pairs[2]} = {round(pairs[2]*100/common)}% | {condProbCases[1]} anchoret = {round(condProbCases[1]*100/pairs[2])}%")
print(f"Three pairs: {pairs[3]} = {round(pairs[3]*100/common)}% | {condProbCases[2]} anchoret = {round(condProbCases[2]*100/pairs[3])}%")
print(f"Common: {common}")
