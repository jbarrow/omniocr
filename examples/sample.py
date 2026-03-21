from anyocr import AnyOcr


client = AnyOcr()

def main():
    response = client.process(
        "examples/resources/sample.pdf",
        response_format="blocks"
    )

    for page in response:
        for block in response.blocks:
            print(block.content)

if __name__ == "__main__":
    main()
