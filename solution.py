assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

      Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

      Returns:
         the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find an instance of naked twins
        unit_twins = find_unit_twins(unit, values)
        if(unit_twins):
            # Eliminate the naked twins as possibilities for their peers
            eliminate_twins(unit, unit_twins, values)
    return values


def find_unit_twins(unit, values):
    """Eliminate values using the naked twins strategy.

      Args:
        unit(array): an array of an axis of elments['A9', 'B8', ... 'I1']
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

      Returns:
         unit_twins(tuple) of matching values ('H4', 'H6')
    """
    unit_twins = {}  # holder for unit values
    for box in unit:
        if len(values[box]) == 2:  # the box has two possible values
            unit_twins[box] = values[box]  # asign the values to a key in the unit twin.
            if len(unit_twins) == 2:  # the unit list has two possible key value pairs
                valsar = tuple(unit_twins.values())
                if(valsar[0] == valsar[1]):
                    return tuple(unit_twins.keys())
                else:
                    return None
    return None


def eliminate_twins(unit, unit_twins, values):
    """
      We can therefore eliminate 2 and 6 from every other square in the A row unit.
      We could code that strategy in a few lines by adding an elif len(values[s]) == 2 test to eliminate.
    """
    box, twin_box = unit_twins[0], unit_twins[1]
    for target_box in set(peers[box]).intersection(peers[twin_box]):
        for digit in values[box]:
            # Remove the twin values
            assign_value(values, target_box, values[target_box].replace(digit, ''))


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in (
    'ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))],
                  [rows[i] + cols[len(cols)-1-i]
                   for i in range(len(rows))
                   ]
                  ]

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    chars = []
    ds = digits
    for c in grid:
        if c in ds:
            chars.append(c)
        if c == '.':
            chars.append(ds)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that
    only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    ds = digits
    for unit in unitlist:
        for digit in ds:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box
    with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same,
    return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = """2.............62....1....7.
                          ..6..8...3...9...7...6..4..
                          .4....8....52.............3"""
    # display(solve(grid_values(diag_sudoku_grid)))
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
