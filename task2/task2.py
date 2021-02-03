from argparse import ArgumentParser, Namespace
from collections import namedtuple
from math import sqrt
from re import finditer
from sys import argv
from typing import Any, Iterator, NoReturn, Tuple

_Token = namedtuple("Token", "kind value")


def _tokenize(text: str) -> Iterator[_Token]:
    tokenSpec = (
        ("NUM", r"-?\d+(\.\d*)?"),
        ("LC", r"{"),
        ("RC", r"}"),
        ("LS", r"["),
        ("RS", r"]"),
        ("COL", r":"),
        ("SEP", r","),
        ("ID", r"\w+"),
        ("SKIP", r"[ \t]+"),
        ("MIS", r"."),
    )
    pattern = "|".join(f"(?P<{k}>{v})" for k, v in tokenSpec)
    for mo in finditer(pattern, text):
        kind = mo.lastgroup
        value = mo.group()
        yield _Token(kind, value)


def _parse(*tokens: _Token):
    def push(obj: Any):
        stack.append(obj)

    def pop():
        if not stack:
            raise ValueError(f"Stack is empty.")
        return stack.pop()

    stack = []
    for kind, value in tokens:
        if kind == "SKIP":
            continue
        if kind == "NUM":
            value = float(value) if "." in value else int(value)
        if value == "}":
            isDict = True
            entries = []
            while True:
                value = pop()
                if value == "{":
                    break
                if value == ",":
                    continue
                if not isDict:
                    if value == ":":
                        raise ValueError(f"Expected number, got {value}")
                    entries.append(value)
                    continue
                colon = pop()
                if colon != ":":
                    if entries:
                        print(stack, entries)
                        raise ValueError(f"Expected ':', got {colon}")
                    isDict = False
                    entries.append(value)
                    continue
                key = pop()
                entries.append((key, value,))
            entries.reverse()
            value = dict(entries) if isDict else frozenset(entries)
        if value == "]":
            values = []
            while True:
                value = stack.pop()
                if value == "[":
                    break
                if value == ",":
                    continue
                values.append(value)
            value = tuple(reversed(values))
        push(value)
    return pop()


def _find(data: dict) -> Tuple:
    def solution(t):
        return px * (1 - t) + t * qx, py * (1 - t) + t * qy, pz * (1 - t) + t * qz

    sphere = data["sphere"]
    cx, cy, cz = sphere["center"]
    radius = sphere["radius"]
    (px, py, pz), (qx, qy, qz) = data["line"]
    vx, vy, vz = qx - px, qy - py, qz - pz
    ux, uy, uz = px - cx, py - cy, pz - cz

    a = vx ** 2 + vy ** 2 + vz ** 2
    b = 2 * (ux * vx + uy * vy + uz * vz)
    c = ux ** 2 + uy ** 2 + uz ** 2 - radius ** 2
    d = b ** 2 - 4 * a * c
    if d < 0:
        return ()
    t1 = (-b - sqrt(d)) / 2 / a
    solution1 = solution(t1)
    if d == 0:
        return solution1,
    t2 = (-b + sqrt(d)) / 2 / a
    return solution1, solution(t2)


def _solution(filename: str) -> NoReturn:
    with open(filename) as f:
        print(f"Reading from {filename}...")
        raw = f.read()
        print(f"Tokenizing: {raw}...")
        tokens = tuple(_tokenize(raw))
        print(f"Parsing: {tokens}...")
        data = _parse(*tokens)
        print(f"Processing: {data}...")
        result = _find(data)
        print(f"Collisions: {result}")


def main(*args: str) -> NoReturn:
    """Find collisions.

    Args:
        args (str): arguments.
    """
    args = _parseArgs(args)
    _solution(args.filename)


def _parseArgs(args: Tuple[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("filename", help="a filename", type=str)
    return parser.parse_args(args)


if __name__ == "__main__":
    main(*argv[1:])
