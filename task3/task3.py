from argparse import ArgumentParser, Namespace
from collections import namedtuple
from csv import DictWriter
from datetime import datetime
from re import compile
from sys import argv
from typing import Iterator, NoReturn, Tuple


def _solution(log: str, encoding: str, from_: datetime, to: datetime) -> NoReturn:
    Row = namedtuple("Row", "timestamp username action amount")
    Result = namedtuple("Result", "attempts percent succeeded failed")
    ResultSummary = namedtuple("Result", "scoop topUp")
    pattern = compile(
        r"(?P<TIMESTAMP>.*)Z – \[(?P<USERNAME>.*)\] - (?P<ACTION>wanna top up|wanna scoop) (?P<AMOUNT>.*)l")

    def parse(row: str) -> Row:
        mo = pattern.match(row)
        if mo is None:
            raise ValueError(f"{row} does not match {pattern}")
        timestamp, username, action, amount = mo.groups()
        timestamp = datetime.fromisoformat(timestamp)
        amount = int(amount)
        return Row(timestamp, username, action, amount)

    def isTimeStampInInterval(row: Row) -> bool:
        return from_ <= row.timestamp <= to

    def solution(it: Iterator[str]) -> ResultSummary:
        META_DATA = "META DATA:"
        actual = next(it)
        if actual != META_DATA:
            raise ValueError(f"Expected {META_DATA}, got {actual}")
        v = int(next(it))
        current = int(next(it))
        filtered = filter(isTimeStampInInterval, map(parse, it))
        results = tuple([0] * 4 for _ in range(2))
        for row in filtered:
            isTopUp = row.action == "wanna top up"
            results[isTopUp][0] += 1  # attempts
            amount = row.amount if isTopUp else -row.amount
            newV = current + amount
            if 0 <= row.amount <= v and 0 <= newV <= v:
                current = newV
                results[isTopUp][2] += row.amount  # succeeded transfer
            else:
                results[isTopUp][1] += 1  # errors
                results[isTopUp][3] += row.amount  # failed transfer
        for i in range(2):
            if results[i][0]:
                results[i][1] = results[i][1] / results[i][0]  # percent of errors
        return ResultSummary(*map(lambda result: Result(*result), results))

    with open(log, encoding=encoding) as f, open(f"{log}.csv", "w", encoding=encoding, newline="") as out:
        stripped = map(lambda s: s.rstrip("\n"), f)
        summary = solution(stripped)
        row = {f"{action}{column.capitalize()}": amount for action, result in summary._asdict().items()
               for column, amount in result._asdict().items()}
        csv = DictWriter(out, row.keys())
        csv.writeheader()
        csv.writerow(row)


def main(*args: str) -> NoReturn:
    """Check log file  .

    Args:
        args (str): arguments.
    """
    args = _parseArgs(args)
    _solution(args.log, args.encoding, getattr(args, "from"), args.to)


def _parseArgs(args: Tuple[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("log", help="a log filename", type=str)
    parser.add_argument("encoding", default="utf-8", nargs="?", help="a log filename", type=str)
    parser.add_argument("from", help="start of interval", type=datetime.fromisoformat)
    parser.add_argument("to", help="end of interval", type=datetime.fromisoformat)
    return parser.parse_args(args)


if __name__ == "__main__":
    main(*argv[1:])
