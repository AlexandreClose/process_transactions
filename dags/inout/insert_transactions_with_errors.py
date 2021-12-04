import os

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

def insert_transactions():
    ps_pg_hook = PostgresHook(postgres_conn_id="airflow_db")
    conn_ps = ps_pg_hook.get_conn()
    transactions = pd.read_csv(AIRFLOW_HOME + '/data/input/transactions_with_unexpected_amount.csv')

    if len(transactions) > 0:
        col_names = ['id', 'amount', 'wording']
        values = transactions[col_names].to_dict('split')
        values = values['data']
        logging.info( values)
        insert_sql = """
                    INSERT INTO transactions (id, amount, wording) 
                    VALUES %s
                    ON CONFLICT DO NOTHING
                    """
        execute_values(conn_ps.cursor(), insert_sql, values, page_size=len(transactions))
        conn_ps.commit()
    else:
        None

    return None