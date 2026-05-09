from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("应用启动：初始化资源")
    app.state.started_at = datetime.now()
    app.state.fake_db_pool = {
        "name": "fake mysql pool",
        "status": "connected",
    }

    yield

    print("应用关闭：释放资源")
    app.state.fake_db_pool["status"] = "closed"


app = FastAPI(title="阶段 4：lifespan 生命周期", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "lifespan 生命周期示例"}


@app.get("/status")
def get_status(request: Request):
    return {
        "started_at": request.app.state.started_at,
        "db_pool": request.app.state.fake_db_pool,
    }
