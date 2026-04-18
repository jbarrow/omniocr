from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated
from pathlib import Path
from urllib.parse import urljoin
from PIL import Image

from omniocr.types import OcrResponse, CostBreakdown
from omniocr.utils import _process_page_range

import requests
import os


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


class OmniOcr(BaseModel):
    api_key: Annotated[str, AfterValidator(_api_key_exists)] = Field(
        default=os.getenv("OMNIOCR_API_KEY", ""), validate_default=True
    )
    base_url: str | None = os.getenv("OMNIOCR_BASE_URL", "http://localhost:8000")

    @property
    def _ocr_url(self) -> str:
        return urljoin(self.base_url, "api/v1/ocr")
    
    @property
    def _headers(self) -> dict[str, str]:
        return {"X-API-KEY": self.api_key}

    def process(
        self,
        file: Path | str | Image.Image,
        model: str,
        pages: str | list[int] | None = None,
        response_format: str = "markdown",
    ) -> OcrResponse:
        # TODO(joe): add exponential backoff
        if isinstance(pages, str):
            pages = _process_page_range(pages)
        
        if isinstance(file, str):
            file = Path(file)
            file_name = file.name

        if isinstance(file, Image.Image):
            # TODO(joe): allow for the OCR'ing of PIL images
            pass

        with open(file, "r") as fp:
            response = requests.post(
                self._ocr_url,
                files={"file": (file_name, fp, "application/pdf")},
                data={
                    "page_range": pages,
                    "response_format": "markdown",
                },
                headers=self._headers
            )

            print(response)

        return OcrResponse(
            content=[],
            page_count=0,
            success=False,
            error="Not implemented",
            cost_breakdown=CostBreakdown()
        )



