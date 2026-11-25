from sagery.schema import Saga


class Manager:
    def __init__(self, saga: Saga):
        self.saga = saga
