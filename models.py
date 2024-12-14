from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    chat_id = Column(BigInteger, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_selected = Column(Boolean, default=False)
