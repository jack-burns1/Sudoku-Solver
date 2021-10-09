# Jack Burns
# April, 2021
# sudoku.py
# A sudoku solver that implements csp backtracking 

import sys
from timeit import default_timer as timer

# Type for every cell on the sudoku board
# Each cell holds a domain, (empty if cell already had a value)
# current value, size of the domain, and index on the board
class Variable:
    def __init__(self, currVal, pos, size):
        if size == 9:
            self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.domain = []
        self.currVal = currVal
        self.domainSize = size
        self.pos = pos

    # Remove a given number from a cell's domain
    def remove_from_domain(self, val):
        if val in self.domain:
            self.domain.remove(val)
            self.domainSize -= 1

    # Add a given number to a cell's domain
    def add_to_domain(self, val):
        self.domain.append(val)
        self.domainSize += 1

    # Set the current value of the cell to 1 <= n <= 9
    def set_value(self, val):
        self.currVal = val

# Type for the entire csp
# Contains a 1D array of Variables representing board,
# Array of board indexes that contain blank cells,
# size of the variable index array at the start, and
# current size of the variable index array
class Problem:
    def __init__(self, board, variables, size):
        self.board = board
        self.variables = variables
        self.size = size
        self.currSize = size

# Type for an assignment to a variable
# Contains the value to change the variable to (1 - 9),
# the variable index to be changed, and the list of variable indexes, whose
# domains need to be stripped of value given this assignment.
class Assignment:
    def __init__(self, value, variable, pruned):
        self.value = value
        self.variable = variable
        self.pruned = pruned

# Read board from the command line as a text file
# Convert every character read in into a variable, and populate a board
# with those variables, as well as creating a list of variable indexes
# Adds this data to a problem and returns it.
def readInput():
    board = []
    variables = []
    numSpaces = 0

    if len(sys.argv) == 2:
        inFile = sys.argv[1]

        with open(inFile, "r") as fp:
            for line in fp:

                for i in range(9):
                    if line[i] == '-':
                        board.append(Variable(0, len(board), 9))
                        variables.append(len(board) - 1)   # index of variables in board
                        numSpaces += 1

                    else:
                        board.append(Variable(line[i], len(board), 0))
        return Problem(board, variables, numSpaces)
    return None

# Main backtracking solver function
# Calls the recursive function and returns its value
def backtrack(csp):
    return backtrack_recurse([], csp)

# Recursive backtracking function
# Takes in a list of assignments and the problem
# Recursively solves the csp, and returns the list of assignments that lead
# to the correct solution
def backtrack_recurse(assignment, csp):
    if is_complete(assignment, csp) == True:
        return assignment

    # Find index of Variable to solve for
    var = select(csp)
    i = 0
    toAdd = []
    # Check every value in the variable's domain
    while i < csp.board[var].domainSize:
       
        # Check if domain value works given sudoku's constraints 
        assign = check(var, csp.board[var].domain[i], csp)
        if assign != False:
            # Add assignment to list of assignments, and recurse
            add_result(assign, csp, assignment)
            result = backtrack_recurse(assignment, csp)

            if result != None:
                return result
            # If there is a conflict, remove the assignment
            remove_assignment(assign, assignment, csp)
            toAdd.append(assign.value)

    if len(toAdd) != 0:
        # An assignment that does not work but could possibly work if a 
        # previous value on the board is changed added back to domain
        for i in range(len(toAdd)):
            add_back_to_domain(csp, var, toAdd[i])
        

    return None

# Takes in the index of a variable to change, a domain value to change it to,
# and the problem.
# Checks if it is a valid move, and keeps track of the indexes it would need
# to prune given the assignment (prune = remove value from domain)
# Returns False if value does't work, and an assignment with value if it does
def check(pos, value, csp):
    row = check_row(csp.board, pos, value)
    # If value does not work, it must be removed from the domain
    if row == None:
        csp.board[pos].remove_from_domain(value) 
        return False

    col = check_col(csp.board, pos, value)
    if col == None:
        csp.board[pos].remove_from_domain(value)
        return False

    box = check_box(csp.board, pos, value)
    if box == None:
        csp.board[pos].remove_from_domain(value)
        return False

    toPrune = row + col + box
    # Get rid of repeats in the list of pruned indexes
    toPrune = list(set(toPrune))

    return Assignment(value, csp.board[pos], toPrune)

# Check if board is complete
# Board is complete when every blank cell has been added to assignments
# True if all assignments were added, and False if not
def is_complete(assignment, csp):
    if len(assignment) != csp.size:
        return False,

    return True

# Select best variable to pick assignment for based on the smallest domain size
# Takes in the porblem, and returns a board index of a variable to change
def select(csp):
    currMin = 10
    index = 0
    i = 0
    for i in range(csp.currSize):
        if csp.board[csp.variables[i]].domainSize < currMin:
            currMin = csp.board[csp.variables[i]].domainSize
            index = i

    return csp.variables[index]

# Checks row of a given index if value can be added given sudoku constraints
# Takes in the board, variable index, and potential value to add.
# Returns None if it does not work, and returns list of indexes it would need
# to prune given the assignment if it does work.
def check_row(board, index, value):
    pruned = []
    i = index
    rowSize = 9

    # Find row start index given any index
    while i % rowSize != 0:
        i -= 1

    for j in range(i, i + 9):

        if str(value) == str(board[j].currVal):
            return None
        
        if board[j].currVal == 0 and j != index:
            # Add to list of pruned indexes
            if value in board[j].domain:
                pruned.append(j)
    
    return pruned

# Checks column of a given index if value can be added given sudoku constraints
# Takes in the board, variable index, and potential value to add.
# Returns None if it does not work, and returns list of indexes it would need
# to prune given the assignment if it does work.
def check_col(board, index, value):
    pruned = []
    # Find index of beginning of column for any index
    i = index % 9
    colSize = 9

    for j in range(colSize):

        if str(value) == board[i].currVal:
            return None

        if board[i].currVal == 0 and i != index:
            # Add to list of pruned indexes
            if value in board[i].domain:
                pruned.append(i)

        i += 9

    return pruned
# Checks box of a given index if value can be added given sudoku constraints
# Takes in the board, variable index, and potential value to add.
# Returns None if it does not work, and returns list of indexes it would need
# to prune given the assignment if it does work.
def check_box(board, index, value):
    blockSize = 9
    pruned = []

    # Find first index of box (3x3) given any index
    col = int(index % 9 / 3) 
    row = int(index / 9 / 3) 

    i = (27 * row) + (3 * col)
    # Must traverse box like a 3 x 3 2D array
    for j in range(int(blockSize / 3)):
        for k in range(int(blockSize / 3)):

            if str(value) == board[i].currVal:
                return None

            if board[i].currVal == 0 and i != index:
                #Add to list of pruned indexes
                if value in board[i].domain:
                    pruned.append(i)
            i += 1
        i += blockSize - 3

    return pruned

# Takes in a valid assignment, the problem, and the list of assignments
# Add assignment to the assignments list, and change the current value at
# the given cell to the assignment's value
def add_result(result, csp, assignment):
    toPrune = len(result.pruned)
    # Remove value from domain of variables at indexes found in check()
    for i in range(toPrune):
        csp.board[result.pruned[i]].remove_from_domain(result.value)

    assignment.append(result)
    # Must remove value from current variable's domain.
    csp.board[result.variable.pos].remove_from_domain(result.value)

    result.variable.currVal = result.value
    csp.board[result.variable.pos].currVal = result.value

    # Remove variables from list of variables to be changed.
    csp.variables.remove(int(result.variable.pos))
    csp.currSize -= 1
   
# Takes in a previous assignment, the list of assignments, and the problem
# Removes the assignment from the list, and resets the variable's value to 0
# Used when we must backtrack, and try a new assignment for given variable
def remove_assignment(assign, assignment, csp):
    # 'unprune' values from variables at indexes found in check()
    toPrune = len(assign.pruned)
    for i in range(toPrune):
        csp.board[assign.pruned[i]].add_to_domain(assign.value)

    assignment.remove(assign)

    assign.variable.currVal = 0
    csp.board[assign.variable.pos].currVal = 0

    # Add variable back to list of variables needed to change
    csp.variables.append(assign.variable.pos)
    csp.currSize += 1

# Takes in the problem, index of a variable, and a value (1 - 9)
# Adds the value to the back of the domain of variable at index
# Used when we must backtrack, and given value does not work with the
# current configuration but could work given other variables change.
def add_back_to_domain(csp, pos, value):
    csp.board[pos].add_to_domain(value)

# Print state of the puzzle board
# Takes in the problem, and prints the entire board after it has been solved
def print_puzzle(csp):
    print("------Completed Puzzle:-------")
    for i in range(9):
        for j in range(9):
            print(csp.board[(i * 9) + j].currVal, end='')
        print('')
    print("------------------------------")

# Print the numerical values of the assignments it took to solve the puzzle
# Takes in the list of assignments when puzzle is solved.
def print_assignments(assignment):
    size = len(assignment)
    print("-Values used in the solution (in order of how the appear):-")
    for i in range(size):
        print(assignment[i].value, end='')
    print("\n----------------------------------------------------------")

# Takes in the problem
# Calls main backtrack function to solve the problem, and prints the solution
# Also times the algorithm, and prints the total elapsed time the algorithm
# takes
def run_backtrack(csp):
    start = timer()
    assignment = backtrack(csp)
    end = timer()
    print("-----Elapsed Time-------")
    print(end - start, " seconds")

    if assignment == None:
        print("No possible solutions for this Puzzle.")
        print("Are you sure you input in the correct format?")

    else:
        print_puzzle(csp)
        print_assignments(assignment)


csp = readInput()
if csp != None:
    run_backtrack(csp)
else:
    # If there is a problem reading the file
    print("Invalid input...")
    print("Please check if your input file is in the correct format.")