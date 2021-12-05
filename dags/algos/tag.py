from typing import Tuple

from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from psycopg2.extras import execute_values
from models.transaction import Transaction
from algos.base_algo import BaseAlgo


class TagAlgo ( BaseAlgo ):

    def __init__(self):
        super().__init__()

    def run_total_algo(self):
        super().run_total_algo( )

    def process_algo( self, transaction ):
        POTENTIAL_TAGS: Tuple[str, ...] = ('TATA', 'TOTO', 'TUTU', 'TAXI')

        tags=[{
                'tag': tag,
            }
            for tags in (tuple(tag for tag in POTENTIAL_TAGS if tag in transaction.wording),)
            for tag in (tags if len(tags) == 1 else (None,))
        ]
        transaction.set_tag(tags[0]["tag"])
        return transaction

    def get_computed_value(self, transaction):
        return transaction.tag

    def get_field_name (self ):
        return "tag"