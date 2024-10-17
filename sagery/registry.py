from sagery.sagas import AbstractSaga


class _Registry:
    def __init__(self):
        self._registry = {}

    def register(self, name: str, klass):
        """Register a new class."""
        self._registry[name] = klass

    def get(self, name: str) -> AbstractSaga:
        """Get a class by name."""
        return self._registry.get(name)


SAGA_REGISTRY = _Registry()
OPERATOR_REGISTRY = _Registry()


def collect_all(jobs: list[str], operators: list[str]):
    """Collect all registered classes: jobs and operators."""
    raise NotImplementedError
