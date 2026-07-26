import asyncio
import sys


async def async_sum_nums(args: list[str]) -> int:
    return sum(map(int, args))


operators = {
    "sum": async_sum_nums,
}


def main() -> None:
    if len(sys.argv) < 2:
        raise RuntimeError("Use: `sagery sum 1 2`")
    else:
        operator_name = sys.argv[1]
        operator = operators.get(operator_name)
        if operator is None:
            raise RuntimeError(f"There is no operator `{operator_name}`")

        result = asyncio.run(operator(sys.argv[2:]))
        print(f"Result is {result}")
