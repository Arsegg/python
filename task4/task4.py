from argparse import ArgumentParser, Namespace
from sys import argv
from typing import NoReturn, Tuple


def _isEqual(text: str, pattern: str) -> bool:
    n, m = len(text), len(pattern)
    if m == 0:
        return n == 0
    i, j = 0, 0
    indexText, indexPattern = -1, -1
    while i < n:
        if j < m and text[i] == pattern[j]:
            i += 1
            j += 1
        elif j < m and pattern[j] == "*":
            indexText = i
            indexPattern = j
            j += 1
        elif indexPattern >= 0:
            i = indexText + 1
            j = indexPattern + 1
            indexText += 1
        else:
            return False
    while j < m and pattern[j] == "*":
        j += 1
    return j == m


def main(*args: str) -> NoReturn:
    """Check two string for equality.

    Args:
        args (str): arguments.
    """
    args = _parseArgs(args)
    result = "ОК" if _isEqual(args.text, args.pattern) else "КО"
    print(result)


def _parseArgs(args: Tuple[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("text", help="a text", type=str)
    parser.add_argument("pattern", help="a pattern", type=str)
    return parser.parse_args(args)


if __name__ == "__main__":
    main(*argv[1:])
