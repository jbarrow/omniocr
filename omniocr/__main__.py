from argparse import ArgumentParser
from pathlib import Path
import sys

from omniocr import OmniOcr
from omniocr.types import MarkdownResponse

import os


def main():
    parser = ArgumentParser()
    parser.add_argument("document", type=Path, nargs="?")
    parser.add_argument("--model", type=str)
    parser.add_argument("--format", type=str, default="markdown")
    parser.add_argument("--pages", type=str, default="")
    parser.add_argument("--api-key", type=str, default=os.getenv("OMNIOCR_API_KEY"))
    parser.add_argument(
        "--resume",
        type=str,
        default=None,
        help="Resume polling an existing job by id instead of uploading a new document.",
    )
    parser.add_argument(
        "--submit-only",
        action="store_true",
        help="Upload and submit the job, print the job id, and exit without polling.",
    )
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=None)
    args = parser.parse_args()

    client = OmniOcr(api_key=args.api_key)

    if args.resume:
        response = client.resume(
            args.resume, interval=args.poll_interval, timeout=args.timeout,
        )
    else:
        if args.document is None or args.model is None:
            parser.error("document and --model are required unless --resume is used")

        if args.submit_only:
            job_id = client.submit(
                file=args.document,
                model=args.model,
                pages=args.pages or None,
                response_format=args.format,
            )
            print(job_id)
            return

        response = client.process(
            file=args.document,
            model=args.model,
            pages=args.pages or None,
            response_format=args.format,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )

    if response.error:
        print(f"Error: {response.error}", file=sys.stderr)
        sys.exit(1)

    for page in response.content:
        if isinstance(page, MarkdownResponse):
            print(page.markdown)


if __name__ == "__main__":
    main()
