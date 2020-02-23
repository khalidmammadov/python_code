import logging
import pandas as pd
from pathlib import Path
from time import time
from functools import wraps

from db.connection import new_connection
from db.lib import insert_rates, update_rates
from db.Findb.Daily_rates import daily_rates_tbl, get_all_rates
from util.config import load_config, get_config


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        logger = args[0].logger
        ts = time()
        logger.info('*' * 50)
        logger.info('Executing: {}()...'.format(f.__name__.upper()))
        logger.info('*' * 50)
        result = f(*args, **kw)
        te = time()
        logger.info('*' * 50)
        logger.info('{}() took: {:.0f}min {:.2f}sec '.format(f.__name__.upper(), (te-ts)/60, te-ts))
        logger.info('*' * 50)
        return result
    return wrap


class App(object):

    def __init__(self, log_flag=None, debug_flag=None, debug_dir=None, dbpwd=None):

        self.logger = App.set_up_logger(log_flag, debug_flag)
        self.debug_enabled = debug_flag
        self.debug_dir = None

        self.config = load_config('conf.ini')
        dsn_name = self.get_config('DSN', 'Name')
        self.db_connection = new_connection(dsn_name, dbpwd)

    @staticmethod
    def set_up_logger(log_flag, debug_flag):

        # Set logging level
        logging_level = logging.ERROR
        if log_flag:
            logging_level = logging.INFO

        if debug_flag:
            logging_level = logging.DEBUG

        # Setup logger
        logging.basicConfig(level=logging_level,
                            format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging_level)

        return logger

    def set_up_debug_dir(self):
        dir_ = None
        if self.debug_enabled:
            dir_ = Path(self.debug_dir)
            if not dir_.exists():
                raise Exception(f"Dir: {self.debug_dir} does not exists!")
        return dir_

    def debug_dump_df(self, name, df):

        # Check if folder setup
        if not self.debug_dir:
            self.debug_dir = App.set_up_debug_dir()

        if self.debug_enabled:
            file = self.debug_dir.joinpath(name).with_suffix('.csv')
            self.debug(f'Dumping into file: {file}')
            df.to_csv(file)

    def debug(self, msg):
        self.logger.debug(msg)

    def log(self, msg):
        self.logger.info(msg)

    def debug_df(self, title, df):
        self.debug('\n' + title + ' - (head) \n' + df.head().to_string())

    @timing
    def get_config(self, section, name):
        return get_config(self.config, section, name)

    @staticmethod
    def get_csv_data(file):
        return pd.read_csv(file)

    @timing
    def save_rates_into_db(self, rates_df):
        # Get rates from DB
        rates_db_df = get_all_rates(self.db_connection)
        rates_db_df = rates_db_df.astype({'RateDate': 'datetime64'})
        # Left Outer Join so we check for existence
        joined = pd.merge(rates_df,
                          rates_db_df,
                          left_on=['RateDate', 'Country'],
                          right_on=['RateDate', 'Country'],
                          how='left',
                          suffixes=['', '_table'])

        # Separate Inserts and updates
        cond = joined['Value_table'].isnull()
        inserts = joined[cond]
        updates = joined[~cond]

        # Check
        self.debug_df('Inserts:', inserts)
        self.debug_df('Updates:', updates)

        if inserts.index.size > 0:
            insert_rates(self.db_connection,
                         daily_rates_tbl,
                         inserts)

        if updates.index.size > 0:
            update_rates(self.db_connection,
                         daily_rates_tbl,
                         updates)

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()
            del self.db_connection
