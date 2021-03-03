import numpy as np

def check_sudoku(grid):

    # For each element in grid
    for i in range(0,arr.shape[0]):
        for j in range(0,arr.shape[1]):

            # Checks if value is unique in row and column
            if np.count_nonzero(arr[i,:] == grid[i,j]) != 1:
                return False
            elif np.count_nonzero(arr[:,j] == grid[i,j]) != 1:
                return False

    # Also check disjoint 3x3 squares for uniqueness
    for i in np.arange(1,arr.shape[0]-1, step = 3):
        for j in np.arange(1,arr.shape[1]-1, step = 3):
            if len(np.unique(grid[i-1:i+2,j-1:j+2])) != 9:
                return False
    return True

sudoku = """145327698
            839654127
            672918543
            496185372
            218473956
            753296481
            367542819
            984761235
            521839764"""

# String grid to numpy array
arr = [[int(i) for i in line] for line in sudoku.split()]
arr = np.array(arr)
print(check_sudoku(arr))