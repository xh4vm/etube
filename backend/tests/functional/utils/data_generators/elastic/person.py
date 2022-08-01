"""
Генерации фейковых данных, которые используются для тестов.

"""



from .base import BaseElasticDataGenerator
from ...fake_models import FakePerson


class PersonDataGenerator(BaseElasticDataGenerator):
    index = 'persons'
    fake_model = FakePerson
