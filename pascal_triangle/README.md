# Pascal Triangle in Python

## Overview

This module uses Python 3.8's a new feature 'math.comb'
to calculate [Pascal Triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) 
and prints it into standard output e.g.

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



## Explained 

To get every number [binomial coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient) must computed and 
it's done by calculating number of Combinations for specific place
by using [combination formula](https://en.wikipedia.org/wiki/Combination)
givig row number as number of elements and column no as number of choices.
