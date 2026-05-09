from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

app = FastAPI(title="阶段 3：Pydantic 数据校验")


class Address(BaseModel):
    province: str = Field(..., min_length=2, max_length=20, examples=["广东省"])
    city: str = Field(..., min_length=2, max_length=20, examples=["深圳市"])
    detail: str = Field(..., min_length=5, max_length=100, examples=["南山区科技园 1 号"])


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, examples=["zhangsan"])
    password: str = Field(..., min_length=6, max_length=30, examples=["123456"])
    age: int = Field(..., ge=1, le=120, examples=[18])
    email: EmailStr = Field(..., examples=["zhangsan@example.com"])
    address: Optional[Address] = None

    @field_validator("username")
    @classmethod
    def username_must_not_contain_space(cls, value: str):
        if " " in value:
            raise ValueError("用户名不能包含空格")
        return value

    @field_validator("password")
    @classmethod
    def password_must_contain_number(cls, value: str):
        if not any(char.isdigit() for char in value):
            raise ValueError("密码至少需要包含一个数字")
        return value


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=20)
    age: Optional[int] = Field(default=None, ge=1, le=120)
    email: Optional[EmailStr] = None
    address: Optional[Address] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    age: int
    email: EmailStr
    address: Optional[Address] = None


users = [
    {
        "id": 1,
        "username": "zhangsan",
        "password": "abc123",
        "age": 18,
        "email": "zhangsan@example.com",
        "address": {
            "province": "广东省",
            "city": "深圳市",
            "detail": "南山区科技园 1 号",
        },
    }
]


def find_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def to_user_response(user: dict):
    public_user = user.copy()
    public_user.pop("password", None)
    return public_user


@app.get("/")
def read_root():
    return {"message": "阶段 3：Pydantic 数据校验"}


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate):
    new_user = user.model_dump()
    new_user["id"] = max(item["id"] for item in users) + 1 if users else 1
    users.append(new_user)
    return to_user_response(new_user)


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return to_user_response(user)


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    update_data = user_update.model_dump(exclude_unset=True)
    user.update(update_data)
    return to_user_response(user)
