from fastapi import APIRouter, Depends

from ..utils.app_types import Id
from ..utils.pagination import Pagination
from ..services.users_service import UserService
from ..schemas.user_schema import UserCreate, UserUpdate, User

router = APIRouter(prefix='/users', tags=['User Routes'])

service = UserService()

@router.post('/')
async def create_user(user: UserCreate) -> int:
    return service.create(user)

@router.get('/id/{id}', response_model=User)
async def read_user(id: Id) -> User:
    return service.read(id)

@router.patch('/id/{id}')
async def update_user(id: Id, user: UserUpdate) -> None:
    service.update(id, user)

@router.delete('/id/{id}')
async def delete_user(id: Id) -> None:
    service.delete(id)

@router.get('/')
async def read_many(body: Pagination = Depends(Pagination)) -> list[User]:
    return service.read_many(body)

@router.get('/count')
async def count() -> int:
    return service.count()
