from interface import implements

from ...utils.app_types import Id
from ...schemas.file_metadata_schema import FileMetadataCreate, FileMetadataUpdate, FileMetadata

from ..interfaces.files_metadata_interface import IFilesMetadataRepository

class FilesMetadataRepository(implements(IFilesMetadataRepository)):
    def create(self, file_metadata: FileMetadataCreate) -> Id:
        pass

    def read(self, id: Id) -> FileMetadata:
        pass

    def update(self, id: Id, file_metadata: FileMetadataUpdate) -> None:
        pass

    def delete(self, id: Id) -> None:
        pass
