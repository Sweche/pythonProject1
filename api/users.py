from fastapi import APIRouter, Query

from servises.users import user_service

from schemas.users import User, UserUpdate, Reg

router = APIRouter()


@router.post("/user/reg", response_model=UserUpdate)
def register_user(data: Reg):
    return user_service.register(data)


@router.post("/user/auth", response_model=UserUpdate)
def auth(username: str = Query(...), password: str = Query(...)):
    return user_service.auth(username, password)
