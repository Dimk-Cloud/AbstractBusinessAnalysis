"""
This module defines the generate() function which returns pseudo-random test 
data to be used as input to the `analyze` function of the `absan` module.
"""

import numpy as np 
import pandas as pd
from pandas import Series, DataFrame
from collections.abc import Sequence # for type hints

# Public API declaration
__all__ = ['Metrange', 'generate']

# Metric range type
type Metrange = tuple[float, float]

def generate(entities: Sequence,
             metrics: Sequence,
             metrics_range: Metrange | Sequence[Metrange]) -> DataFrame:

    """Return a DataFrame containing pseudo-random data numerically representing
    each entity's value for each metric.

    The returned data is in the form of a 2D-matrix (DataFrame), where each row
    represents an entity (i.e, product, service or customer in a real analysis)
    and each column is a certain metric. Thus, the intersection of an entity and
    a metric gives that entity's value for the business in therms of the metric.

    Arguments are as follows:

    entities: an iterable containing entities' names or ids;
    metrics: an iterable containing metrics` names or ids;
    metrics_range:
        if a tuple: lower and upper boundaries for the generated data;
        if an iterable: lower and upper boundaries for the generated data,
            for each metric; the length should be equal to that of metrics
    """

    entities = tuple(entities)
    metrics = tuple(metrics)

    # Generate a matrix of normally distributed random values
    # to reflect a real distribution of product values,
    # where a few products are significantly more valuable than others.
    
    rng = np.random.default_rng()
    data = np.abs(rng.normal(size = (len(entities), len(metrics))))

    # as an alternative, the uniform distribution
    #data = np.random.rand(len(entities), len(metrics))

    # using pattern matching to quickly handle metrics_range
    match metrics_range:
        case [lower, upper]:
            data = lower + data*(upper-lower)
        case [*_]:
            met_ranges = list(metrics_range)
            for colnum in range(len(metrics)):
                data[:, colnum] = met_ranges[colnum][0]\
                                  + data[:, colnum]\
                                  * (met_ranges[colnum][1]
                                     - met_ranges[colnum][0])
        case _:
            raise TypeError(
                'metric_range should be Metrange | Iterable[Metrange]')

    # construct the final DataFrame          
    data = DataFrame(data = data,
                     index = entities,
                     columns = metrics)
    
    return data

'''
# Usage examples
entities = ('computer', 'mouse', 'keyboard')
metrics = ('recency', 'frequency', 'monvalue')
metric_range = (0, 100)

data = generate(entities, metrics, ((1, 2), (5, 6), (15, 16)))
#data = generate(entities, metrics, metric_range)
'''
            
    
        



