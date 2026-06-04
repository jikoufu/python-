# MySQL 安装配置与本机信息

## 1. 本机安装位置

当前你的 MySQL 已按“放在 D 盘”的方式整理，信息如下：

| 项目 | 路径 / 配置 |
|------|-------------|
| MySQL 程序目录 | `D:\Tools\mysql-8.4.8-winx64` |
| MySQL 数据目录 | `D:\Tools\mysql-data` |
| 启动脚本 | `D:\Tools\start-mysql.bat` |
| 停止脚本 | `D:\Tools\stop-mysql.bat` |
| 默认端口 | `3306` |
| 默认用户 | `root` |
| 当前 root 密码 | 空密码 |

注意：空密码只适合本地学习。以后做真实项目或连接公网环境时，必须设置强密码。

## 2. 启动和停止

在 PowerShell 或文件管理器中执行：

```powershell
D:\Tools\start-mysql.bat
```

停止：

```powershell
D:\Tools\stop-mysql.bat
```

如果启动失败，优先检查：

```powershell
netstat -ano | findstr :3306
```

如果 3306 已被占用，说明可能已经有一个 MySQL 或 MariaDB 在运行。

## 3. 连接 MySQL

进入 MySQL 客户端：

```powershell
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot
```

查看版本：

```sql
SELECT VERSION();
```

查看数据库：

```sql
SHOW DATABASES;
```

## 4. 创建学习数据库

```sql
CREATE DATABASE fastapi_study DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE fastapi_study;
```

`utf8mb4` 可以存中文和 emoji，是现在更推荐的字符集。

## 5. 设置 root 密码

如果后续想设置密码，例如 `root123456`：

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root123456';
FLUSH PRIVILEGES;
```

设置后连接方式变为：

```powershell
D:\Tools\mysql-8.4.8-winx64\bin\mysql.exe -uroot -proot123456
```

## 6. 常用排错

### 6.1 连接不上 MySQL

先确认进程是否存在：

```powershell
Get-Process | Where-Object { $_.ProcessName -like "*mysql*" }
```

再确认端口是否监听：

```powershell
netstat -ano | findstr :3306
```

### 6.2 Access denied

常见原因：

- 用户名错。
- 密码错。
- root 只允许 localhost 登录。
- 设置过密码后还按空密码连接。

### 6.3 Unknown database

说明数据库还没有创建。先执行：

```sql
CREATE DATABASE fastapi_study DEFAULT CHARACTER SET utf8mb4;
```

