'''
Links:
------
https://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
'''
from sqlalchemy import (
    Column,
    String,
    Integer,
    Sequence,
    DateTime
)
from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship

from ...utils.sqlalchemy_base_model import SQLBaseModel

class UserModel(SQLBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, nullable=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)

    file_metadata = relationship("FileMetadataModel")

    def __init__(self, username, email, password, name, updated_at=datetime.now(), created_at=datetime.now()):
        self.username = username
        self.email = email
        self.password = bcrypt.encrypt(password)
        self.name = name
        self.updated_at = updated_at
        self.created_at = created_at

    def __repr__(self):
        return "<User(username='%s', name='%s', email='%s', password=*****, updated_at=%s, created_at='%s')>" % (self.username, self.name, self.email, self.updated_at, self.created_at)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)
