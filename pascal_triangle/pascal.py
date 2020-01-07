"""
    This module uses Python 3.8's a new feature
    'math.comb'
    to calculate Pascal's Triangle (https://en.wikipedia.org/wiki/Pascal%27s_triangle)
    and prints it into standard output
    e.g.
                     1
                    1 1
                   1 2 1
                  1 3 3 1
                 1 4 6 4 1
               1 5 10 10 5 1
              1 6 15 20 15 6 1
            1 7 21 35 35 21 7 1
           1 8 28 56 70 56 28 8 1
        1 9 36 84 126 126 84 36 9 1

"""

import math
import sys
import logging


def bin_expans(row, col):
    """
        Calculate binomial coefficient
    """
    nCr = math.comb(row, col)
    return nCr


def build_triangle(rows = 10):
    """
        Calculate triangle  
    """
    triangle = [[str(bin_expans(row, col))
                    for col in range(row+1)] 
                        for row in range(rows)]
    return triangle


def print_nicely(pascal_triangle):
    """
       Print a Pascal's Triangle
       iterable of iterables i.e. line and col
    """
    for _row in pascal_triangle:
        str_row = " ".join(_row)
        last_row_len = len(" ".join(pascal_triangle[len(pascal_triangle)-1]))
        print(str_row.center(last_row_len, ' '))


if __name__ == "__main__":

    # Extract Python version info    
    ver_major, ver_minor, _, _, _ = sys.version_info
    
    # Check if version is correct: should be above 3.8
    if (ver_major*10 + ver_minor) < 38:
        logger = logging.getLogger(__name__)
        logging.warning("**** Python version must be above or equal to 3.8 for this module to work "
                        "as it uses a new math's modules Combinatorial (math.comb) API ****")
        exit()

    # Check if a line argument is supplied and is valid
    no_of_rows = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10

    # Build and print
    pascal_triangle = build_triangle(int(no_of_rows))
    print_nicely(pascal_triangle)
    

