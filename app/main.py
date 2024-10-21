from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import database

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'this is root'}


@app.get('/users/{id}')
async def get_user_by_id(id: int, session: AsyncSession = Depends(database.get_session)):
    user = await database.get_user_by_id_db(session, id)
    return user.email
