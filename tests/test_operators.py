from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from sagery.enums import OperatorStatus
from sagery.operators import sum_2


class _Exception(Exception):
    pass


class TestSum2Operator:
    def test_init_fail(self) -> None:
        with pytest.raises(TypeError):
            _ = sum_2(1)  # type: ignore[call-arg]

    @patch("sagery.operators.asyncio.Queue")
    def test_init_ok(self, queue_mock: Mock) -> None:
        operator = sum_2(a="b", c="d")

        assert operator.kwargs == {"a": "b", "c": "d"}
        assert queue_mock.call_args_list == [call(), call()]
        assert operator.inputs == queue_mock.return_value
        assert operator.outputs == queue_mock.return_value

    def test_status_empty(self) -> None:
        operator = sum_2()
        assert operator.status == OperatorStatus.NOT_STARTED

    def test_status_done_false(self) -> None:
        operator = sum_2()
        operator.task = Mock(done=Mock(return_value=False))
        assert operator.status == OperatorStatus.RUNNING

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_not_called()
        operator.task.exception.assert_not_called()

    def test_status_done_true_cancelled_true(self) -> None:
        operator = sum_2()
        operator.task = Mock(done=Mock(return_value=True), cancelled=Mock(return_value=True))
        assert operator.status == OperatorStatus.ABORTED

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_not_called()

    def test_status_done_true_cancelled_false_exception_not_null(self) -> None:
        operator = sum_2()
        operator.task = Mock(
            done=Mock(return_value=True), cancelled=Mock(return_value=False), exception=Mock(return_value=Mock())
        )
        assert operator.status == OperatorStatus.ERROR

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_called_once_with()

    def test_status_done_true_cancelled_false_exception_null(self) -> None:
        operator = sum_2()
        operator.task = Mock(
            done=Mock(return_value=True), cancelled=Mock(return_value=False), exception=Mock(return_value=None)
        )
        assert operator.status == OperatorStatus.DONE

        operator.task.done.assert_called_once_with()
        operator.task.cancelled.assert_called_once_with()
        operator.task.exception.assert_called_once_with()

    def test_start_with_task(self) -> None:
        operator = sum_2()
        operator.task = Mock()
        with pytest.raises(ValueError):
            operator.start()

    @patch("sagery.operators.asyncio.create_task")
    def test_start_without_task(self, create_task_mock: Mock) -> None:
        operator = sum_2()
        with patch.object(operator, "_run_handler", new_callable=Mock, return_value=Mock()) as _run_handler_mock:
            operator.start()

            _run_handler_mock.assert_called_once_with()
            create_task_mock.assert_called_once_with(_run_handler_mock.return_value)
            assert operator.task == create_task_mock.return_value

    async def test_run_handler_ok(self) -> None:
        operator = sum_2()
        with patch.object(operator, "run") as run_mock:
            await operator._run_handler()

            run_mock.assert_called_once_with()

    async def test_run_handler_error(self) -> None:
        operator = sum_2()
        with patch.object(operator, "run", side_effect=_Exception()) as run_mock:
            with pytest.raises(_Exception):
                await operator._run_handler()

            run_mock.assert_called_once_with()

    async def test_run_ok(self) -> None:
        operator = sum_2()

        with (
            patch.object(operator, "inputs", Mock(get=AsyncMock(side_effect=[("a", 1), ("b", 2)]))) as inputs_mock,
            patch.object(operator, "outputs", Mock(put=AsyncMock())) as output_mock,
        ):
            await operator.run()

            assert inputs_mock.get.call_args_list == [call(), call()]
            output_mock.put.assert_called_once_with(("c", 3))

    async def test_run_1_arg_wrong(self) -> None:
        operator = sum_2()

        with (
            patch.object(operator, "inputs", Mock(get=AsyncMock(side_effect=[("b", 1), ("b", 2)]))) as inputs_mock,
            patch.object(operator, "outputs", Mock(put=AsyncMock())) as output_mock,
        ):
            with pytest.raises(NameError):
                await operator.run()

            assert inputs_mock.get.call_args_list == [call()]
            output_mock.put.assert_not_called()

    async def test_run_2_arg_wrong(self) -> None:
        operator = sum_2()

        with (
            patch.object(operator, "inputs", Mock(get=AsyncMock(side_effect=[("a", 1), ("a", 2)]))) as inputs_mock,
            patch.object(operator, "outputs", Mock(put=AsyncMock())) as output_mock,
        ):
            with pytest.raises(NameError):
                await operator.run()

            assert inputs_mock.get.call_args_list == [call(), call()]
            output_mock.put.assert_not_called()
