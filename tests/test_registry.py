from unittest.mock import Mock

from sagery import registry


def test_class_registry():  # noqa: D103
    name = "test_name"
    klass = Mock()

    r = registry._Registry()
    r.register(name, klass)

    assert r.get(name) == klass


def test_collect_all():  # noqa: D103
    registry.collect_all(["tests/example/jobs:ExampleJob"], [])
