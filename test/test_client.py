import os
import pytest

from pydantic import ValidationError


def test_client_requires_apy_key():
    os.environ["ANYOCR_API_KEY"] = ""

    from anyocr import AnyOcr
    with pytest.raises(ValidationError):
        client = AnyOcr()

def test_create_client_with_api_key():
    from anyocr import AnyOcr
    client = AnyOcr(api_key="Empty")
