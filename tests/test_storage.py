from unittest.mock import Mock, patch

from sagery.storage import Storage


class TestStorage:
    def test_init(self) -> None:
        sagas_dict = Mock()
        storage = Storage(sagas_dict)
        assert sagas_dict == storage.sagas_dict

    def test_getitem(self) -> None:
        job = Mock()
        sagas_dict = Mock()
        storage = Storage(sagas_dict)

        with patch.object(storage, "_storage", {job.id: job}):
            assert storage[job.id] == job
