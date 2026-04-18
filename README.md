# `omniocr`

Python packge for using OmniOcr: https://omniocr.ai

```
pip install omniocr
```

## Usage

Get your API key from: https://omniocr.ai/

Then you can start to OCR documents with:

```sh
export OMNIOCR_API_KEY=<OMNIOCR_API_KEY>

omniocr examples/resources/sample.pdf \
    --model=lightonocr-2-1b \
    --format=markdown \
    --pages "1-3" > output.md
```

Alternatively, you can run it programmatically:

```py
from omniocr import OmniOcr


client = OmniOcr()

document = client.process(
    "examples/resources/sample.pdf",
    model="lightonocr-2-1b",
    format="markdown",
    pages="1-3"
)

print(document)
```

## Formats

There are two _types_ of formats that `omniocr` supports:

1. markdown conversion -- this is the simplest, the document is just converted to markdown, typically with placeholders for images
2. block-based output -- if you need bounding boxes for _where_ the text comes from, you should use a model that supports bounding box outputs

## Supported Models


