from ..testdata.films import films

def generate_docs(index: str) -> list:
    match index:
        case _:
            return films


def del_docs(index: str) -> list:
    match index:
        case _:
            docs = films

    return [
        {'_op_type': 'delete', '_index': index, '_id': doc['_id']}
        for doc in docs
    ]
