# Introduction and rationale.

Some types of business analysis entail calculating an entity's value from a collection of metrics. 

To give an example, there are two categorical metrics in ABC/XYZ analysis:

- The ABC metric is made up of three categories (A, B abd C) which determine the value of a product to the business in terms of a certain criteria, usually revenue or margin.
- Similarly, the XYZ metric's categories reflect a product's variation in demand.

The overall value of a product item is found by combining the two above-mentioned categories to get an ABX/XYZ score. The two metrics may be considered equal or each assigned a "weight", reflecting their importance.

Another example is RFM analysis, which has three metrics: Recency, Frequency and Monetary value. In a like manner, the overal RFM score of a customer is the result of combining the three metrics for that customer, with or without weights.

In ABC/XYZ analysis the entity is the product, in RFM - the customer.

This small project abstracts away the details of a particular analysis, and measures the overall score for each entity based on a set of conceptual metrics and values for those metrics.

# Sample data generation.

The `generate` function of the `absgen` module generates pseudo-random data that could be used to pass to the `analyze` function (see below), to test it. The pseudo-random data simulates a "value" for each entity, in the context of each metric. The function returns a 2D-matrix (DataFrame) of such values, where rows represent entities and columns represent abstract metrics. 

To reflect a real distribution of product values, where a small number of products are more valuable than the rest, the normal distribution is used to produce the pseudo-random values.

A more detailed description is given in `absgen.__doc__` 

# Analysis.
## The `analyze` function.

The function `analyze` in the `absan` module performs abstract business analysis of a list of entities based on a number of metrics, regardless of the nature of both entities and metrics. The arguments of the function are:

`data`: an E x M DataFrame, where E is the number of entities (rows), and M is the number of metrics (columns). The index of the DataFrame contains the names or IDs of the entities, while the columns contain the names or IDs for the metrics. For each metric (column), a.k.a. criterium, the respective numbers represent entities' "values". To give a specific example, entities could be customers and a metric could be Recency (the date of last purchase), in which case the values would be dates of last purchase, for each customer.

`cats`: number of categories, into which entities are grouped prior to analysis. For details, see the subsection "Category assignment".

`weights`: a sequence of weights, for each metric. The weights reflect various degrees of each metric's significance. If `None`, all metrics are treated equally. See also "Analysis result."

`binfun`: a mapping of the form { metric_name : function }, which, for each metric, specifies a function that should be used for categorizing entities in the context of that metric. For metrics not present in the mapping, the default function will be applied. If `None`, the default function will be applied for all metrics. See also "Category assignment."

The function returns a DataFrame with the result of the analysis, indexed by entities and containing the following columns: 

- {$M_i$}: M columns, where $i \in[1, M]$ and M is the number of metrics. $i^{th}$ column contains category designations for each entity, for $i^{th}$ metric.
- `score`: the overall scores, for each entity.
- `group`: a concatenation of category names across all metrics, for each entity. 

For detailed information, see "Analysis result". 

## Category assignment.
For each metric in `data`, there is a list of numerical values, with each value corresponding to a particular entity. To facilitate the category-based business analysis, the numerical values and, by implication, entities, are classified into categories. The number of categories, `cats`, is the same for all metrics and is passed as an argument to the `analyze` function. Categories themselves are assigned uppercase letters, A through Z, effectively limiting their number by `len(string.ascii_uppercase)`. 

This approach is employed in many types of business analysis, e.g. RFM or ABC/XYZ. The limit on the number of categories is not a problem, since having more categories than the limit will be impractical. The number of categories in a typical category-based business analysis ranges, on average, from 3 to 10.

The default method in which the classification, or grouping, is done is by simple value-based dividing of the range of metric values into equal bins (binning), the number of bins being the same as the number of categories. If a function is provided for that purpose, it should take a Series with metric values and return another Series, with the same index, containing category letters corresponding to those values. Both Series should be indexed by entities, and the number of categories should be the same across all metrics.

## Category values.
For the purpose of determining the overall score for each entity, each category is assigned a numerical value in a monotonically increasing fashion, starting with 1 (A = 1, B = 2, and so on). The higher the value of a category, the more important the products in that category are for the business.

## Analysis results.
For each entity, the analysis returns:

1. Category designation for each metric, given in the first M columns, M being the total number of metrics.
2. Entity group, which is a simple concatenation of category names across all metrics. In some types of analysis it is also called a cell (e.g., an RFM cell). For instance, "ACBBA" means that an entity has been assigned those five categories in an analysis with five metrics. It should be noted that even in a weighted analysis, the entity group does not take account of various levels of metric's significance.
3. Entity score, which is determined as:

$Score (e_i) = \frac{\sum_{j=1}^{M} w_j *c_i^j}{\sum_{j=1}^{M} w_j}$, where:

$e_i$ : the entity with the index $i \in[1, E]$, where E is the total number of entities;
$w_j$: a series of weights, one for each metric, such that $j \in[1, M]$, where M is the number of metrics;
$c_i^j$: numerical category value for the $i^{th}$ entity ($e_i$) and $j^{th}$ metric.

A print-out with the results of an analysis with 5 categories (A through E), 10 entities (E1 through E10) and 10 unweighted metrics (M1 through M10) may look like this:

    result
        M1 M2 M3 M4 M5 M6 M7 M8 M9 M10  score       group
    E1   E  A  B  D  C  A  A  A  A   B     21  EABDCAAAAB
    E2   A  B  D  C  E  A  A  A  C   E     26  ABDCEAAACE
    E3   C  A  A  B  B  B  C  B  A   E     22  CAABBBCBAE
    E4   E  B  A  B  E  E  A  D  E   D     34  EBABEEADED
    E5   C  B  A  E  C  C  E  D  D   A     31  CBAECCEDDA
    E6   A  E  B  A  E  B  D  A  C   B     26  AEBAEBDACB
    E7   B  B  B  A  C  C  C  E  B   E     28  BBBACCCEBE
    E8   A  A  D  E  E  A  A  D  B   D     28  AADEEAADBD
    E9   B  B  E  B  C  B  A  A  E   A     24  BBEBCBAAEA
    E10  A  B  C  B  A  E  A  B  C   A     21  ABCBAEABCA

In a weighted analysis, the entity score takes into account the various levels of metric's significance. 

The result of the analysis may be used to identify the most and least valuable products for the business, or classify customers into groups or cohorts for more efficient targeting and marketing communication.


# The `main` module.

The `main` module is given as a convenience. It shows how to specify the initial parameters, such as the number of metrics, entities, categories, category weights and a range $^{1}$ for metric random values, as well as how to provide names for entities and metrics, which are used as the index and columns, respectively.

The module calls the `generate` function of the `absgen` module and passes the results into the `analyze` function of the `absan` module, before getting the results of the analysis.

*Notes.*

*1. The range for metric values essentially represents a linear transformation to make the values more realistic. This makes more sense in the context of the uniform distribution, which can be produced by uncommenting a specific line in the `generate` function, rather than the normal distribution.*


















