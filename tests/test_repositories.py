import pytest

from sagery.repositories import AbstractRepository, SagaRepository


@pytest.mark.parametrize(
    ["klass"],
    [
        (SagaRepository,),
    ],
)
class TestRepository:
    def test(self, klass: AbstractRepository) -> None:
        pass
