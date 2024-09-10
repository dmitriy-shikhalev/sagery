from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class Job:
    terms: tuple[Term, ...]

    @classmethod
    def from_string(cls, string: str) -> "Job":
        lines = string.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        terms = [
            Term.from_string(line)
            for line in lines
        ]
        if not terms:
            raise ValueError("Empty job string")
        return cls(terms=tuple(terms))


@dataclass(frozen=True)
class Term:
    pairs: tuple[Pair, ...]
    call: Call

    @classmethod
    def from_string(cls, string: str) -> Term:
        left, right = string.split('=')
        left = left.strip()
        right = right.strip()

        pairs = tuple(map(Pair.from_string, left.split(',')))
        call = Call.from_string(right)

        return cls(pairs=pairs, call=call)


@dataclass(frozen=True)
class Pair:
    first_name: str
    second_name: str

    @classmethod
    def from_string(cls, string: str) -> Pair:
        first_name, second_name = string.split(':')
        first_name = first_name.strip()
        second_name = second_name.strip()

        return cls(first_name=first_name, second_name=second_name)


@dataclass(frozen=True)
class Call:
    function: str
    args: tuple[Argument, ...]

    @classmethod
    def from_string(cls, string: str) -> Call:
        function, others = string.split('(')
        function = function.strip()

        args = others.split(')')[0]
        args = args.split(',')
        arguments = tuple(map(Argument.from_string, args))

        return cls(function=function, args=arguments)


class Operator(StrEnum):
    MULTIPLY = '*'


@dataclass(frozen=True)
class Argument:
    names: tuple[str, ...]
    operator: Operator | None = None

    @classmethod
    def from_string(cls, string: str) -> Argument:
        string = string.strip()
        if Operator.MULTIPLY in string:
            names = string.split(Operator.MULTIPLY)
            names = tuple(map(str.strip, names))

            operator = Operator.MULTIPLY
        else:
            names = [string]

            operator = None
        return Argument(names, operator)
