from pathlib import Path
from typing import Literal
from pydantic import BaseModel


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


class OcrRequest(BaseModel):
    """OCR request format:

    Args:
        file_path: the local path of the file
        page_range: the list of pages to be processed, or None for all pages
                    (default is None)
        response_format: what format you want the OCR to be returned in.
    """
    file_path: str | Path
    page_range: list[int] | None = None
    response_format: Literal["markdown", "html", "blocks"]


class MarkdownResponse(BaseModel):
    markdown: str
    images: dict[str, str]
    page_index: int


class HtmlResponse(BaseModel):
    html: str
    images: dict[str, str]
    page_index: int


class BlockResponse(BaseModel):
    """
    Args:
        blocks: a reading-order sorted list of content blocks on the page,
                if the page supports bounding-box out; otherwise just a single
                block for markdown or HTML content
        page_index: the 0-indexed integer for the page
    """
    blocks: list[LayoutBlock]
    images: dict[str, str]
    page_index: int


class CostBreakdown(BaseModel):
    pass


class OcrResponse(BaseModel):
    """OCR response format:

    Args:
        content:
    """
    content: list[MarkdownResponse | HtmlResponse | JsonResponse]
    page_count: int
    success: bool
    error: str | None = None
    cost_breakdown: CostBreakdown
