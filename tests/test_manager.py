from unittest.mock import Mock

from sagery.manager import Manager


class TestManager:
    def test_init(self) -> None:
        saga = Mock()
        streams = Mock()

        manager = Manager(saga, streams)
        assert manager.saga == saga
        assert manager.streams == streams
