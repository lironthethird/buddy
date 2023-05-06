from fastapi import FastAPI, Body
from pydantic import BaseModel

class Question(BaseModel):
    q: str
    value: int
from typing import Annotated
from fastapi import Body

"""
/api
    /<subject>
        /validate
            /question
                /<name>
            /test
                /<name>
        /check
            /teacher
"""
app = FastAPI()

@app.post("/api/math/validate/question/positive")
def validate_positive(q: Annotated[Question, Body(embed=True)], bruh: Annotated[int, Body()]):
    assert q.value > 0, "Question value must be positive"

@app.post("/api/math/validate/question/length")
def validate_question_length(q: Question, max_length: Annotated[int, Body(embed=True)] = 10):
    assert len(q.q) < max_length, "Question is too long"


@app.post("/api/math/validate/test/length")
def validate_test_length(test: Annotated[list[Question], Body(embed=True)]):
    assert len(test) < 10, "Test is too long"

@app.post("/api/math/validate/test/grade")
def validate_grade(test: list[Question], max_grade: Annotated[int, Body(embed=True)] = 100):
    assert sum(q.value for q in test) == max_grade

@app.post("/api/math/check/teacher")
def teacher_check(test: list[Question], teacher_name: Annotated[str, Body()], teacher_id: Annotated[str, Body()]):
    raise NotImplemented

