from fastapi import APIRouter


router = APIRouter()

@router.post('/users')
async def create_user():
    pass


@router.get('/users/{id}')
async def get_user_by_id(id: int):
    pass
