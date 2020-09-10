from itertools import islice
import os

all_id = (i for i in range(1000000, 1441696))
with open("names", 'r') as f:
    b = f.read().splitlines()
    print(b)

for i in range(1000000, 1441696):
    if str(i) not in b:
        with open("names_new", 'a') as f:
            f.write(str(i) + '\n')