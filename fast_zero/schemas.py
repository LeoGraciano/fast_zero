from uuid import UUID

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublicSchema(BaseModel):
    id: UUID
    email: EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: UUID
    email: EmailStr
    password: str


class UserList(BaseModel):
    users: list[UserPublicSchema]
