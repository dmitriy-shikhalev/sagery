from unittest.mock import AsyncMock, Mock, patch

import pytest

from sagery.enums import OperatorStatus
from sagery.operators import sum_2


class _Exception(Exception):
    pass


class TestSum2Operator:
    @patch("sagery.operators.asyncio.Queue")
    def test_init_ok(self, queue_mock: Mock) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)

        assert operator.kwargs == {}
        queue_mock.assert_not_called()
        assert operator._queues == queues
        assert operator.timeout == timeout

    def test_status_empty(self) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        assert operator.status == OperatorStatus.NOT_STARTED

    def test_status_done_false(self) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        operator.task = Mock(done=Mock(return_value=False))
        assert operator.status == OperatorStatus.RUNNING

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_not_called()
        operator.task.exception.assert_not_called()

    def test_status_done_true_cancelled_true(self) -> None:
        queues = Mock()
        operator = sum_2(queues)
        operator.task = Mock(done=Mock(return_value=True), cancelled=Mock(return_value=True))
        assert operator.status == OperatorStatus.ABORTED

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_not_called()

    def test_status_done_true_cancelled_false_exception_not_null(self) -> None:
        queues = Mock()
        operator = sum_2(queues)
        operator.task = Mock(
            done=Mock(return_value=True), cancelled=Mock(return_value=False), exception=Mock(return_value=Mock())
        )
        assert operator.status == OperatorStatus.ERROR

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_called_once_with()

    def test_status_done_true_cancelled_false_exception_null(self) -> None:
        queues = Mock()
        operator = sum_2(queues)
        operator.task = Mock(
            done=Mock(return_value=True), cancelled=Mock(return_value=False), exception=Mock(return_value=None)
        )
        assert operator.status == OperatorStatus.DONE

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_called_once_with()

    async def test_start_with_task(self) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        operator.task = Mock()
        with pytest.raises(ValueError):
            await operator.start()

    @patch("sagery.operators.asyncio.create_task")
    async def test_start_without_task(self, create_task_mock: Mock) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        with patch.object(operator, "_run_handler", new_callable=Mock, return_value=Mock()) as _run_handler_mock:
            await operator.start()

            _run_handler_mock.assert_called_once_with()
            create_task_mock.assert_called_once_with(_run_handler_mock.return_value)
            assert operator.task == create_task_mock.return_value

    async def test_run_handler_ok(self) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        with patch.object(operator, "run") as run_mock:
            await operator._run_handler()

            run_mock.assert_called_once_with()

    async def test_run_handler_error(self) -> None:
        queues = Mock()
        timeout = Mock()
        operator = sum_2(queues, timeout)
        with patch.object(operator, "run", side_effect=_Exception()) as run_mock:
            with pytest.raises(_Exception):
                await operator._run_handler()

            run_mock.assert_called_once_with()

    async def test_run_ok(self) -> None:
        queues = {"a": Mock(get=AsyncMock(return_value=1)), "b": Mock(get=AsyncMock(return_value=2)), "c": AsyncMock()}
        operator = sum_2(queues)  # type: ignore[arg-type]

        await operator.run()

        queues["a"].get.assert_called_once_with()
        queues["b"].get.assert_called_once_with()
        queues["c"].put.assert_called_once_with(3)
