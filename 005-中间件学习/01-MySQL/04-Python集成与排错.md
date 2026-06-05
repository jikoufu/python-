# Python 集成 MySQL 与排错

## 1. 依赖

你之前已经在项目虚拟环境里安装过：

```text
SQLAlchemy
PyMySQL
```

如果以后重新安装：

```powershell
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m pip install sqlalchemy pymysql
```

异步 MySQL 可以安装：

```powershell
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m pip install aiomysql
```

## 2. 同步连接示例

```python
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:@127.0.0.1:3306/fastapi_study?charset=utf8mb4",
    echo=True,
    pool_pre_ping=True,
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT VERSION()"))
    print(result.scalar())
```

说明：

- `root:` 后面没有密码，表示当前本机 root 是空密码。
- 如果你设置了密码，例如 `root123456`，连接串改成 `root:root123456@127.0.0.1`。
- `pool_pre_ping=True` 可以在连接池里自动检查连接是否可用。

## 3. FastAPI + SQLAlchemy 基础结构

推荐把数据库连接拆成单独文件，例如：

```text
app/
├── database.py
├── models.py
├── schemas.py
└── main.py
```

`database.py`：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/fastapi_study?charset=utf8mb4"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`models.py`：

```python
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1)
```

`main.py`：

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.get(User, user_id)
```

## 4. 连接池必须知道

后端服务不会每次请求都重新创建数据库连接，而是使用连接池。

常见参数：

| 参数 | 说明 |
|------|------|
| `pool_size` | 常驻连接数 |
| `max_overflow` | 连接不够时允许额外创建的连接数 |
| `pool_timeout` | 获取连接的最大等待时间 |
| `pool_recycle` | 连接回收时间 |
| `pool_pre_ping` | 使用前检查连接是否可用 |

示例：

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
```

## 5. 常见问题

### 5.1 连接超时

排查顺序：

1. MySQL 是否启动。
2. 端口 `3306` 是否监听。
3. 用户名和密码是否正确。
4. 数据库名是否存在。
5. 防火墙或网络是否阻断。

### 5.2 连接池耗尽

现象：

```text
QueuePool limit reached
```

常见原因：

- 请求结束后没有关闭 session。
- 慢 SQL 太多，连接长期占用。
- 并发量超过连接池配置。

解决：

- 使用 FastAPI `Depends(get_db)` 管理 session 生命周期。
- 排查慢 SQL。
- 合理调整连接池大小。

### 5.3 中文乱码

连接串加：

```text
?charset=utf8mb4
```

建库建表也使用：

```sql
default charset=utf8mb4
```

### 5.4 Too many connections

说明 MySQL 连接数被打满。

排查：

```sql
show variables like 'max_connections';
show PROCESSLIST;
```

处理：

- 检查应用是否泄漏连接。
- 检查连接池是否配置过大。
- 分析是否有慢 SQL 长时间占用连接。

## 6. 测开岗位怎么理解 MySQL

测试开发不一定每天写复杂 SQL，但必须能：

- 准备测试数据。
- 校验接口落库结果。
- 排查接口异常是不是数据库问题。
- 分析慢接口是否由慢 SQL 导致。
- 理解事务导致的数据一致性问题。
- 做自动化测试前后清理数据。

