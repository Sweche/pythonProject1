from typing import List

from fastapi import APIRouter, Query

from servises.tests import test_service

from schemas.test import TestInfo, Test, CrQuestion1, CrQuestion2, CrTest, TestList, TestAccess, TestPlay, TestResult, \
    ListComplitedTest

router = APIRouter()


@router.post("/test/create", response_model=CrTest)
def create_test(data: TestInfo):
    return test_service.create_test(data)


@router.post("/test/create_question", response_model=CrQuestion2)
def create_question(data: CrQuestion1):
    return test_service.create_question(data)


@router.get("/test/list", response_model=List[TestList])
def test_list():
    return test_service.test_list()


@router.post("/test/access", response_model=str)
def test_access(data: TestAccess):
    return test_service.test_access(data)


@router.post("/test/play", response_model=TestResult)
def test_play(data: TestPlay):
    return test_service.test_play(data)


@router.get("/test/complited_list", response_model=List[str])
def complited_tests(id_user: str = Query(...)):
    return test_service.compl_tests(id_user)
