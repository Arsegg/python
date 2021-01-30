from argparse import ArgumentParser, Namespace
from string import printable
from sys import argv
from typing import NoReturn, Tuple


def _check_range(base: int, name: str = "baseSrc") -> NoReturn:
    if not 2 <= base <= 36:
        raise ValueError(f"{name}: expected number between 2 and 36, got {base}")


def itoBase(nb: str, baseSrc: int, baseDst: int = 10) -> str:
    """Convert a number or string to string.

    Args:
        nb (str): a number.
        baseSrc (int): a source base.
        baseDst (int): a destination base.

    Returns:
        A string.

    Raises:
        ValueError: An error occurred when baseSrc or baseDst is not between 2 and 36 (inclusive).
    """
    _check_range(baseSrc)
    _check_range(baseDst, "baseDst")

    def _itoBase(n, result):
        if n < baseDst:
            result.append(printable[n])
            return result
        d, r = divmod(n, baseDst)
        result.append(printable[r])
        return _itoBase(d, result)

    decimal = int(nb, baseSrc)
    return "".join(reversed(_itoBase(decimal, [])))


def main(*args: str) -> NoReturn:
    """Convert a number from arguments and print it.

    Args:
        args (str): arguments.
    """
    args = _parseArgs(args)
    result = itoBase(args.nb, args.baseSrc, args.baseDst)
    print(result)


def _parseArgs(args: Tuple[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("nb", help="a number", type=str)
    parser.add_argument("baseSrc", default=10, help="a source base", nargs="?", type=int)
    parser.add_argument("baseDst", metavar="base", help="a destination base", type=int)
    return parser.parse_args(args)


if __name__ == "__main__":
    main(*argv[1:])
