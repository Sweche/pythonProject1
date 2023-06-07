from __future__ import annotations

import json
from typing import List

import sql.db_tests as db
import sql.db_users as db_us
from schemas.test import TestInfo, CrQuestion1, CrQuestion2, CrTest, TestList, TestAccess, TestPlay, TestResult, \
    ListComplitedTest

import uuid


class TestService:

    def create_test(self, payload: TestInfo) -> CrTest:
        id = uuid.uuid4().__str__()
        test = CrTest(
            test_name=payload.test_name,
            username=payload.username,
            id=id,
            id_user=payload.id_user,
            access=True,
            describe=payload.describe,
            answers_true=0,
            answers_all=0
        )
        return db.add_test(test)

    def create_question(self, payload: CrQuestion1) -> CrQuestion2:
        id = uuid.uuid4().__str__()
        question = CrQuestion2(
            id=id,
            idTest=payload.idTest,
            id_user=payload.id_user,
            question=payload.question,
            right_answer=payload.right_answer,
            passed_all=0,
            passed_true=0,
        )
        return db.add_question(question)

    def test_access(self, payload: TestAccess) -> str:
        return db.change_access(payload)

    def test_list(self):
        return db.get_tests()

    def test_play(self, payload: TestPlay) -> TestResult:
        res = db.test_play(payload)
        if res.result == "100.0%":
            db_us.compl_test(payload.idTest, payload.id_user)
        return res

    def compl_tests(self, id_user) -> List[str]:
        id_tests1 = db_us.test_id_list(id_user)
        id_tests = json.loads(id_tests1)
        tests = db.comlited_tests(id_tests)
        return tests


test_service: TestService = TestService()
