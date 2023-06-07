import json
from typing import List

from fastapi import HTTPException
from sqlalchemy import create_engine, Column, String, Integer, update, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from schemas.users import User, UserUpdate

Base = declarative_base()


class TableUser(Base):
    __tablename__ = "users"
    id = Column("id", String, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)
    complited_tests = Column("complited_tests", JSON)


engine = create_engine("sqlite:///db/users.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def user_to_table_user(user: User) -> TableUser:
    return TableUser(
        id=user.id,
        username=user.username,
        password=user.password,
        complited_tests=json.dumps(user.complited_tests)
    )


def add_user(user: User) -> UserUpdate:
    us = session.query(TableUser).filter_by(username=user.username).first()
    if not us:
        table_user = user_to_table_user(user)
        session.add(table_user)
        session.commit()
        x = UserUpdate(
            id=user.id,
            username=user.username
        )
        return x
    raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует.")


def auth_user(username, password) -> UserUpdate:
    user_from_db = session.query(TableUser).filter_by(username=username).first()
    if user_from_db and user_from_db.password == password:
        return UserUpdate(
            id=user_from_db.id,
            username=user_from_db.username
        )
    raise HTTPException(status_code=400, detail="Неверный логин или пароль")


def compl_test(id_test: str, id_user: str):
    user = session.query(TableUser).filter_by(id=id_user).first()
    test = json.loads(user.complited_tests)
    test.append(id_test)
    testjs = json.dumps(test)
    user.complited_tests = testjs
    session.commit()


def test_id_list(id_user: str) -> JSON:
    user = session.query(TableUser).filter_by(id=id_user).first()
    return user.complited_tests
