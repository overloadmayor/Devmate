---
name: create-python-project
description: 创建 Python 项目的基础结构和配置文件，包括 src/、tests/、docs/ 等目录
---

# Create Python Project

当用户要求创建 Python 项目时，请按照以下步骤操作：

## 项目结构
- 创建 `src/` 目录存放源代码
- 创建 `tests/` 目录存放测试代码
- 创建 `docs/` 目录存放文档
- 创建 `.gitignore` 文件

## 配置文件
- 创建 `pyproject.toml` 管理项目配置和依赖
- 创建 `README.md` 提供项目说明
- 创建 `.env.example` 作为环境变量模板

## 基础代码
- 在 `src/` 目录下创建主模块
- 在 `tests/` 目录下创建基础测试文件
- 添加 `__init__.py` 文件使目录成为 Python 包

## 依赖管理
- 在 `pyproject.toml` 中配置项目依赖
- 包含开发依赖：`pytest`, `black`, `flake8`, `mypy`

## 示例代码
```toml
# filename: pyproject.toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "black>=24.0.0", "flake8>=7.0.0", "mypy>=1.8.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```python
# filename: src/main.py
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

## Guidelines
- 确保生成的代码符合 PEP 8 规范
- 使用类型提示
- 添加适当的文档字符串
- 包含基本的错误处理
