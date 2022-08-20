import re
from datetime import datetime

from core.config import CONFIG
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.scoping import scoped_session

db = SQLAlchemy()


class BaseModel(db.Model):
    """Базовая модель объекта БД"""

    __abstract__ = True
    __table_args__ = {'schema': CONFIG.DB.SCHEMA_NAME}

    session: scoped_session = db.session

    id: int = Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @declared_attr
    def __tablename__(cls):
        """Имя таблицы в базе данных"""

        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower() + 's'

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)

    # TODO обрабатывать исключения от бд чтобы не блочить работу
    def insert_and_commit(self):
        db.session.add(self)
        db.session.commit()
