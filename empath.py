#!/usr/bin/env python3

import sys
N=int(sys.argv[1])

print("No Spy and No Recluse or Both:")
print(f"Zero Reds: {round(100*(N-4)*(N-5)/(N-1)/(N-2))}%")
print(f"One  Red:  {round(100*6*(N-4)/(N-1)/(N-2))}%")
print(f"Two  Reds: {round(100*6/(N-1)/(N-2))}%")
