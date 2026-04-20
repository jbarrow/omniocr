from pydantic import BaseModel, AfterValidator, Field
from typing import Annotated
from pathlib import Path
from PIL import Image

from omniocr.types import OcrResponse, CostBreakdown

import requests
import os
import mimetypes


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
    base_url: str = Field(
        default_factory=lambda: os.getenv("OMNIOCR_BASE_URL", "https://omniocr.ai")
    )

    @property
    def _ocr_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/api/v1/ocr"

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
        if isinstance(file, str):
            file = Path(file)

        if isinstance(file, Image.Image):
            # TODO(joe): allow for the OCR'ing of PIL images
            pass

        page_range: str | None = None
        if isinstance(pages, str):
            page_range = pages
        elif isinstance(pages, list):
            page_range = ",".join(str(p) for p in pages)

        content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"

        data: dict[str, str] = {"model": model, "response_format": response_format}
        if page_range is not None:
            data["page_range"] = page_range

        with open(file, "rb") as fp:
            response = requests.post(
                self._ocr_url,
                files={"file": (file.name, fp, content_type)},
                data=data,
                headers=self._headers,
            )

        if response.status_code != 200:
            return OcrResponse(
                content=[],
                page_count=0,
                success=False,
                error=f"{response.status_code}: {response.text}",
                cost_breakdown=CostBreakdown(),
            )

        return OcrResponse.model_validate_json(response.content)
