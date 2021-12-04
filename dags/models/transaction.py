from typing import List


class Transaction:

    def __init__(self, id , amount, wording ):
        self.id = id
        self.amount = amount
        self.wording = wording
        self.has_error_tags = False
        self.has_error_annotations = False

    def set_tag(self, tag : str):
        self.tag = tag

    def set_error_tag(self):
        self.has_error_tag = True

    def set_error_annotation(self):
        self.has_error_annotation = True

    def set_annotation(self, annotation : str):
        self.annotation = annotation