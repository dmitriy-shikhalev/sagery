from sagery.schema import Saga, Stream


class Manager:
    def __init__(self, saga: Saga, streams: dict[str, Stream]):
        self.saga = saga
        self.streams = streams
