from argparse import ArgumentParser
from pathlib import Path
from typing import Literal


def main():
    parser = ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("--model", type=str)
    parser.add_argument("--format", type=str, default="markdown")
    parser.add_argument("--pages", type=str, default="")
    args = parser.parse_args()

    pass


if __name__ == "__main__":
    main()
