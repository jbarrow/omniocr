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


