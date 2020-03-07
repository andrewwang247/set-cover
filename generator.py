"""
Generate random set cover problems.

Copyright 2020. Siwei Wang.
"""
# pylint: disable=no-value-for-parameter
from random import randint, sample
from os import path
from json import dump
import click


def check_args(universe, num, size, output):
    """Ensure command line arguments are valid."""
    num_lower, num_upper = num
    size_lower, size_upper = size
    assert num_lower < num_upper
    assert size_lower < size_upper < universe
    _, extension = path.splitext(output)
    assert extension == '.json'


@click.command()
@click.option('--universe', '-u', type=int, default=1_000,
              help='Universe size of integers.')
@click.option('--num', '-n', type=(int, int), default=(100, 500),
              help='Bounds on number of subsets in cover.')
@click.option('--size', '-s', type=(int, int), default=(10, 30),
              help='Bounds on size of any subset.')
@click.option('--output', '-o', type=click.Path(), required=True,
              help='JSON file to write output.')
def main(universe, num, size, output):
    """Generate random test cases."""
    check_args(universe, num, size, output)
    # The number of subsets.
    num_subs = randint(*num)
    print('Generating {} subsets...'.format(num_subs))
    problem = dict()
    for i in range(num_subs):
        key = 'S' + str(i + 1)
        # The size of this particular subset.
        sub_size = randint(*size)
        value = sample(range(universe), sub_size)
        problem[key] = value
    with open(output, 'w') as fout:
        dump(problem, fout, indent=4)


if __name__ == '__main__':
    main()
