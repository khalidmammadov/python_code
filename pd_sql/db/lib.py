import pandas as pd
from sqlalchemy import Column, Table, and_
from lib.converter import make_upsert_list, make_select_list


class Db:
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema
        self.db_schema = '.'.join([name, schema])


class LabeledColumn(Column):

    def __init__(self, name, *args, label=None, select_exp=None, **kwargs):
        Column.__init__(self, name, *args, **kwargs)
        self.label = label if label else name
        self.select_exp = select_exp


class LabeledTable(Table):

    def __init__(self, *args, **kwargs):
        Table.__init__(self, *args, **kwargs)

    @property
    def labels(self):
        return [col.label for col in self.columns]

    @property
    def column_label_dict(self):
        return {col.name: col.label for col in self.columns}

    @property
    def select_columns_exp_dict(self):
        return {col.select_exp
                if col.select_exp
                else col.name: col.label
                for col in self.columns}

    @property
    def select_columns_dict(self):
        return {col.name: col.label
                for col in self.columns}


def table_reader(connection, table, columns, condition=''):
    cond = '' if condition == '' else f'where {condition}'
    sql = 'select {} from {} {}'.format(','.join(columns), table, cond)

    return pd.read_sql(sql, connection)


def insert_rates(connection, table, inserts):
    # Make dictionary of parameters for the inserts
    ins_params = make_upsert_list(inserts)
    connection.execute(
        table.insert(),
        ins_params)


def update_rates(connection, table, updates):
    # Make dictionary of parameters for the updates
    upd_params = make_upsert_list(updates)
    # Execute statement (will autocommit)
    # Generate single updates
    for uld in upd_params:
        connection.execute(
            table.update().
                where(
                    and_(
                        table.c.RateDate == uld['RateDate'],
                        table.c.Country == uld['Country'])),
            upd_params)
