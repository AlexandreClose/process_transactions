from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values

from models.transaction import Transaction

class BaseAlgo :

    def __init__(self):
        pass

    def process_algo(self):
        raise NotImplementedError

    def get_computed_value(self):
        raise NotImplementedError

    def get_field_name(self):
        raise NotImplementedError

    def run_total_algo( self ):
        algo_contains_error = False

        #Load the datas into Transactions objs.
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
        transactions_with_field = []
        for row in rows:
            transaction_iter = Transaction( row[0], row[1], row[2] )
            transactions.append( transaction_iter )
        cur.close()
        conn_ps.close()

        for transaction_iter in transactions:
            amount_iter = transaction_iter.amount
            transaction_iter = self.process_algo( transaction_iter )
            transactions_with_field.append(transaction_iter)
        transactions_with_field_values=[]
        for  transactions_with_field_iter in transactions_with_field:
            computed_value_iter = self.get_computed_value( transactions_with_field_iter )
            transactions_with_field_values.append([transactions_with_field_iter.id,computed_value_iter])
            if computed_value_iter == 'ERROR':
                algo_contains_error = True

        # update the transactions table with the annotation
        conn_ps = ps_pg_hook.get_conn()
        update_with_field_name = """
            update transactions as t set
                {field} = t2.{field}
            from (values
                %s
            ) as t2(id, {field}) 
            where t2.id = t.id
            """.format( field = self.get_field_name())
        execute_values(conn_ps.cursor(), update_with_field_name, transactions_with_field_values, page_size=len(transactions_with_field_values))
        conn_ps.commit()
        conn_ps.close()
        # if a transaction at least has an error, send a non blocking Error to inform the GUI that you need to consult the report.
        # this error will perform the error callback defined in the DAG
        if algo_contains_error:
            raise ValueError('Unexpected error. Please see the report output_transactions_in_error.csv')




