import sqlalchemy as sqla
import platform


def new_connection(dsn_name, dbpwd=None):
    print('Creating new connection')

    if platform.system() == 'Linux':
        return sqla.create_engine(f"mssql+pyodbc://sa:{dbpwd}@{dsn_name}", echo=True).connect()

    return sqla.create_engine(f"mssql+pyodbc://{dsn_name}", echo=True).connect()

