from typing import Any


def header_extractor(context : dict[str, Any], key: str):
        header_value = context.get(key)

        if header_value is None or not isinstance(header_value, str):
            return None

        return header_value
