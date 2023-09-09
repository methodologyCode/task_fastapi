from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.user import UserCreate, UserResponse
from ..Service.user import UserService
from auth.security import (get_password_hash, verify_password,
                           create_access_token, get_user_by_token)
from exceptions import UserAlreadyExistsException, CannotAddDataToDatabase

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    existing_user = await UserService.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException
    
    new_user = await UserService.add(username=user_data.username, email=user_data.email,
                                     hashed_password=get_password_hash(user_data.password))
    if not new_user:
        raise CannotAddDataToDatabase
    
    return new_user


@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserService.find_one_or_none(username=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    jwt_token = create_access_token({"sub": form_data.username})
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/about_me/", response_model=UserResponse)
async def read_user(username: str = Depends(get_user_by_token)):
    user = await UserService.find_one_or_none(username=username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user