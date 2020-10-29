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
from timeit import default_timer as timer
from pprint import pprint
from typing import Dict, Optional
from click import command, option, Path


def parse_args(filepath: str, output: Optional[str]) -> Dict[str, list]:
    """Parse the json file with extension check."""
    # Check that the file is a json.
    _, in_file_extension = path.splitext(filepath)
    if in_file_extension != '.json':
        raise Exception('Input file must be JSON.')
    if output is not None:
        assert isinstance(output, str)
        _, out_file_extension = path.splitext(output)
        if out_file_extension != '.json':
            raise Exception('Output file must be JSON.')
    with open(filepath) as fin:
        content: Dict[str, list] = load(fin)
    return content


def check_input(subsets: Dict[str, list]) -> Dict[str, set]:
    """Ensure inputs are valid and convert lists to sets."""
    # Do some sanity checks on input.
    if len(subsets) == 0:
        raise Exception('Input is empty.')
    if not isinstance(subsets, dict):
        raise Exception('Parent JSON type must be dict.')
    alt_subset: Dict[str, set] = dict()
    # Ensure proper type and no duplicates.
    for key, value in subsets.items():
        if not isinstance(value, list):
            raise Exception('Secondary JSON type must be list.')
        value_set = set(value)
        if len(value) != len(value_set):
            raise Exception('There\'s a duplicate in {}.'.format(key))
        alt_subset[key] = value_set
    # Return as dictionary of sets.
    return alt_subset


def union(subsets: Dict[str, set]) -> set:
    """Take the union of a list of sets given a dictionary."""
    set_list = list(subsets.values())
    first: set = set_list[0]
    return first.union(*set_list[1:])


def largest_valued_key(dic: Dict[str, set]) -> str:
    """Find the key with the largest value."""
    biggest_size = -1
    biggest_key = None
    for key, value in dic.items():
        length = len(value)
        if length > biggest_size:
            biggest_size = length
            biggest_key = key
    assert isinstance(biggest_key, str)
    return biggest_key


def biggest_intersection(
        universe: set, subsets: Dict[str, set], large: bool) -> str:
    """Get the subset with the greatest intersection with universe."""
    opt_size = -1
    # Stores key value pairs with the largest intersection.
    opt: Dict[str, set] = dict()
    opt_key = str()
    for key, value in subsets.items():
        # Compare the intersection size.
        intersect_size = len(universe.intersection(value))
        if intersect_size > opt_size:
            opt_size = intersect_size
            opt_key = key
            # Reset opt dictionary.
            opt.clear()
            opt[key] = value
        elif intersect_size == opt_size:
            opt[key] = value
    return largest_valued_key(opt) if large else opt_key


def write_solution(solution: Dict[str, list], output: str):
    """Print solution to output JSON file."""
    # Sort solution by key.
    sorted_solution = dict(sorted(solution.items()))
    with open(output, 'w') as fout:
        dump(sorted_solution, fout, indent=2)
    print(f'Solution written to {output}.')


@command()
@option('--filepath', '-f', required=True,
        type=Path(exists=True, file_okay=True, dir_okay=False),
        help='The path to the JSON file that will be used as input.')
@option('--large', '-l', is_flag=True, default=False,
        help='Prefer larger subsets (more overlap). Often more optimal.')
@option('--output', '-o', required=False, type=Path(),
        help='JSON file in which to write solution. No arg: console.')
def main(filepath: str, large: bool, output: Optional[str]):
    """Compute the approximate set cover."""
    # Map every key to a set.
    raw_json = parse_args(filepath, output)
    subset_dict = check_input(raw_json)
    print(f'Original cover has {len(subset_dict)} subsets.')
    start = timer()
    # Compute their total union.
    universe = union(subset_dict)
    solution: Dict[str, list] = dict()
    # We wish to use the subsets to carve away at the universe.
    while len(universe) != 0:
        # Find the subset with the biggest intersection with universe.
        opt_key = biggest_intersection(universe, subset_dict, large)
        # Remove and return the largest entry.
        opt_val = subset_dict.pop(opt_key)
        # Take the set difference against universe.
        universe = universe.difference(opt_val)
        # Add the entry to solution as a sorted list.
        solution[opt_key] = sorted(opt_val)
    end = timer()
    # Report stats and execution time.
    print(f'Greedy solution requires {len(solution)} subsets.')
    print(f'Execution took {round(end - start, 4)} seconds.')
    # If no argument was provided, pretty print to console.
    if output is None:
        pprint(solution)
    else:
        assert isinstance(output, str)
        write_solution(solution, output)


if __name__ == '__main__':
    main()
