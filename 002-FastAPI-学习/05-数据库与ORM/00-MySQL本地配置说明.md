# 00 MySQL 本地配置说明

这份文件记录本机 MySQL 的安装位置、启动方式、登录方式和 FastAPI 连接配置，避免以后忘记。

## 安装信息

MySQL 版本：

```text
MySQL Community Server 8.4.8
```

MySQL 程序目录：

```text
D:\Tools\mysql-8.4.8-winx64
```

MySQL 数据目录：

```text
D:\Tools\mysql-data
```

MySQL 配置文件：

```text
D:\Tools\mysql-8.4.8-winx64\my.ini
```

启动脚本：

```text
D:\Tools\start-mysql.bat
```

停止脚本：

```text
D:\Tools\stop-mysql.bat
```

## 当前 my.ini 配置

```ini
[mysqld]
basedir=D:/Tools/mysql-8.4.8-winx64
datadir=D:/Tools/mysql-data
port=3306
character-set-server=utf8mb4
collation-server=utf8mb4_0900_ai_ci

[client]
default-character-set=utf8mb4
```

## 启动 MySQL

双击或运行：

```bash
D:\Tools\start-mysql.bat
```

也可以直接运行：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysqld.exe --defaults-file=D:\Tools\mysql-8.4.8-winx64\my.ini
```

注意：这个方式会让 MySQL 在当前窗口运行。窗口关闭后，MySQL 也会停止。

## 停止 MySQL

运行：

```bash
D:\Tools\stop-mysql.bat
```

或者：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysqladmin.exe -uroot shutdown
```

## 登录 MySQL

当前 root 用户是空密码。

登录命令：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot
```

如果后面设置了 root 密码，再使用：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot -p
```

## 检查 MySQL 是否正常

启动 MySQL 后，执行：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot -e "SELECT VERSION(), @@datadir, @@port;"
```

正常会看到：

```text
VERSION(): 8.4.8
@@datadir: D:\Tools\mysql-data\
@@port: 3306
```

## 创建学习数据库

登录 MySQL 后，可以创建一个 FastAPI 学习用数据库：

```sql
CREATE DATABASE fastapi_study DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

查看数据库：

```sql
SHOW DATABASES;
```

进入数据库：

```sql
USE fastapi_study;
```

## Python 项目依赖

当前项目虚拟环境位置：

```text
D:\PycharmProjects\python后端学习\.venv
```

已安装：

```text
SQLAlchemy 2.0.49
PyMySQL 1.1.3
```

如果以后环境丢失，可以重新安装：

```bash
D:\PycharmProjects\python后端学习\.venv\Scripts\python.exe -m pip install SQLAlchemy pymysql
```

## SQLAlchemy 连接地址

如果 root 没有密码：

```python
DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/fastapi_study?charset=utf8mb4"
```

如果 root 设置了密码，例如密码是 `123456`：

```python
DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fastapi_study?charset=utf8mb4"
```

## FastAPI 中常见配置写法

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/fastapi_study?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## 常见问题

### 1. mysql 命令找不到

如果直接输入：

```bash
mysql -uroot
```

提示找不到命令，是因为 MySQL 没有配置到系统环境变量。

可以使用完整路径：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot
```

### 2. 连接失败

先确认 MySQL 是否启动。

可以执行：

```bash
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot -e "SELECT 1;"
```

如果无法连接，先运行：

```bash
D:\Tools\start-mysql.bat
```

### 3. 端口冲突

当前 MySQL 使用端口：

```text
3306
```

如果以后提示端口被占用，可以修改：

```text
D:\Tools\mysql-8.4.8-winx64\my.ini
```

把：

```ini
port=3306
```

改成其他端口，例如：

```ini
port=3307
```

对应的 SQLAlchemy 连接地址也要改端口。

## 学习建议

学习 FastAPI + SQLAlchemy 时，建议先按这个顺序：

1. 启动 MySQL。
2. 创建 `fastapi_study` 数据库。
3. 用 SQLAlchemy 连接数据库。
4. 创建 ORM 模型。
5. 实现增删改查。
6. 再学习 Alembic 数据库迁移。
