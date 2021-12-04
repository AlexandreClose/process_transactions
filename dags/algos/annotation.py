from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values

from models.transaction import Transaction


def run_algo_annotation():
    algo_contains_error = False
    ps_pg_hook = PostgresHook(postgres_conn_id="airflow_db")
    conn_ps = ps_pg_hook.get_conn()
    query = """
        SELECT *
        from transactions
    """
    cur = conn_ps.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    transactions = []
    transactions_annoted = []
    for row in rows:
        transaction_iter = Transaction( row[0], row[1], row[2] )
        transactions.append( transaction_iter )
    cur.close()
    conn_ps.close()

    for transaction_iter in transactions:
        amount_iter = transaction_iter.amount
        transaction_iter.annotation = str( 'ERROR' if amount_iter >= 100000 else
                                           'LARGE SALE' if amount_iter > 300. and amount_iter < 100000 else
                                           'SALE' if amount_iter > 0. else
                                           'EXPENSE' if amount_iter < -200. else
                                           'SMALL EXPENSE')
        transactions_annoted.append(transaction_iter)
    transactions_annoted_values=[]
    for  transactions_annoted_iter in transactions_annoted:
        transactions_annoted_values.append([transactions_annoted_iter.id,transactions_annoted_iter.annotation])
        if transactions_annoted_iter.annotation == 'ERROR':
            algo_contains_error = True


    conn_ps = ps_pg_hook.get_conn()
    update_with_annotations = """
        update transactions as t set
            annotation = t2.annotation
        from (values
            %s
        ) as t2(id, annotation) 
        where t2.id = t.id
        """
    execute_values(conn_ps.cursor(), update_with_annotations, transactions_annoted_values, page_size=len(transactions_annoted_values))
    conn_ps.commit()
    conn_ps.close()
    if algo_contains_error:
        raise ValueError('Unexpected amount. Please see the report')



