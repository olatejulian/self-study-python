from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Sequence,
    ForeignKey
)
from datetime import datetime

from ...utils.sqlalchemy_base_model import SQLBaseModel

class FilesMetadataModel(SQLBaseModel):
    __tablename__ = 'files_metadata'

    id = Column(Integer, Sequence('file_metadata_seq'), primary_key=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    path = Column(String, unique=True, nullable=False)
    url_path = Column(String, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey('users.id'))
    expire_at = Column(DateTime, default=None, nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, name, path, url_path, client_id, expire_at, updated_at, create_at):
        self.name = name
        self.path = path
        self.url_path = url_path
        self.client_id = client_id
        self.expire_at = expire_at
        self.updated_at = updated_at
        self.create_at = create_at

    def __repr__(self):
        return "<FileMetadata(name='%s', path='%s', url_path='%s', client_id='%s', expire_at='%s', updated_at='%s', create_at='%s')>" % (self.name, self.path, self.url_path, self.client_id, self.expire_at, self.updated_at, self.create_at)
