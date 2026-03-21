from pydantic import BaseModel
from pathlib import Path

import os


class BoundingBox(BaseModel):
    """
    xyxyn storage of bounding box (all values are 0/1 normalized)
    """
    x0: float
    y0: float
    x1: float
    y1: float


class LayoutBlock(BaseModel):
    bounding_box: BoundingBox
    label: str
    content: str


class OcrResponse(BaseModel):
    """OCR response format:

    Args:
        blocks: a reading-order sorted list of content blocks on the page,
                if the page supports bounding-box out; otherwise just a single
                block for markdown or HTML content
        page_index: the 0-indexed integer for the page
    """
    blocks: list[LayoutBlock]
    page_index: int


# question: how do I represent (a) markdown, (b) html, (c) blocks all separately?


def _process_page_range(page_range: str) -> list[int]:
    """Convert a string page range to a list of pages. For instance: "0-2,4,6"
    should be converted to [0, 1, 2, 4, 6]. Raises an exception if the range isn't
    valid (e.g. 4-2).

    Args:
        page_range: the string representation of the desired page range, supporting
                    '-' and ',' as separators. Note that '-' is *inclusive*.

    Returns:
        the list of integers represented by the page range
    """
    pages  = []
    groups = page_range.split(",")

    for group in groups:
        endpoints = group.split("-")

        if len(endpoints) == 2:
            start, end = endpoints
            start, end = int(start), int(end)

            if start > end:
                raise ValueError(f"page range ({page_range}) is not valid")

            pages.extend(range(start, end+1))
        elif len(endpoints) == 1:
            page = endpoints[0]
            pages.append(int(page))
        else:
            raise ValueError(f"page range ({page_range}) not valid")

    return pages


class AnyOcr(BaseModel):
    api_key: str | None = os.getenv("anyocr_api_key")
    base_url: str | None = os.getenv("anyocr_base_url", "http://localhost:7000")
    
    def process(
        file: Path | str,
        pages: str | list[int] | None = None
    ) -> OcrResponse:
        if isinstance(pages, str):
            pages = _process_page_range(pages)


class AsyncAnyOcr(AnyOcr):
    async def process(
        file: Path | str,
        pages: str | list[int] | None = None
    ) -> OcrResponse:
        if isinstance(pages, str):
            pages = _process_page_range(pages)
