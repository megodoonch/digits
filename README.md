# digits
Implementing a version of NYTimes Games' Digits

Authors: Meaghan Fowlie and Doug Barr

So far you can generate a random game with the same rules as the original and play it via the command line.

Usage: just run digits.py:

```bash
cd path/to/digits
python digits.py
```
The interface is the interactive command line prompt.

It will create a game with no one-step solution.

## To change the parameters of the game

Edit the script section at the bottom of `digits.py` before you run it.

Change `maximum_starter, maximum_intermediate_result, maximum_small_starter, max_target=500` to try to make the game easier or harder.

Change `negatives_allowed` to change whether we can get into negative numbers for the target and intermediate values.

Change `no_remainders_allowed` to change whether the win conditions include using up all digits.

## Solver

`solver.py` finds all solutions and partial solutions to a game.