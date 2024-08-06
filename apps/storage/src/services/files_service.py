from ..utils.app_types import Id
from ..schemas.file_metadata_schema import FileMetadataCreate, FileMetadataUpdate, FileMetadata
from ..repositories.implementations.files_metadata_sqlalchemy_repository import FilesMetadataRepository

class FilesService:
    def __init__(self, files_metadata_repository: FilesMetadataRepository = FilesMetadataRepository()):
        self.files_metadata_repository = files_metadata_repository()

    def upload(self, file_metadata: FileMetadataCreate) -> Id:
        return self.files_metadata_repository.create(file_metadata)

    def download(self, id: Id):
        raise NotImplementedError

    def read(self, id: Id) -> FileMetadata:
        return self.files_metadata_repository.read(id)

    def update(self, id: Id, file_metadata: FileMetadataUpdate) -> None:
        self.files_metadata_repository.update(id, file_metadata)

    def delete(self, id: Id) -> None:
        self.files_metadata_repository.delete(id)
