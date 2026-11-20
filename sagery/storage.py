from sagery.models import Saga


class Storage:
    def __init__(self, sagas_dict: dict[str, Saga]):
        self.sagas_dict = sagas_dict
