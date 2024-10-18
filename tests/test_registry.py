from unittest.mock import Mock

from sagery import registry


def test_class_registry():  # noqa: D103
    name = "test_name"
    klass = Mock(__name__=name)

    r = registry.Registry()
    r.register(klass)

    assert r.get(name) == klass


def test_collect_all():  # noqa: D103
    registry.collect_all(["tests.example.sagas:ExampleSaga"], ["tests.example.operators:ExampleOperator"])

    assert registry.SAGA_REGISTRY.get("ExampleSaga") is not None
    assert registry.OPERATOR_REGISTRY.get("ExampleOperator") is not None
