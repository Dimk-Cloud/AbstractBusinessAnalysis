"""This module defines the analyze() function that performs abstract business
analysis of a list of entities based on a number of metrics, regardless
of the nature of both entities and metrics.
"""

import numpy as np 
import pandas as pd
from pandas import Series, DataFrame
from collections.abc import Sequence, Mapping, Callable # for type hints
from string import ascii_uppercase

from absgen import generate

# Public API declaration
__all__ = ['analyze']

# Setting comfortable display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def analyze(data: DataFrame,
            cats: int,
            weights: Sequence[int|float] | None = None,
            binfun: Mapping[str, Callable] | None = None) -> DataFrame:
    
    """Perform abstract business analysis of entities based on a number of
    conceptual metrics, returning the entity group and the overall value
    score, for each entity.

    Arguments:

    data: a DataFrame, where data.index lists the entities, and data.columns
    lists the conceptual metrics for each entity. The DataFrame contains values
    for each entity in the context of each metric;

    cats: number of categories;

    weights: a sequence of weights for the metrics;

    binfun: a mapping of the form { metric_name : function },
    which, for each metric, specifies a function that should be used
    for categorizing entities in the context of that metric.
    """

    # Checks on the parameters
    #
    if not isinstance(data, DataFrame):
        raise TypeError('data should be a pandas.DataFrame')

    if not isinstance(cats, int):
        raise TypeError('cats should be an int')

    match weights:
        case [*_]:
            if not all(isinstance(weight, (int, float)) for weight in weights):
                raise ValueError(
                    'weights should be a Sequence[int|float] or None'
                    )
        case None:
            pass

        case _:
            raise ValueError('weights should be a Sequence[int|float] or None')

    match binfun:
        case {**_a}:
            if not all(all((isinstance(k, str), isinstance(v, Callable)))
                       for k, v in binfun.items()):
                raise ValueError(
                    'binfun should be Mapping[str, Callable] or None'
                    )
        case None:
            pass

        case _:
            raise ValueError('binfun should be Mapping[str, Callable] or None')

    # define the uppercase labels and corresponding values
    labels = list(ascii_uppercase[:cats])
    valuemap = { label : value
                 for value, label in enumerate(labels, start = 1) }

    # the default categorization function
    def categorize(s: Series, n: int) -> Series:
        return pd.cut(s, n, labels = labels)

    # categorize data
    if binfun:
        # apply functions to the metrics specified in binfun
        # apply the default function to the rest
        result  = data.transform(
            dict.fromkeys(data.columns, categorize) | binfun,
            n = cats)
        
    else: # apply the default function to all metrics
        result = data.transform(categorize, n = cats)

    # concatenate category letters to get entity groups
    groups = result.apply(lambda s : s.str.cat(), axis = 1)

    # determine entity scores
    if weights:
        #breakpoint()
        result['score'] = (
            result.apply(lambda e :
                         (e.map(valuemap).astype(int) * weights).sum()
                         /sum(weights),
                         axis = 1)
            )
    else:
        result['score'] = result.apply(lambda e :
                                       e.map(valuemap).astype(int).sum(),
                                       axis = 1)

    # add the group column
    result['group'] = groups
    
    return result

    
    























    

        

