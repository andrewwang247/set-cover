"""
Generate random set cover problems.

Copyright 2020. Siwei Wang.
"""
# pylint: disable=no-value-for-parameter
from random import randint, sample
from os import path
from json import dump
from typing import Dict, List, Tuple
from click import command, option, Path


def check_args(universe: int,
               num: Tuple[int, int],
               size: Tuple[int, int],
               output: str):
    """Ensure command line arguments are valid."""
    num_lower, num_upper = num
    size_lower, size_upper = size
    assert num_lower < num_upper
    assert size_lower < size_upper < universe
    _, extension = path.splitext(output)
    assert extension == '.json'


@command()
@option('--universe', '-u', type=int, default=1_000,
        help='Universe size of integers.')
@option('--num', '-n', type=(int, int), default=(100, 500),
        help='Bounds on number of subsets in cover.')
@option('--size', '-s', type=(int, int), default=(10, 30),
        help='Bounds on size of any subset.')
@option('--output', '-o', type=Path(), required=True,
        help='JSON file to write output.')
def main(universe: int, num: Tuple[int, int],
         size: Tuple[int, int], output: str):
    """Generate random test cases."""
    check_args(universe, num, size, output)
    # The number of subsets.
    num_subs = randint(*num)
    print(f'Generating {num_subs} subsets...')
    problem: Dict[str, List[int]] = {}
    for i in range(num_subs):
        key = 'S' + str(i + 1)
        # The size of this particular subset.
        sub_size = randint(*size)
        value = sample(range(universe), sub_size)
        problem[key] = value
    with open(output, 'w', encoding='UTF-8') as fout:
        dump(problem, fout, indent=2)


if __name__ == '__main__':
    main()
