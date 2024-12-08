from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users():
    return users


@app.post('/user/{username}/{age}')
async def post_user(username: str = Path(min_length=5, max_length=20, description='Enter username',
                                         example='UrbanUser'),
                    age: int = Path(ge=18, le=120, description='Enter age', example='24')):
    user_id = max((us.id for us in users), default=0) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int = Path(ge=0, description='Enter user_id', example='15'),
                      username: str = Path(min_length=5, max_length=20, description='Enter username',
                                           example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description='Enter age', example='24')):
    for us in users:
        if us.id == user_id:
            us.username = username
            us.age = age
            user = us
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def deleted_user(user_id: int = Path(ge=0, description='Enter user_id', example='15')):
    for us in users:
        if us.id == user_id:
            del_user = us
            users.pop(user_id - 1)
            return del_user
    raise HTTPException(status_code=404, detail='User was not found')
