from __future__ import annotations

from fastapi import HTTPException

import sql.db_users as db
from schemas.users import User, UserUpdate, Reg

import uuid


class UserService:

    def register(self, payload: Reg) -> UserUpdate:
        if payload.password == payload.password1:
            id = uuid.uuid4().__str__()
            user = User(
                id=id,
                username=payload.username,
                password=payload.password,
                complited_tests=[]
            )
            return db.add_user(user)
        raise HTTPException(status_code=400, detail="Пароли не совпадают.")

    def auth(self, username, password) -> UserUpdate:
        return db.auth_user(username, password)


user_service: UserService = UserService()
