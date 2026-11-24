from asyncio import Queue
from unittest.mock import Mock, patch

import pytest

from sagery import enums, operators, schema, settings

input_queue: Queue = Queue()
input_queue.put_nowait(None)

output_queue: Queue = Queue()

fake = operators.sum_2({"input_queue": input_queue}, {"output_queue": output_queue})


class TestSettings:
    def test_get_sagas_dict(self) -> None:
        settings_obj = settings.Settings(
            sagas=[settings.Saga(name="test", queues=[], operators=[])],
            api=settings.ApiSettings(host="test", port=123),
            queue=settings.QueueSettings(engine=enums.QueueEngine.LOCAL),
        )
        sagas = settings_obj.get_sagas_dict()
        assert len(sagas) == 1
        assert list(sagas.keys()) == ["test"]
        saga = list(sagas.values())[0]
        assert saga.name == "test"
        assert saga.queues == set()
        assert saga.operators == {}

    @patch("sagery.settings.YamlConfigSettingsSource")
    def test_settings_customise_sources(self, source_mock: Mock) -> None:
        settings_cls = Mock()
        init_settings = Mock()
        env_settings = Mock()
        dotenv_settings = Mock()
        file_secret_settings = Mock()

        with patch.object(settings.Settings, "config_file") as config_file:
            s = settings.Settings.settings_customise_sources(
                settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings
            )

            source_mock.assert_called_once_with(settings_cls, yaml_file=config_file)
            assert s == (init_settings, source_mock.return_value)


@pytest.fixture()
def operator_settings() -> settings.Operator:
    return settings.Operator(
        package="sagery",
        module="operators",
        klass="sum_2",
        name="sum2",
        inputs=["a", "b"],
        outputs=["c"],
        params={},
    )


@pytest.fixture()
def saga_settings(operator_settings: settings.Operator) -> settings.Saga:
    return settings.Saga(
        name="test saga",
        queues=["a", "b", "c"],
        operators=[operator_settings],
    )


class TestOperator:
    def test_get_operator_ok(self, operator_settings: settings.Operator) -> None:
        operator = operator_settings.get_operator()
        assert isinstance(operator, operators.sum_2)

    def test_get_operator_value_error(self, operator_settings: settings.Operator) -> None:
        with (
            pytest.raises(ValueError),
            patch.object(operator_settings, "module", "settings"),
            patch.object(operator_settings, "klass", "Operator"),
        ):
            operator_settings.get_operator()

    def test_to_model(self, operator_settings: settings.Operator) -> None:
        with patch.object(settings.Operator, "get_operator", return_value=fake) as get_operator_mock:
            model = operator_settings.to_model()
            assert isinstance(model, schema.Operator)
            assert model.name == "sum2"
            assert model.inputs == {"a", "b"}
            assert model.outputs == {"c"}
            get_operator_mock.assert_called_once_with()
            assert model.object == get_operator_mock.return_value


class TestSaga:
    def test_to_model(self, saga_settings: settings.Saga) -> None:
        saga = saga_settings.to_model()
        assert isinstance(saga, schema.Saga)
