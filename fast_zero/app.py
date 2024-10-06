from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException

from fast_zero.helpers.database import get_session
from fast_zero.helpers.validations.user import email_existis
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublicSchema, UserSchema

app = FastAPI()
database = []  # Placeholder para os dados de usuários


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Olá Mundo!!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session=Depends(get_session)):
    if email_existis(user.email, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="EMAIL ALREADY EXISTS"
        )

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(path="/users/", response_model=UserList)
def read_users():
    return {"users": database}


@app.get("/users/{user_id}", response_model=UserPublicSchema)
def read_user(user_id: UUID):
    # Implementar a lógica de leitura de um usuário específico
    for db_user in database:
        if db_user.id == user_id:
            return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="NOT FOUND")


@app.put("/users/{user_id}", response_model=UserPublicSchema)
def update_user(user_id: UUID, user: UserSchema):
    # Implementar a lógica de atualização do usuário
    for db_user in database:
        if db_user.id == user_id:
            user_dump = user.model_dump()
            for user_field in user_dump.keys():
                setattr(db_user, user_field, user_dump[user_field])
            return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="NOT FOUND")


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: UUID):
    # Implementar a lógica de exclusão do usuário
    for db_user in database:
        if db_user.id == user_id:
            database.remove(db_user)
            return {"message": "User deleted successfully"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="NOT FOUND")
