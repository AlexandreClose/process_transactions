import os
from airflow.providers.postgres.hooks.postgres import PostgresHook

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
def dump_transactions():
    ps_pg_hook = PostgresHook(postgres_conn_id="airflow_db")
    conn_ps = ps_pg_hook.get_conn()
    query = """
        SELECT *
        from transactions
    """
    cur = conn_ps.cursor()
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    with open(AIRFLOW_HOME + '/data/output/output_transactions.csv', 'w') as f:
        cur.copy_expert(outputquery, f)
    conn_ps.close()
