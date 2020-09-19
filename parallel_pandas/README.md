# Parallel Python (Pandas example)

## Overview

This codes show how one can process data in parallel.
It demonstrates how to read files in parallel and convert to Pandas and do some transformation before returning.

It's demo code for below article:
[Parallel processing (Pandas example)](http://www.khalidmammadov.co.uk/parallel-processing-pandas-example)

## Run it

For Sequential test
```
import timeit
timeit.timeit("pp.process_files_sequentially(Path('~/dev/test/exchange-rates/data/').expanduser())", "from parallel_pandas import parallel as pp; from pathlib import Path", number=1000)
```

For Parallel test
```
import timeit
timeit.timeit("pp.process_files_parallel(Path('~/dev/test/exchange-rates/data/').expanduser())", "from parallel_pandas import parallel as pp; from pathlib import Path", number=1000)
```