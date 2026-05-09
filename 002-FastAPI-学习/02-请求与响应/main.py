from typing import Optional

from fastapi import Cookie, FastAPI, Header, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI(title="阶段 2：请求与响应")


class UserCreate(BaseModel):
    name: str
    age: int
    email: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


users = [
    {"id": 1, "name": "张三", "age": 18, "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "age": 20, "email": "lisi@example.com"},
    {"id": 3, "name": "王五", "age": 22, "email": "wangwu@example.com"},
]


def find_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


@app.get("/")
def read_root():
    return {"message": "阶段 2：掌握接口参数"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    return user


@app.get("/users")
def list_users(
    page: int = 1,
    page_size: int = 10,
    user_agent: Optional[str] = Header(default=None),
    session_id: Optional[str] = Cookie(default=None),
):
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "page": page,
        "page_size": page_size,
        "total": len(users),
        "items": users[start:end],
        "request_info": {
            "user_agent": user_agent,
            "session_id": session_id,
        },
    }


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    new_user = {
        "id": max(item["id"] for item in users) + 1 if users else 1,
        "name": user.name,
        "age": user.age,
        "email": user.email,
    }
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    update_data = user_update.model_dump(exclude_unset=True)
    user.update(update_data)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    users.remove(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
