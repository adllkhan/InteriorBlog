from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from . import schemas, utils
from config import ALG, KEY, ACCESS_TOKEN_EXPIRE_MINUTES, USERNAME, PASSWORD

auth_admin = schemas.Admin(username=USERNAME, hashed_password=utils.encode(PASSWORD))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")

router = APIRouter()

def authenticate_user(username: str, password: str):
    if not username == auth_admin.username:
        return False
    if not utils.verify(password, auth_admin.hashed_password):
        return False
    return auth_admin


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALG)
    return encoded_jwt

@router.post("/", response_model=schemas.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    admin = authenticate_user(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=schemas.Admin)
async def admin(current: Annotated[schemas.Admin, Depends()]):
    return current
