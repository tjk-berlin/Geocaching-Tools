north = "1322.246"

import math


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m

for i in toBinary(north):
    print(f"{i:08}")