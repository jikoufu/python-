# Linux 学习目录

这个目录用于系统学习 Linux 操作系统，从文件系统、用户权限、进程管理、网络配置，到 Shell 脚本、性能排查和服务器运维实战，逐步具备独立管理和维护 Linux 服务器的能力。

## 目录结构

```text
004-Linux学习/
├── README.md
├── 学习路径.md
├── 01-系统基础与文件操作/
├── 02-用户与权限管理/
├── 03-进程与服务管理/
├── 04-网络与防火墙/
├── 05-Shell脚本/
├── 06-性能排查与日志/
└── 07-服务器运维实战/
```

## 学习模块

### 01-系统基础与文件操作

- Linux 发行版选择（Ubuntu / CentOS / Debian）
- 目录结构：`/etc`、`/var`、`/home`、`/opt`、`/proc` 的作用
- 文件操作：`ls`、`cd`、`cp`、`mv`、`rm`、`mkdir`
- 文件查看：`cat`、`less`、`head`、`tail`、`grep`
- 文件查找：`find`、`locate`、`which`
- 文本处理：`grep`、`sed`、`awk`、`sort`、`uniq`
- 压缩解压：`tar`、`gzip`、`zip`
- 软链接与硬链接

### 02-用户与权限管理

- 用户与用户组：`useradd`、`usermod`、`groupadd`
- 文件权限：`rwx`、`chmod`、`chown`、`chgrp`
- 特殊权限：SUID、SGID、Sticky Bit
- `sudo` 配置与最小权限原则
- SSH 密钥登录配置
- `/etc/passwd`、`/etc/shadow` 文件解读

### 03-进程与服务管理

- 进程查看：`ps`、`top`、`htop`
- 进程控制：`kill`、`pkill`、`nohup`、`&` 后台运行
- 作业管理：`jobs`、`fg`、`bg`
- systemd 服务管理：`systemctl start/stop/enable/status`
- 编写 systemd service 文件
- 定时任务：`crontab`
- 日志服务：`journalctl`

### 04-网络与防火墙

- 网络基础：IP、子网掩码、网关、DNS
- 网络工具：`ip`、`ifconfig`、`ping`、`traceroute`、`netstat`、`ss`
- 端口查看：`lsof -i`、`ss -tlnp`
- 防火墙：`ufw`（Ubuntu）、`firewalld`（CentOS）
- `iptables` 基础规则
- `curl` 和 `wget` 的使用
- SSH 隧道与端口转发

### 05-Shell脚本

- Bash 基础语法：变量、引号、特殊变量
- 条件判断：`if`、`case`
- 循环：`for`、`while`
- 函数定义与调用
- 字符串操作与数组
- 脚本调试：`set -x`、`set -e`
- 常用脚本模式：参数解析、错误处理、日志输出

### 06-性能排查与日志

- CPU 分析：`top`、`vmstat`、`mpstat`
- 内存分析：`free`、`vmstat`、`/proc/meminfo`
- 磁盘 I/O：`df`、`du`、`iostat`、`iotop`
- 网络分析：`nethogs`、`iftop`、`tcpdump`
- 日志查看：`tail -f`、`journalctl -f`
- 日志切割：`logrotate`
- 系统监控：Prometheus + Grafana 基础

### 07-服务器运维实战

- 购买和初始化云服务器（阿里云 / 腾讯云）
- 基础安全加固：禁用 root 登录、修改 SSH 端口、配置防火墙
- 部署 Python 应用：Gunicorn + systemd
- 部署 Nginx 反向代理
- 配置 HTTPS：Let's Encrypt + Certbot
- 服务器监控与告警
- 自动化运维：Ansible 基础

## 推荐学习方式

每个模块建议采用以下节奏：

1. 在本机用 WSL2 或虚拟机搭建练习环境。
2. 先理解命令的作用，再记用法。
3. 每个命令至少实际执行一次，观察输出。
4. 把常用命令整理成速查手册。
5. 最终在真实云服务器上完成部署实战。

## 练习环境推荐

| 方式 | 适合场景 |
|------|----------|
| WSL2（Windows）| 日常练习，最方便 |
| VirtualBox + Ubuntu | 需要完整 Linux 环境 |
| 云服务器（按量计费）| 网络和运维实战 |
| Docker 容器 | 快速启动隔离环境 |
