import argparse
from pathlib import Path
from app import App


def parse_arguments():
    parser = argparse.ArgumentParser(description='Liability Cash Flow Generation Tool')
    parser.add_argument('--log',
                        action='store_true',
                        help='Log messages')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Save files in various stages into csv files')
    parser.add_argument('--debug_dir',
                        required=False,
                        help='Dir where to save CSV files to')
    parser.add_argument('--dbpwd',
                        required=False,
                        help='Password to SQL Server (for Linux ODBC drivers)')
    args = parser.parse_args()

    return args.log, args.debug, args.debug_dir, args.dbpwd


if __name__ == '__main__':
    """
    This small application demonstrates how it's to read from a CSV file and
    save it into a database.
    NOTE:
    There is some overhead here with date type (datetime64) when read 
    from a database which is relevant only in Linux and ok in Windows.  
    
    params: Supply password as a params when executed for Linux systems.
            No need in windows as you can save the password in the ODBC 
            connection settings 
    """
    # Parse arguments
    logging_enabled, debug_enabled, debug_dir, dbpwd = parse_arguments()

    print(f'Logging:{logging_enabled}')
    print(f'Debug:{debug_enabled}')
    print(f'Debug dir:{debug_dir}')

    # Initialise a global app
    # this will hold the state and components of the app
    app = App(log_flag=logging_enabled,
              debug_flag=debug_enabled,
              debug_dir=debug_dir,
              dbpwd=dbpwd)

    # Main implementation
    csv_path = Path('~/docker/test/exchange-rates/data')
    daily_csv_file = 'daily.csv'

    # Read file to a DataFrame
    csv_df = app.get_csv_data(csv_path.joinpath(daily_csv_file))
    csv_df = csv_df.astype({'Date': 'datetime64'})
    csv_df = csv_df.rename(columns={'Date': 'RateDate'})
    csv_df = csv_df.fillna(0)
    # Check the data
    app.debug_df('Rates from CSV:', csv_df)

    # Save Rates Into DB
    app.save_rates_into_db(csv_df)




