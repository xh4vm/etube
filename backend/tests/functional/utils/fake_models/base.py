import uuid

from faker import Faker

fake = Faker()


def get_new_id() -> str:
    return str(uuid.uuid4())
