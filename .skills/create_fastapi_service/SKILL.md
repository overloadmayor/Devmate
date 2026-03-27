---
name: create-fastapi-service
description: 创建 FastAPI 服务的基础结构和文件，包括 main.py、requirements.txt 等必要文件
---

# Create FastAPI Service

当用户要求创建 FastAPI 服务时，请按照以下步骤操作：

## 项目结构
- 创建 `main.py` 作为应用入口文件
- 创建 `requirements.txt` 或 `pyproject.toml` 管理依赖
- 创建 `app/` 目录存放应用代码
- 创建 `app/__init__.py` 和 `app/main.py`

## 基础代码
- 在 `main.py` 中创建 FastAPI 实例
- 定义基本的路由和端点
- 添加 CORS 中间件（如果需要）
- 添加健康检查端点

## 依赖管理
- 在 `requirements.txt` 中包含 `fastapi`, `uvicorn[standard]`
- 或者使用 `pyproject.toml` 配置项目

## 运行说明
- 提供启动命令：`uvicorn main:app --reload`
- 说明如何访问 API 文档：`http://localhost:8000/docs`

## 示例代码
```python
# filename: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Guidelines
- 确保生成的代码符合 FastAPI 最佳实践
- 使用类型提示
- 添加适当的错误处理
- 包含基本的文档字符串
