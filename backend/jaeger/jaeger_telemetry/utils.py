

def header_extractor(request, key: str):
        header_value = request.headers.get(key)

        if header_value is None or not isinstance(header_value, str):
            return None

        return header_value
