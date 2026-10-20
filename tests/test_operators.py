import pytest

from sagery.operators import sum_2


async def test_sum_2() -> None:
    sum_2_launch = sum_2()
    generator = sum_2_launch.run()

    await anext(generator)
    await generator.asend(("a", 2))
    result = await generator.asend(("b", 3))
    assert result == ("c", 5)


async def test_sum_wrong_first_arg() -> None:
    sum_2_launch = sum_2()
    generator = sum_2_launch.run()

    await anext(generator)
    with pytest.raises(NameError):
        await generator.asend(("aa", 2))


async def test_sum_wrong_second_arg() -> None:
    sum_2_launch = sum_2()
    generator = sum_2_launch.run()

    await anext(generator)
    await generator.asend(("a", 2))
    with pytest.raises(NameError):
        await generator.asend(("bb", 3))
