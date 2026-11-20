from unittest.mock import Mock

from sagery.storage import Storage


class TestStorage:
    def test_init(self) -> None:
        sagas_dict = Mock()
        storage = Storage(sagas_dict)
        assert sagas_dict == storage.sagas_dict
