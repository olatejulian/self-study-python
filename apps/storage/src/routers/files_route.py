from fastapi import APIRouter

from ..utils.app_types import Id
from ..services.files_service import FilesService
from ..schemas.file_metadata_schema import FileSavedInfo, FileMetadataCreate, FileMetadataUpdate

router = APIRouter(prefix='/files', tags=['Files'])
service = FilesService()

router.post('/upload')
def upload(file_metadata: FileMetadataCreate) -> FileSavedInfo:
    return service.upload(file_metadata)

router.get('/download/id/{id}')
def download(id: Id):
    return service.download(id)

router.get('/id/{id}')
def read(id: Id) -> FileSavedInfo:
    return service.read(id)

router.patch('/id/{id}')
def update(id: Id, file_metadata: FileMetadataUpdate) -> None:
    service.update(id, file_metadata)

router.delete('/id/{id}')
def delete(id: Id) -> None:
    service.delete(id)
