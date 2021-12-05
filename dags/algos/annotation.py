from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values

from models.transaction import Transaction

from algos.base_algo import BaseAlgo


class AnnotationAlgo(BaseAlgo):

    def __init__(self):
        super().__init__()

    def run_total_algo(self):
        super().run_total_algo( )

    def process_algo( self, transaction ):
        amount_iter = transaction.amount
        # I added a way to simulate error when the amount is over 100000
        transaction.set_annotation(str('ERROR' if amount_iter >= 100000 else
                                            'LARGE SALE' if amount_iter > 300. and amount_iter < 100000 else
                                            'SALE' if amount_iter > 0. else
                                            'EXPENSE' if amount_iter < -200. else
                                            'SMALL EXPENSE'))
        return transaction

    def get_computed_value(self, transaction):
        return transaction.annotation

    def get_field_name (self ):
        return "annotation"
