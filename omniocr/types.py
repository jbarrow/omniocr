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
    content: list[MarkdownResponse | HtmlResponse | BlockResponse]
    page_count: int
    success: bool
    error: str | None = None
    cost_breakdown: CostBreakdown


JobState = Literal["pending", "running", "completed", "failed"]


class JobStatus(BaseModel):
    """Status of an asynchronous OCR job.

    `result` is populated only when `status == "completed"`.
    `error` is populated when `status == "failed"`.
    """
    job_id: str
    status: JobState
    result: OcrResponse | None = None
    error: str | None = None
