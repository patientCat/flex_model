from typing import Dict
from ..db_context import context

"""
process select
"""


class Selector:
    def __init__(self, main_table: context.Table, select_dict: Dict, schema_holder=None):
        self.main_table = main_table
        self.select_dict = select_dict
        self.schema_holder = schema_holder

    def valid(self):
        pass
