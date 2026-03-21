from anyocr import AsyncAnyOcr

import asyncio


client = AsyncAnyOcr()

async def main():
    response = await client.process(
        "examples/resources/sample.pdf",
        response_format="blocks"
    )

    for page in response:
        for block in response.blocks:
            print(block.content)


if __name__ == "__main__":
    asyncio.run(main())
