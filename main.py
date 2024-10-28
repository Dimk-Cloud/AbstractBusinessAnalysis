import numpy as np 
import pandas as pd
from pandas import Series, DataFrame
from string import ascii_uppercase

from absgen import generate
from absan import analyze

# Setting comfortable display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)

E = NUM_OF_ENTITIES = 10
M = NUM_OF_METRICS = 10
C = NUM_OF_CATS = 5

# define a list of entities,
# as sequential strings E1, E2, ..., E<NUM_OF_ENTITIES>
entities = ["E" + str(n) for n in range(1, NUM_OF_ENTITIES + 1)]

# define a list of metrics,
# as sequential strings M1, M2, ..., M<NUM_OF_METRICS>
metrics = ["M" + str(n) for n in range(1, NUM_OF_METRICS + 1)]

# define a metric range, one for all metrics, for simplicity
metric_range = (0, 100)

#def get_random_weights(n: int):
weights = [15, 4, 7, 13, 11, 10, 12, 6, 8, 14]

def testcatfun(s: Series, n: int) -> Series:
    return Series(data = 'C', index = s.index)

data = generate(entities, metrics, metric_range)
result = analyze(data = data, cats = 5, weights = weights)

