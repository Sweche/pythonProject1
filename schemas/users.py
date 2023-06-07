from typing import List

import pydantic


class User(pydantic.BaseModel):
    id: str
    username: str
    password: str
    complited_tests: List[str]


class UserUpdate(pydantic.BaseModel):
    username: str
    id: str


class Reg(pydantic.BaseModel):
    username: str
    password: str
    password1: str
