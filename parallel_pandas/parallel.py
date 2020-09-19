from pathlib import Path
from typing import List
import multiprocessing as mpp
import pandas as pd


def process_file(f: Path, filter_string: str) -> pd.DataFrame:
    """
    Process single file:
     Load as Pandas Dataframe and filter my matching filter_string
    """
    df = pd.read_csv(f, header='infer')
    return df[df["Date"] == filter_string]


def process_files_sequentially(p: Path) -> List:
    """
    Process files one at a time by looping the given directory
    """
    all_dfs = []
    for f in p.glob('*.csv'):
        df = process_file(f, '1982-01-01')
        all_dfs.append(df)

    return all_dfs


def process_files_parallel(p: Path) -> List:
    """
    Process files in the folder by creating parallel loads
    It will create N parallel processes based on CPU count (vertical scaling)
    """
    p_args = []
    for f in p.glob('*.csv'):
        p_args.append([f, '1982-01-01'])

    with mpp.Pool() as p:
        all_dfs = p.starmap(process_file, p_args)

    return all_dfs


if __name__ == "__main__":
    """
    Main entry point for local test
    """
    path = Path('~/dev/test/exchange-rates/data/').expanduser()

    all_dfs_in_list_seq = process_files_sequentially(path)
    all_dfs_in_list_par = process_files_parallel(path)

    for p_df in all_dfs_in_list_seq:
        print(p_df.head())

    for p_df in all_dfs_in_list_par:
        print(p_df.head())

