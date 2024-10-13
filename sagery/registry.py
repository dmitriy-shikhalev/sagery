class _Registry:
    def __init__(self):
        self._registry = {}

    def register(self, name: str, klass):
        """
        Register a new class.
        """
        self._registry[name] = klass

    def get(self, name: str):
        """
        Get a class by name.
        """
        return self._registry.get(name)


job_registry = _Registry()
operator_registry = _Registry()


def collect_all(jobs: list[str], operators: list[str]):
    """
    Collect all registered classes: jobs and operators.
    """
    raise NotImplementedError
