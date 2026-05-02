# 头条新闻后端 (Toutiao Backend)

基于 FastAPI 的新闻资讯平台后端服务，提供用户认证、新闻浏览、收藏、浏览历史等功能。

## 技术栈

- **Web 框架**: FastAPI
- **ORM**: SQLAlchemy (异步)
- **数据库**: MySQL
- **缓存**: Redis
- **认证**: Token 认证

## 项目结构

```
toutiao_backend/
├── main.py                  # 应用入口、中间件、路由注册
├── configs/                 # 配置模块
│   ├── db_conf.py           # 数据库连接（异步引擎、会话工厂）
│   ├── cache_conf.py        # Redis 连接与缓存操作
│   └── news_cache.py        # 新闻数据缓存策略
├── models/                  # 数据库模型 (SQLAlchemy ORM)
│   ├── users.py             # 用户模型
│   ├── news.py              # 新闻、分类模型
│   ├── favorite.py          # 收藏模型
│   └── history.py           # 浏览历史模型
├── schemas/                 # Pydantic 请求/响应模型
│   ├── users.py
│   ├── favorite.py
│   ├── history.py
│   └── base.py
├── crud/                    # 数据访问层
│   ├── users.py             # 用户 CRUD
│   ├── news.py              # 新闻 CRUD
│   ├── news_cache.py        # 新闻缓存 CRUD
│   ├── favority.py          # 收藏 CRUD
│   └── history.py           # 浏览历史 CRUD
├── routers/                 # 路由处理
│   ├── users.py             # /api/users/*
│   ├── news.py              # /api/news/*
│   ├── favorite.py          # /api/favorite/*
│   └── history.py           # /api/history/*
└── utils/                   # 工具模块
    ├── auth.py              # Token 鉴权依赖
    ├── security.py          # 密码加密
    ├── response.py          # 统一响应格式
    ├── exception.py         # 自定义异常
    └── exception_handlers.py # 全局异常处理
```

## API 接口

### 用户 `/api/users`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/register` | 用户注册 |
| POST | `/login` | 用户登录 |
| GET | `/me` | 获取当前用户信息 |
| PUT | `/update` | 更新用户信息 |
| PUT | `/change-password` | 修改密码 |

### 新闻 `/api/news`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/categories` | 获取新闻分类列表 |
| GET | `/list` | 分页获取新闻列表（按分类） |
| GET | `/detail/{news_id}` | 获取新闻详情（含浏览量+1） |
| GET | `/related` | 获取相关新闻（排除当前） |

### 收藏 `/api/favorite`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/check` | 检查新闻是否已收藏 |
| POST | `/add` | 添加收藏 |
| DELETE | `/remove` | 移除单条收藏 |
| GET | `/list` | 分页获取收藏列表 |
| DELETE | `/clear` | 清空所有收藏 |

### 浏览历史 `/api/history`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/check` | 检查是否有浏览记录 |
| POST | `/add` | 添加浏览记录 |
| DELETE | `/remove` | 删除单条记录 |
| GET | `/list` | 分页获取浏览历史 |
| DELETE | `/remove_all` | 清空所有历史 |

## 快速开始

### 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 6.0+

### 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy aiomysql redis pydantic
```

### 数据库配置

在 `configs/db_conf.py` 中修改数据库连接信息：

```python
ASYNC_DATABASE_URL = "mysql+aiomysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4"
```

在 `configs/cache_conf.py` 中修改 Redis 连接信息：

```python
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
```

### 创建数据库表

```python
# 在 Python 交互环境中执行
from models.users import Base as UserBase
from models.news import Base as NewsBase
from models.favorite import Base as FavoriteBase
from models.history import Base as HistoryBase
from configs.db_conf import engine

# 创建所有表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(NewsBase.metadata.create_all)
        await conn.run_sync(FavoriteBase.metadata.create_all)
        await conn.run_sync(HistoryBase.metadata.create_all)
```

### 启动服务

```bash
python main.py
# 或
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

启动后访问 http://127.0.0.1:8000/docs 查看 Swagger API 文档。
