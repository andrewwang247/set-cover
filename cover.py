"""
Greedy heuristic for the NP-Hard set cover problem.

The greedy algorithm stipulates that at each step,
we choose the subset that contains the greatest number
of yet-to-be-covered items.

Requires: input file is a JSON dictionary of lists.
If output file is provided, it must be JSON too.

Copyright 2020. Siwei Wang.
"""
# pylint: disable=no-value-for-parameter
from json import load, dump
from os import path
from functools import reduce
from timeit import default_timer as timer
from pprint import pprint
import numpy as np
import click


def parse_args(filepath, output):
    """Parse the json file with extension check."""
    # Check that the file is a json.
    in_file_extension = path.splitext(filepath)[1]
    if in_file_extension != '.json':
        raise Exception('Input file must be JSON.')
    if output is not None:
        out_file_extension = path.splitext(output)[1]
        if out_file_extension != '.json':
            raise Exception('Output file must be JSON.')
    with open(filepath, 'r') as fin:
        return load(fin)


def check_input(subsets):
    """Ensure inputs are valid and convert lists to sets."""
    # Do some sanity checks on input.
    if len(subsets) == 0:
        raise Exception('Input is empty.')
    if not isinstance(subsets, dict):
        raise Exception('Parent JSON type must be dict.')
    alt_subset = dict()
    # Ensure proper type and no duplicates.
    for key, value in subsets.items():
        if not isinstance(value, list):
            raise Exception('Secondary JSON type must be list.')
        value_set = np.unique(value)
        if len(value) != len(value_set):
            raise Exception('There\'s a duplicate in {}.'.format(key))
        alt_subset[key] = value_set
    # Return as dictionary of sets.
    return alt_subset


def largest_valued_key(dic):
    """Find the key with the largest value."""
    biggest_size = -1
    biggest_key = None
    for key, value in dic.items():
        length = len(value)
        if length > biggest_size:
            biggest_size = length
            biggest_key = key
    return biggest_key


def biggest_intersection(universe, subsets, large):
    """Get the subset with the greatest intersection with universe."""
    opt_size = -1
    # Stores key value pairs with the largest intersection.
    opt = dict()
    opt_key = None
    assert len(subsets) > 0
    for key, value in subsets.items():
        # Compare the intersection size.
        intersection = np.intersect1d(universe, value, assume_unique=True)
        intersect_size = len(intersection)
        if intersect_size > opt_size:
            opt_size = intersect_size
            opt_key = key
            # Reset opt dictionary.
            opt.clear()
            opt[key] = value
        elif intersect_size == opt_size:
            opt[key] = value
    return largest_valued_key(opt) if large else opt_key


def sorted_set(subset):
    """Convert a set to a sorted list."""
    as_list = list(subset)
    as_list.sort()
    return as_list


def write_solution(solution, output):
    """Print solution to output JSON file."""
    serialized = {key: value.tolist() for key, value in solution.items()}
    with open(output, 'w') as fout:
        dump(serialized, fout, indent=4)
    print('Solution written to {}.'.format(output))


@click.command()
@click.option('--filepath', '-f', required=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='The path to the JSON file that will be used as input.')
@click.option('--large', '-l', is_flag=True, default=False,
              help='Prefer larger subsets with more overlap.')
@click.option('--output', '-o', required=False, type=click.Path(),
              help='JSON file in which to write solution. No arg: console.')
def main(filepath, large, output):
    """Compute the approximate set cover."""
    # Map every key to a set.
    raw_json = parse_args(filepath, output)
    subset_dict = check_input(raw_json)
    print('Original cover has {} subsets.'.format(len(subset_dict)))
    start = timer()
    # Compute their total union.
    universe = reduce(np.union1d, subset_dict.values())
    solution = dict()
    # We wish to use the subsets to carve away at the universe.
    while len(universe) != 0:
        # Find the subset with the biggest intersection with universe.
        opt_key = biggest_intersection(universe, subset_dict, large)
        # Remove and return the largest entry.
        opt_val = subset_dict.pop(opt_key)
        # Take the set difference against universe.
        universe = np.setdiff1d(universe, opt_val, assume_unique=True)
        # Add the entry to solution.
        solution[opt_key] = opt_val
    end = timer()
    print('Greedy solution requires {} subsets.'.format(len(solution)))
    print('Execution took {} seconds.'.format(round(end - start, 4)))
    # If no argument was provided, pretty print to console.
    if output is None:
        pprint(solution)
    else:
        write_solution(solution, output)


if __name__ == '__main__':
    main()
