from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String

from ...utils.sqlalchemy_base_model import SQLBaseModel


class FilesMetadataModel(SQLBaseModel):
    __tablename__ = "files_metadata"

    id = Column(Integer, Sequence("file_metadata_seq"), primary_key=True, nullable=False)
    name = Column(String, unique=False, nullable=False)
    path = Column(String, unique=True, nullable=False)
    url_path = Column(String, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"))
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
        return f"<FileMetadata(name='{self.name}', path='{self.path}', url_path='{self.url_path}', client_id='{self.client_id}', expire_at='{self.expire_at}', updated_at='{self.updated_at}', create_at='{self.create_at}')>"
