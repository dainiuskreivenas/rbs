# Introduction 
This is a RBS (Rule Based System). Build rules using facts that are cached to neurons and ran on NEST or SpiNNaker.

# How to Use It

View [Wiki](https://github.com/dainiuskreivenas/rbs/wiki) for more information


# Examples

## Monkey and Banana Problem

The monkey and banana problems is a famous toy problem in artificial intelligence, particularly in logic programming and planning. 

A monkey is in a room. Suspended from the ceiling is a bunch of bananas, beyond the monkey's reach. However, in the room there are also a chair and a stick. The ceiling is just the right height so that a monkey standing on a chair could knock the bananas down with the stick. The monkey knows how to move around, carry other things around, reach for the bananas.

Monkey problem code is located at the ./monkeys folder.

To run the tests:

1. Open terminal at root of the Repository
2. type ./monkeys/run.sh

The results will be printed out to ./monkeys/tests/results

## Tower of Hanoi

The Tower of Hanoi is a mathematical game or puzzle. It consists of three rods and a number of disks of different sizes, which can slide onto any rod. The puzzle starts with the disks in a neat stack in ascending order of size on one rod, the smallest at the top, thus making a conical shape. 

ToH code is located at the ./toh folder.

To run the tests:

1. Open terminal at root of the Repository
2. type ./toh/run.sh

The results will be printed out to ./toh/tests/results

## Sudoku

Sudoku is a logic-based, combinatorial number-placement puzzle. The objective is to fill a 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") contain all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a well-posed puzzle has a single solution.

Sudoku code is located at the ./sudoku folder.

To run the 6x6 tests:

1. Open terminal at root of the Repository
2. Type: python ./sudoku/tests/Sudoku6_Test.py > ./sudoku/tests/results/sudoku6.txt
3. Press enter

To run the 9x9 tests:

1. Open terminal at root of the Repository
2. Type: python ./sudoku/tests/Sudoku9_Test.py > ./sudoku/tests/results/sudoku9.txt
3. Press enter

The results will be printed out to "./sudoku/tests/results" folder