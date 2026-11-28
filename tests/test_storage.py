from unittest.mock import Mock, patch

from sagery.storage import Storage


class TestStorage:
    def test_init(self) -> None:
        sagas_dict = Mock()
        storage = Storage(sagas_dict)
        assert sagas_dict == storage.sagas_dict

    @patch("sagery.storage.Job")
    def test_create_job(self, job_mock: Mock) -> None:
        saga_name = Mock()
        saga = Mock()
        comment = Mock()
        sagas_dict = {saga_name: saga}
        storage = Storage(sagas_dict)  # type: ignore[arg-type]

        job = storage.create_job(saga_name, comment)

        job_mock.assert_called_once_with(saga, comment)
        assert job.id in storage._storage
        assert storage._storage[job.id] == job
        assert job is job_mock.return_value

    def test_get_job(self) -> None:
        job = Mock()
        sagas_dict = Mock()
        storage = Storage(sagas_dict)

        with patch.object(storage, "_storage", {job.id: job}):
            assert storage.get_job(job.id) == job
