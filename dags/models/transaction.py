class Transaction:

    def __init__(self, id , amount, wording ):
        self.id = id
        self.amount = amount
        self.wording = wording

    def set_tag(self, tag : str):
        self.tag = tag

    def set_annotation(self, annotation : str):
        self.annotation = annotation