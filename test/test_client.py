import os
import pytest

from pydantic import ValidationError


def test_client_requires_apy_key():
    os.environ["OMNIOCR_API_KEY"] = ""

    from omniocr import OmniOcr
    with pytest.raises(ValidationError):
        client = OmniOcr()

def test_create_client_with_api_key():
    from omniocr import OmniOcr
    client = OmniOcr(api_key="Empty")
