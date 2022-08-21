from ...fake_models.sign_in_history import FakeSignInHistory
from .base import BasePostgresDataGenerator


class HistoryDataGenerator(BasePostgresDataGenerator):
    table = 'sign_in_history'
    fake_model = FakeSignInHistory
