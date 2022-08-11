import re
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, Column, BigInteger, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.scoping import scoped_session

db = SQLAlchemy()


class BaseModel(db.Model):
    """Базовая модель объекта БД"""

    __abstract__ = True

    session: scoped_session = db.session

    id: int = Column(BigInteger().with_variant(Integer, 'sqlite'), nullable=False, unique=True, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        """Имя таблицы в базе данных"""
        
        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower() + 's'

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
