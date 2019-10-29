# Introduction 

This is N-ARC (Neural Cognitive Architecture). Build rules using facts and associative memory that are cached to neurons and ran on NEST or SpiNNaker platforms.

# How it Works

Adding Rules and Facts to the system produces python objects to represent neurons and synapses. These then are passed to the executor which uses pyNN simulator to create neurons and synapes on the Nest or spyNNaker platforms.

# How to Use It

View [Wiki](https://github.com/dainiuskreivenas/rbs/wiki) for more information.

# To Run Tests

1. Download Repository to {location}/rbs
2. Naviaget to {location}
3. Execute shell script command "./rbs/runTests.sh"

Results will be written to: "./rbs/tests/results.sp" file.

# Examples

Examples can be found in the following repositories:

* [Tower of Hanoi](https://github.com/dainiuskreivenas/tower-of-hanoi)
* [Sudoku](https://github.com/dainiuskreivenas/sudoku)
* [Parser](https://github.com/dainiuskreivenas/parser)
* [Monkey Problem](https://github.com/dainiuskreivenas/monkeys)
