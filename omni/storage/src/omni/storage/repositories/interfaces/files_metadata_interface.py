from interface import Interface

from ...schemas.file_metadata_schema import (
    FileMetadata,
    FileMetadataCreate,
    FileMetadataUpdate,
)
from ...utils.app_types import Id


class IFilesMetadataRepository(Interface):
    def create(self, file_metadata: FileMetadataCreate) -> Id:
        pass

    def read(self, id: Id) -> FileMetadata:
        pass

    def update(self, id: Id, file_metadata: FileMetadataUpdate) -> None:
        pass

    def delete(self, id: Id) -> None:
        pass
