from sqlalchemy import DECIMAL, String, Date, MetaData
from db.lib import LabeledColumn, LabeledTable, make_select_list, table_reader

db_schema = 'Findb.dbo'
daily_rates_tbl = LabeledTable(
                     'daily_rates', MetaData()
                     , LabeledColumn('RateDate', Date, select_exp="format(RateDate, 'yyyyMMdd')")
                     , LabeledColumn('Country', String)
                     , LabeledColumn('Value', DECIMAL)
                     , schema=db_schema
                     )


def get_all_rates(connection):
    select_list = make_select_list(daily_rates_tbl.select_columns_exp_dict)
    df = table_reader(
                      connection
                      , columns=select_list
                      , table=f'{db_schema}.{daily_rates_tbl.name}'
                      )
    return df

