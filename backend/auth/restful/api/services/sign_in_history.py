import uuid

from user_agents.parsers import UserAgent

from ..model.models import SignInHistory
from ..schema.base import SignInRecord, SignInRecordMap


class SignInHistoryService:
    def create_record(self, user_id: uuid.UUID, user_agent: UserAgent) -> None:
        record = SignInRecordMap(
            user_id=user_id, os=user_agent.get_os(), browser=user_agent.get_browser(), device=user_agent.get_device()
        )
        SignInHistory(**record.dict()).insert_and_commit()

    def get_records(self, user_id: uuid.UUID) -> list[SignInRecord]:
        records = SignInHistory.query.filter_by(user_id=user_id).all()
        return [SignInRecord(os=record.os, device=record.device, browser=record.browser) for record in records]
