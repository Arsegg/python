from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from random import choice, randrange, normalvariate
from sys import argv
from typing import Iterator, NoReturn, Tuple
from uuid import uuid4


def _generate(log: str, encoding: str, v: int, current: int, from_: datetime, to: datetime, step: int,
              size: int) -> NoReturn:
    def generate() -> Iterator[str]:
        yield "META DATA:"
        yield str(v)
        yield str(current)
        timestamp = from_
        choices = "wanna top up", "wanna scoop",
        while timestamp < to:
            isoFormat = timestamp.isoformat(sep="Т",  # NB: "Т" is cyrillic letter (ord("Т") == 1058)
                                            timespec="milliseconds")
            userName = f"username{uuid4()}"
            action = choice(choices)
            amount = int(normalvariate(v / 2, v / 4))  # NB: amount can be negative or greater than v
            # NB: "–" is en dash (ord("–") == 8211)
            # NB: "-" is hyphen minus (ord("-") == 45)
            yield f"{isoFormat}Z – [{userName}] - {action} {amount}l"
            milliseconds = randrange(1, step)
            timestamp += timedelta(milliseconds=milliseconds)

    with open(log, "w", encoding=encoding) as f:
        for row in generate():
            print(row, file=f)
            size -= len(row)
            if size < 0:
                break


def main(*args: str) -> NoReturn:
    """Check two string for equality.

    Args:
        args (str): arguments.
    """
    args = _parseArgs(args)
    _generate(args.log, args.encoding, args.v, args.current, getattr(args, "from"), args.to, args.step, args.size)


def _parseArgs(args: Tuple[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("log", default="log.log", nargs="?", help="log filename", type=str)
    parser.add_argument("encoding", default="utf-8", nargs="?", help="log file encoding", type=str)
    parser.add_argument("v", default=200, nargs="?", help="volume of barrel", type=int)
    parser.add_argument("current", default=30, nargs="?", help="current volume of barrel", type=int)
    parser.add_argument("from", default="2020-01-01T12:00:00", nargs="?", help="start of interval",
                        type=datetime.fromisoformat)
    parser.add_argument("to", default="2021-01-01T13:00:00", nargs="?", help="end of interval",
                        type=datetime.fromisoformat)
    parser.add_argument("step", default=2645, nargs="?", help="step of interval", type=int)
    parser.add_argument("size", default=2 ** 20, nargs="?", help="size of log file", type=int)
    return parser.parse_args(args)


if __name__ == "__main__":
    main(*argv[1:])
