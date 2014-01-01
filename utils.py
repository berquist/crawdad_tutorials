#!/usr/bin/env python2

def print_mat(mat):
    """Pretty-print a general NumPy matrix in a traditional format."""
    dim_rows, dim_cols = mat.shape
    # first, handle the column labels
    print(" " * 5),
    for i in range(dim_cols):
        print("{0:11d}".format(i+1)),
    print("")
    # then, handle the row labels
    for i in range(dim_rows):
        print("{0:5d}".format(i+1)),
        # print the matrix data
        for j in range(dim_cols):
            print("{0:11.7f}".format(mat[i][j])),
        print("")