import time
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from pydantic import BaseModel

app = FastAPI(title="阶段 4：依赖注入")


class User(BaseModel):
    id: int
    username: str
    role: str


class Article(BaseModel):
    id: int
    title: str
    content: str
    author_id: int


class PageParams(BaseModel):
    page: int
    page_size: int


users = [
    {"id": 1, "username": "zhangsan", "role": "user", "token": "user-token"},
    {"id": 2, "username": "admin", "role": "admin", "token": "admin-token"},
]

articles = [
    {"id": 1, "title": "FastAPI 入门", "content": "第一个 FastAPI 接口", "author_id": 1},
    {"id": 2, "title": "Depends 基础", "content": "学习依赖注入", "author_id": 2},
    {"id": 3, "title": "Pydantic 校验", "content": "请求模型和响应模型", "author_id": 1},
]


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("1. 进入耗时统计中间件")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    response.headers["X-Learning-Stage"] = "depends-and-middleware"
    print("4. 离开耗时统计中间件")
    print(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} time={process_time:.6f}s"
    )
    return response


@app.middleware("http")
async def show_middleware_order(request: Request, call_next):
    print("0. 进入顺序演示中间件")
    response = await call_next(request)
    response.headers["X-Middleware-Order"] = (
        "show_middleware_order -> add_process_time_header -> endpoint"
    )
    print("5. 离开顺序演示中间件")
    return response


def get_db():
    return {
        "users": users,
        "articles": articles,
    }


def get_page_params(
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=50, description="每页数量")] = 10,
):
    return PageParams(page=page, page_size=page_size)


def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
    db: dict = Depends(get_db),
):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少 Authorization 请求头",
        )

    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization 格式应为 Bearer token",
        )

    token = authorization.removeprefix(prefix)
    for user in db["users"]:
        if user["token"] == token:
            return User(id=user["id"], username=user["username"], role=user["role"])

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效 token",
    )


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )
    return current_user


@app.get("/")
def read_root():
    return {"message": "阶段 4：掌握依赖注入"}


@app.get("/articles")
def list_articles(
    page_params: PageParams = Depends(get_page_params),
    db: dict = Depends(get_db),
):
    start = (page_params.page - 1) * page_params.page_size
    end = start + page_params.page_size

    return {
        "page": page_params.page,
        "page_size": page_params.page_size,
        "total": len(db["articles"]),
        "items": db["articles"][start:end],
    }


@app.get("/users/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/articles/mine")
def list_my_articles(
    current_user: User = Depends(get_current_user),
    db: dict = Depends(get_db),
):
    return [
        article
        for article in db["articles"]
        if article["author_id"] == current_user.id
    ]


@app.get("/admin/users")
def list_all_users(
    admin_user: User = Depends(require_admin),
    db: dict = Depends(get_db),
):
    return {
        "operator": admin_user.username,
        "items": [
            {"id": user["id"], "username": user["username"], "role": user["role"]}
            for user in db["users"]
        ],
    }
