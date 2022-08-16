import uuid
from user_agents.parsers import UserAgent

from ..schema.base import SignInRecord
from ..model.models import SignInHistory


class SignInHistoryService:

    def create_record(self, user_id: uuid.UUID, user_agent: UserAgent) -> None:
        record = SignInRecord(
            user_id=user_id, 
            os=user_agent.get_os(), 
            browser=user_agent.get_browser(),
            device=user_agent.get_device()
        )
        SignInHistory(**record.dict()).insert_and_commit()

    def get_records(self, user_id: uuid.UUID):
        pass
