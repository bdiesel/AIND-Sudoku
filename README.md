# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?

A: We look for two squares in the same unit that both have the same two possible values. Using the {'A1': '18', 'A8':'18'} as an example twin pair we can conclude that 1 and 8 must be in A1 and A8. Although this does not tell us which value belongs in which square, it does impose a constraint which allows 1 and 8 to be eliminated from every other square in the unit vector thus reducing the search space.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?

A: Constraint propagation in diagonal sudoku problem applies the same constraint propagation techniques as regular sudoku problem along a new unit vector. In the diagonal problem the sames rules of elimination, only_choice, assign, and later naked_twins are applied iteratively so that a value appears only once along the new unit vector.



### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.