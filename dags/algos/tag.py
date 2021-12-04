from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values
from models.transaction import Transaction


def run_algo_tag():
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
    transactions_tagged = []
    for row in rows:
        transaction_iter = Transaction( row[0], row[1], row[2] )
        transactions.append( transaction_iter )
    cur.close()
    conn_ps.close()

    POTENTIAL_TAGS: Tuple[str, ...] = ('TATA', 'TOTO', 'TUTU', 'TAXI')

    for transaction_iter in transactions:
        tags=[{
                'tag': tag,
            }
            for tags in (tuple(tag for tag in POTENTIAL_TAGS if tag in transaction_iter.wording),)
            for tag in (tags if len(tags) == 1 else (None,))
        ]
        transaction_iter.tag = tags[0]["tag"]
        transactions_tagged.append(transaction_iter)
    transactions_tagged_values=[]
    for  transactions_annoted_iter in transactions_tagged:
        transactions_tagged_values.append([transactions_annoted_iter.id,transactions_annoted_iter.tag])

    conn_ps = ps_pg_hook.get_conn()
    update_with_tags = """
        update transactions as t set
            tag = t2.tag
        from (values
            %s
        ) as t2(id, tag) 
        where t2.id = t.id
        """
    execute_values(conn_ps.cursor(), update_with_tags, transactions_tagged_values, page_size=len(transactions_tagged_values))
    conn_ps.commit()
    conn_ps.close()
