import os

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
def delete_output_files( ):
    dir = AIRFLOW_HOME + '/data/output/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
