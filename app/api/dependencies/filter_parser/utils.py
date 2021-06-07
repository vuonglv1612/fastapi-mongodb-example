import itertools
from typing import Dict, List, Tuple


def parse_sort_query(str_sort) -> Dict[str, int]:
    client_sort = dict()
    for sort_arg in [s.strip() for s in str_sort.split(",")]:
        if sort_arg[0] == "-":
            client_sort[sort_arg[1:]] = -1
        elif sort_arg[0] == "+":
            client_sort[sort_arg[1:]] = 1
        else:
            client_sort[sort_arg[:]] = 1
    return client_sort


def combine_queries(query_a, query_b):
    """Takes two db queries and applies db-specific syntax to produce
    the intersection.

    This is used because we can't just dump one set of query operators
    into another.

    Consider for example if the dataset contains a custom datasource
    pattern like --
        'filter': {'username': {'$exists': True}}

    If we simultaneously try to filter on the field `username`,
    then doing
        query_a.update(query_b)
    would lose information.

    This implementation of the function just combines everything in the
    two dicts using the `$and` operator.

    Note that this is exactly same as performing dict.update() except
    when multiple operators are operating on the /same field/.

    Example:
        combine_queries({'username': {'$exists': True}},
                        {'username': 'mike'})
    {'$and': [{'username': {'$exists': True}}, {'username': 'mike'}]}

    .. versionadded: 0.1.0
        Support for intelligent combination of db queries
    """
    # Chain the operations with the $and operator
    return {
        "$and": [{
            k: v
        } for k, v in itertools.chain(query_a.items(), query_b.items())]
    }