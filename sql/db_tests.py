from typing import List

from fastapi import HTTPException
import json
from sqlalchemy import create_engine, Column, String, Boolean, ForeignKey, Integer, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from schemas import test
from schemas.test import Test, TestInfo, Question, CrQuestion1, CrQuestion2, CrTest, TestList, TestAccess, TestPlay, \
    TestResult, Question1, ListComplitedTest

Base = declarative_base()


class TableQuestions(Base):
    __tablename__ = "questions"
    id = Column("id", String, primary_key=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    question = Column("question", String)
    right_answer = Column("right_answer", Boolean)
    passed_all = Column("passed_all", Integer)
    passed_true = Column("passed_true", Integer)


class TableTest(Base):
    __tablename__ = "tests"
    id = Column("id", String, primary_key=True)
    id_user = Column("id_user", String)
    username = Column("username", String)
    test_name = Column("test_name", String)
    access = Column("access", Boolean)
    describe = Column("describe", String)
    answers_true = Column("answers_true", String)
    answers_all = Column("answers_all", String)
    questions = relationship("TableQuestions")


engine = create_engine("sqlite:///db/tests.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def test_to_table_test(test: Test) -> TableTest:
    return TableTest(
        id=test.id,
        username=test.username,
        id_user=test.id_user,
        test_name=test.test_name,
        describe=test.describe,
        access=test.access,
        answers_true=test.answers_true,
        answers_all=test.answers_all,
        questions=[]
    )


def table_to_test(test: TableTest) -> TestList:
    return TestList(
        id=test.id,
        username=test.username,
        id_user=test.id_user,
        test=test.test_name,
        describe=test.describe
    )


def add_test(test: Test) -> CrTest:
    table_test = test_to_table_test(test)
    session.add(table_test)
    session.commit()
    x = CrTest(
        test_name=test.test_name,
        username=test.username,
        id=test.id,
        id_user=test.id_user,
        access=test.access,
        describe=test.describe,
        answers_true=test.answers_true,
        answers_all=test.answers_all
    )
    return x


def question_to_table_question(question: CrQuestion2) -> TableQuestions:
    return TableQuestions(
        id=question.id,
        test_id=question.idTest,
        question=question.question,
        right_answer=question.right_answer,
        passed_all=question.passed_all,
        passed_true=question.passed_true
    )


def table_to_question(question: TableQuestions) -> Question:
    return Question(
        id=question.id,
        right_answer=question.right_answer,
        passed_all=question.passed_all,
        passed_true=question.passed_true
    )


def add_question(question: CrQuestion2) -> CrQuestion2:
    test = session.query(TableTest).filter_by(id=question.idTest).first()
    if test.id_user == question.id_user:
        table_question = question_to_table_question(question)
        session.add(table_question)
        session.commit()
    return question


def get_tests() -> List[TestList]:
    list_test = session.query(TableTest).filter_by(access=1).all()
    list_test_mas = []
    for item in list_test:
        list_test_mas.append(table_to_test(item))
    return list_test_mas


def change_access(payload: TestAccess) -> str:
    test = session.query(TableTest).filter_by(id=payload.idTest).first()
    if test.id_user == payload.id_user:
        access = payload.access
        temp = update(TableTest).where(TableTest.id == payload.idTest).values(access=access)
        session.execute(temp)
        session.commit()
        return "successful"
    raise HTTPException(status_code=400, detail="Вы не владелец теста")


def test_play(payload: TestPlay) -> TestResult:
    count_right_answer = 0

    test = session.query(TableTest).filter_by(id=payload.idTest).first()

    for question in payload.questions:
        question_from_table = session.query(TableQuestions).filter_by(id=question.id).first()
        question_from_table_py = Question.from_orm(question_from_table)
        question_from_table_py.passed_all += 1

        temp1 = update(TableQuestions).where(TableQuestions.id == question.id).values(
            passed_all=question_from_table_py.passed_all)
        session.execute(temp1)
        session.commit()

        test_answer = Test.from_orm(test)
        test_answer.answers_all += 1

        temp4 = update(TableTest).where(TableTest.id == test.id).values(answers_all=test_answer.answers_all)
        session.execute(temp4)
        session.commit()

        if question.right_answer == question_from_table_py.right_answer:
            count_right_answer += 1
            question_from_table_py.passed_true += 1

            temp2 = update(TableQuestions).where(TableQuestions.id == question.id).values(
                passed_true=question_from_table_py.passed_true)
            session.execute(temp2)
            session.commit()

            test_answer.answers_true += 1
            temp5 = update(TableTest).where(TableTest.id == test.id).values(answers_true=test_answer.answers_true)
            session.execute(temp5)
            session.commit()

    procent_right_answer = (count_right_answer / len(payload.questions) * 100).__str__()
    str_res = str(procent_right_answer + "%")

    result = TestResult(
        test=test,
        result=str_res
    )

    return result


def comlited_tests(id_tests: str) -> List[str]:
    test = session.query(TableTest).filter_by(id=id_tests).first()
    tests = Test.from_orm(test)

    return tests
