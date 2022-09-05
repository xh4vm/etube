import uuid
from typing import Any

from api.utils.decorators import traced
from flask_sqlalchemy import Pagination
from user_agents.parsers import UserAgent

from ..model.models import SignInHistory
from ..schema.base import Page, Paginator, SignInRecord, SignInRecordMap
from .storage.base import BaseStorage


class SignInHistoryService:
    def __init__(self, storage_svc: BaseStorage) -> None:
        self.storage_svc = storage_svc

    @traced('sign_in_history::create')
    def create_record(self, user_id: uuid.UUID, user_agent: UserAgent) -> None:
        record = SignInRecordMap(
            user_id=user_id, os=user_agent.get_os(), browser=user_agent.get_browser(), device=user_agent.get_device()
        )
        SignInHistory(**record.dict()).insert_and_commit()

    @traced('sign_in_history::all')
    def get_records(self, paginator: Paginator, user_id: uuid.UUID) -> Page[SignInRecord]:
        keys_values = [f'{key}::{value}' for key, value in paginator.dict().items()]
        storage_key: str = f'sign_in_history::get_records::{"::".join(keys_values)}'
        records: dict[str, Any] = self.storage_svc.get(key=storage_key)

        if records is not None:
            return Page(
                page=records.get('page'),
                page_size=records.get('page_size'),
                page_next=records.get('next_num'),
                page_prev=records.get('prev_num'),
                total=records.get('total'),
                items=[
                    SignInRecord(
                        os=record.get('os'),
                        device=record.get('device'),
                        browser=record.get('browser'),
                        created_at=record.get('created_at'),
                    )
                    for record in records.get('items')
                ],
            )

        records: Pagination = (
            SignInHistory.query.filter_by(user_id=user_id)
            .order_by(SignInHistory.created_at.desc())
            .paginate(page=paginator.page, per_page=paginator.page_size)
        )

        page_racords = Page(
            page=records.page,
            page_size=records.per_page,
            page_next=records.next_num,
            page_prev=records.prev_num,
            total=records.total,
            items=[
                SignInRecord(
                    os=record.os,
                    device=record.device,
                    browser=record.browser,
                    created_at=record.created_at.strftime('%d.%m.%Y'),
                )
                for record in records.items
            ],
        )

        self.storage_svc.set(key=storage_key, data=page_racords.dict())
        return page_racords
