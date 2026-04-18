from argparse import ArgumentParser
from pathlib import Path
from typing import Literal

from omniocr import OmniOcr
from omniocr.types import MarkdownResponse

import os


def main():
    parser = ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("model", type=str)
    parser.add_argument("--format", type=str, default="markdown")
    parser.add_argument("--pages", type=str, default="")
    parser.add_argument("--api-key", type=str, default=os.getenv("OMNIOCR_API_KEY"))
    args = parser.parse_args()

    client = OmniOcr(api_key=args.api_key)

    response = client.process(
        file=args.document,
        model=args.model,
        pages=args.pages or None,
        response_format=args.format,
    )

    if not response.error and isinstance(response.content, MarkdownResponse):
        print(response.content.markdown)



if __name__ == "__main__":
    main()
