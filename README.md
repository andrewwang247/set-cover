# Set Cover

Greedy heuristic for the NP-Hard set cover problem. See <https://en.wikipedia.org/wiki/Set_cover_problem> for more information. The heuristic achieves an approximation ratio of ln(*n*) - ln(ln(*n*)) relative to the optimal set cover. At each step, we choose the subset that contains the greatest number of yet-to-be-covered items.

## Usage

The program `cover.py` takes as input a JSON file that names and enumerates each subset. Its output is another dictionary/JSON that gives the approximately smallest subcover of the input. Using the `-l` flag will prefer larger subsets in the event of a tie. The program also notes the amount of time (in seconds) it took to execute the heuristic.

`python3 cover.py` [options]:

  -f, --filepath PATH : The path to the JSON file that will be used as input. [required]

  -l, --large : Prefer larger subsets (more overlap). Often more optimal.

  -o, --output PATH : JSON file in which to write solution. No arg: console.

  --help : Show this message and exit.

## Testing

Several unit tests can be found in the *Test* directory. The test `eecs.json` shows a real-world situation where one may need to choose a subset of test cases that exposes the same bugs as the entire test suite. To show that the greedy heuristic does not always produce the smallest cover, running the program on `non_optimal.json` will produce a cover of 3 subsets, when the optimal cover requires only 2. Finally, `gen.json` and `big.json` are randomly generated test cases using `generator.py`, which is invoked with the following options.

`python3 generator.py` [options]:

  -u, --universe INTEGER : Size of the universe of integers, counting up.

  -n, --num (INTEGER, INTEGER) : Bounds on the number of subsets in the cover.

  -s, --size (INTEGER, INTEGER) : Bounds on the size of any given subset.

  -o, --output PATH : JSON file in which to write test case. [required]

  --help : Show this message and exit.
