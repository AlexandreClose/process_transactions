import os

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator

from algos.annotation import run_algo_annotation
from algos.tag import run_algo_tag
from inout.dump_transactions import dump_transactions
from inout.generate_error_report import generate_report
from inout.insert_transactions_with_errors import insert_transactions

args = {
    'owner': 'Alexandre Close',
    'start_date': days_ago(1)
}

dag = DAG(dag_id='transactions_dag_with_errors', default_args=args, schedule_interval=None)

with dag:
    task_delete_table_transactions = PostgresOperator(task_id='delete_table_transactions',
                                                      sql=("drop table if exists transactions "),
                                                      postgres_conn_id='airflow_db',
                                                      autocommit=True,
                                                      dag=dag)

    task_create_table_transactions = PostgresOperator(task_id='create_table_transactions',
                             sql=("create table if not exists transactions " +
                                  "(" +
                                  "id serial primary key, " +
                                  "amount double precision, " +
                                  "wording varchar(500), " +
                                  "tag varchar(500), " +
                                  "annotation varchar(15) " +
                                  ")"),
                             postgres_conn_id='airflow_db',
                             autocommit=True,
                             dag=dag)

    task_populate_table_transactions = PythonOperator(
        task_id='populate_table_transactions',
        python_callable=insert_transactions
    )

    task_dump_table_transactions_to_csv = PythonOperator(
        task_id='dump_table_transactions_to_csv',
        python_callable=dump_transactions,
        trigger_rule = "all_done"
    )

    task_run_algo_annotation = PythonOperator(
        task_id='run_algo_annotation',
        python_callable=run_algo_annotation,
        on_failure_callback = generate_report
    )

    task_run_algo_tag = PythonOperator(
        task_id='run_algo_tag',
        python_callable=run_algo_tag,

    )

    # this is the way to chain the task with specific operators. the algo are branched into individual tasks
    task_delete_table_transactions>> task_create_table_transactions >> task_populate_table_transactions >>  [task_run_algo_annotation,task_run_algo_tag] >> task_dump_table_transactions_to_csv