from unittest.mock import Mock

from sagery.manager import Manager


class TestManager:
    def test_init(self) -> None:
        saga = Mock()

        manager = Manager(saga)
        assert manager.saga == saga
