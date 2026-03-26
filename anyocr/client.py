from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated
from pathlib import Path
from urllib.parse import urljoin

from anyocr.types import OcrResponse, OcrRequest, CostBreakdown

import os


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


def _api_key_exists(value: str):
    """Validator to ensure that an API key exists (either through environment
    variables, or provided during client creation. Note that I use the
    combination of: AfterValidator, and Field(..., validate_default=True) to
    validate the os.environment variable in case no key is provided.

    Args:
        value: the current field value

    Returns:
        the passed in value, after checking that it's non-empty
    """
    if not value.strip():
        raise ValueError("No API key provided")
    return value.strip()


class AnyOcr(BaseModel):
    api_key: Annotated[str, AfterValidator(_api_key_exists)] = Field(
        default=os.getenv("ANYOCR_API_KEY", ""), validate_default=True
    )
    base_url: str | None = os.getenv("ANYOCR_BASE_URL", "http://localhost:7000")

    @property
    def _ocr_url(self) -> str:
        return urljoin(self.base_url, "api/v1/ocr")
    
    @property
    def _headers(self) -> dict[str, str]:
        return {"X-API-Key": self.api_key}

    def process(
        self,
        file: Path | str,
        model: str,
        pages: str | list[int] | None = None,
        response_format: str = "markdown",
    ) -> OcrResponse:
        if isinstance(pages, str):
            pages = _process_page_range(pages)
        
        if isinstance(file, str):
            file = Path(file)

        with open(file, "rb") as fp:
            response = requests.post(
                self._ocr_url,
                files={"file": (file.name, fp, "application/pdf")},
                data={
                    "page_range": pages,
                    "response_format": "markdown",
                },
                headers=self._headers
            )

        return OcrResponse(
            content=[],
            page_count=0,
            success=False,
            error="Not implemented",
            cost_breakdown=CostBreakdown()
        )



