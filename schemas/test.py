from typing import List

import pydantic


class Question1(pydantic.BaseModel):
    id: str
    right_answer: bool

    class Config:
        orm_mode = True


class Question(pydantic.BaseModel):
    id: str
    right_answer: bool
    passed_all: int
    passed_true: int

    class Config:
        orm_mode = True


class CrQuestion1(pydantic.BaseModel):
    id_user: str
    idTest: str
    question: str
    right_answer: bool


class CrQuestion2(pydantic.BaseModel):
    id: str
    idTest: str
    id_user: str
    question: str
    right_answer: bool
    passed_all: int
    passed_true: int


class CrQuestion3(pydantic.BaseModel):
    question2: CrQuestion2
    passed_all: str
    passed_true: str


class Test(pydantic.BaseModel):
    test_name: str
    username: str
    id_user: str
    id: str
    describe: str
    access: bool
    answers_true: int
    answers_all: int
    questions: List[Question]

    class Config:
        orm_mode = True


class TestResult(pydantic.BaseModel):
    test: Test
    result: str

    class Config:
        orm_mode = True


class CrTest(pydantic.BaseModel):
    test_name: str
    username: str
    id_user: str
    id: str
    access: bool
    answers_true: int
    answers_all: int
    describe: str


class TestInfo(pydantic.BaseModel):
    test_name: str
    username: str
    id_user: str
    describe: str


class TestList(pydantic.BaseModel):
    id: str
    id_user: str
    username: str
    test: str
    describe: str


class TestAccess(pydantic.BaseModel):
    idTest: str
    id_user: str
    access: bool


class TestPlay(pydantic.BaseModel):
    idTest: str
    id_user: str
    questions: List[Question1]

    class Config:
        orm_mode = True


class ListComplitedTest(pydantic.BaseModel):
    id_test_list: List[str]
