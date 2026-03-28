# DevMate - AI 编程助手

DevMate 是一个由 LangChain 和 LangGraph 驱动的智能 AI 编程助手，能够帮助开发者完成各种编程任务，包括代码生成、文件操作、技能管理等。

## 功能特性

### 🤖 核心能力

- **文件操作**：使用 LangChain 官方工具进行文件读取、写入、列表查看和删除
- **技能系统**：动态加载和使用专业技能（如创建 FastAPI 服务、Python 项目等）
- **短期记忆**：基于 InMemorySaver 的对话历史记忆，保持多轮对话的连贯性
- **网络搜索**：通过 Tavily Search 获取最新的技术信息和最佳实践
- **知识库检索**：搜索本地文档和知识库
- **工具调用**：自动调用适当的工具完成复杂任务

### 🛠️ 技术架构

- **框架**：LangChain 1.2.x + LangGraph
- **记忆系统**：InMemorySaver（内存检查点存储）
- **消息处理**：ChatPromptTemplate + 消息占位符
- **文件工具**：LangChain Community 官方文件操作工具
- **搜索集成**：Tavily Search API

## 安装

### 环境要求

- Python 3.13+
- uv 包管理器
- Docker 

### 安装步骤

1. **克隆项目**
   ```bash
   cd d:\DevMate
   ```

2. **安装依赖**
   ```bash
   uv sync
   ```

3. **配置环境变量**
   创建 `.env` 文件：
   ```bash
   notepad .env
   ```
   添加以下内容：
   ```env
   # LLM 配置（必须）
   MODEL_API_KEY=your_model_api_key_here

   # Embedding 配置（必须）
   EMBEDDING_API_KEY=your_embedding_api_key_here

   # Tavily 搜索 API（必须，否则搜索功能不可用）
   TAVILY_API_KEY=your_tavily_api_key_here

   # LangSmith 配置（可选）
   LANGCHAIN_API_KEY=your_langchain_api_key_here
   ```

## 使用方法

### 方式一：本地运行

#### 步骤 1：启动 MCP Server

在第一个终端窗口中运行：

```powershell
$env:PYTHONPATH='d:\DevMate\src'; uv run python -m devmate.mcp.server
```

#### 步骤 2：启动主程序

在第二个终端窗口中运行：

```powershell
uv run d:/DevMate/main.py
```

### 方式二：Docker 部署（推荐）

所有服务都运行在 Docker 容器中。

#### 步骤 1：配置环境变量或者修改配置文件config.toml

创建 `.env` 文件（如果还没有）：
```powershell
notepad .env
```

添加以下内容：
```env
# LLM 配置（必须）
MODEL_API_KEY=your_model_api_key_here

# Embedding 配置（必须）
EMBEDDING_API_KEY=your_embedding_api_key_here

# Tavily 搜索 API（必须）
TAVILY_API_KEY=your_tavily_api_key_here

# LangSmith 配置（可选）
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

#### 步骤 2：构建并启动服务

```powershell
# 构建镜像并启动所有服务（后台运行）
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看 MCP Server 日志
docker-compose logs -f mcp-server
```

#### 步骤 3：启动交互式对话

```powershell
# 启动交互式主程序
docker-compose run --rm devmate-app
```

#### 步骤 4：停止服务

```powershell
# 停止所有服务
docker-compose down

# 停止并删除数据卷（彻底清理）
docker-compose down -v
```

### Docker 服务架构

```
┌─────────────────────────────────────────┐
│           Docker Compose                │
│                                         │
│  ┌─────────────────────────────────────┐│
│  │           mcp-server                ││
│  │  - Port 8000 (MCP Search API)      ││
│  │  - Tavily 网络搜索                  ││
│  │  - ChromaDB 知识库                  ││
│  └─────────────────────────────────────┘│
│                    │                   │
│                    ▼                   │
│  ┌─────────────────────────────────────┐│
│  │         devmate-app                 ││
│  │  - 交互式对话终端                   ││
│  │  - Agent 智能助手                   ││
│  │  - 文件操作 (/app/test_dir)        ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
          │
          ▼
   ./test_dir (文件操作目录 - 自动挂载)
```

### Docker 卷挂载说明

| 宿主机目录 | 容器内路径 | 用途 |
|-----------|----------|------|
| `./src` | `/app/src` | 代码目录 |
| `./config.toml` | `/app/config.toml` | 配置文件 |
| `./test_dir` | `/app/test_dir` | **Agent 生成文件的目录** |
| `./docs` | `/app/docs` | RAG 文档目录 |
| `./main.py` | `/app/main.py` | 主程序 |
| `vector_db` (卷) | `/app/vector_db` | ChromaDB 持久化数据 |

**重要**：Agent 创建的文件会在容器的 `/app/test_dir` 中，自动同步到宿主机的 `./test_dir` 文件夹。

### 验证 Docker 部署

```powershell
# 检查 MCP Server 健康状态
curl http://localhost:8000/health

# 查看生成的文件
ls -la ./test_dir/

# 进入容器内部查看
docker-compose exec devmate-app ls -la /app/test_dir/
```

## 使用示例

启动后，你可以与 DevMate 进行对话：

```
用户: 你好，请介绍一下你自己
DevMate: 你好！我是你的AI编程助手...

用户: 我想创建一个 FastAPI 项目
DevMate: 好的，我来帮你创建一个 FastAPI 项目...

用户: 项目名称叫 my-api
DevMate: 已经为你创建好了 my-api 项目，包含以下文件...
```

### 对话示例

#### 1. 简单对话
```
用户: 你好
DevMate: 你好！我是 Claude，一个智能编程助手...
```

#### 2. 文件操作
```
用户: 帮我创建一个 test.txt 文件，内容为 Hello World
DevMate: 已成功创建 test.txt 文件，内容为 Hello World
```

#### 3. 技能加载
```
用户: 请加载 create-python-project 技能
DevMate: create-python-project 技能已加载成功！...
```

#### 4. 记忆功能
```
用户: 我叫张三
DevMate: 你好张三，很高兴认识你！...

用户: 我叫什么名字？
DevMate: 你叫张三！...
```

## 项目结构

```
DevMate/
├── src/
│   └── devmate/
│       ├── agents/           # Agent 相关代码
│       │   ├── agent.py      # Agent 主类
│       │   └── prompts.py    # 系统提示词
│       ├── mcp/              # MCP 协议相关
│       │   ├── client.py     # MCP 客户端
│       │   └── server.py     # MCP 服务器
│       ├── rag/              # RAG 相关
│       │   └── retriever.py  # 检索器
│       ├── skills/            # 技能系统
│       │   └── manager.py    # 技能管理器
│       ├── tools/            # 工具集
│       │   └── tools.py     # 文件操作工具
│       └── utils/            # 工具函数
│           ├── config.py     # 配置管理
│           ├── llm.py        # LLM 初始化
│           └── logger.py     # 日志
├── .skills/                  # 技能目录
│   ├── create-fastapi-service/
│   ├── create-python-project/
│   └── ... (其他技能)
├── docs/                     # RAG 文档目录
├── test_dir/                 # 文件操作目录
├── config.toml               # 配置文件
├── pyproject.toml            # 项目配置
├── Dockerfile                # Docker 镜像构建
├── docker-compose.yml        # Docker 服务编排
└── main.py                   # 主入口
```

## 配置文件

配置文件位于 `config.toml`，包含以下部分：

```toml
[model]                 # 模型配置
ai_base_url = "https://api.modelverse.cn/v1/"
api_key = "${MODEL_API_KEY}"
model_name = "gpt-5.1"

[embedding]            # Embedding 配置
ai_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "${EMBEDDING_API_KEY}"
model_name = "text-embedding-v4"

[search]               # 搜索配置
tavily_api_key = "${TAVILY_API_KEY}"

[skills]               # 技能配置
skills_dir = ".skills"
```

## 技能系统

DevMate 支持动态加载技能。每个技能是一个包含 `SKILL.md` 文件的目录：

```markdown
---
name: skill-name
description: 技能描述
---

# 技能名称

技能说明和使用方法...
```

### 内置技能

- `create-fastapi-service`: 创建 FastAPI 服务
- `create-python-project`: 创建 Python 项目
- `skill-creator`: 创建新技能

## 注意事项

### 环境变量

⚠️ **重要**：必须配置以下环境变量（`.env` 文件）才能正常运行：

| 环境变量 | 必须 | 说明 |
|---------|------|------|
| `MODEL_API_KEY` | ✅ 必须 | LLM 模型 API 密钥 |
| `EMBEDDING_API_KEY` | ✅ 必须 | Embedding 模型 API 密钥 |
| `TAVILY_API_KEY` | ✅ 必须 | Tavily 搜索 API 密钥 |
| `LANGCHAIN_API_KEY` | ❌ 可选 | LangSmith 追踪密钥 |

### 其他注意事项

1. **依赖版本**：建议使用 Python 3.13+ 以获得最佳兼容性
2. **MCP Server**：本地运行时 MCP Server 必须先于主程序启动
3. **线程 ID**：使用相同的线程 ID 可以保持对话记忆
4. **Docker 端口**：确保 8000 端口未被占用

## 常见问题

### Q: Docker 服务无法启动？

1. 确保 Docker Desktop 已安装并运行
2. 检查端口 8000 是否被占用
3. 查看日志：`docker-compose logs -f mcp-server`

### Q: MCP Server 返回 404 或连接失败？

1. 检查 `.env` 文件中的 API keys 是否正确配置
2. 确保 MCP Server 已启动：`docker-compose ps`
3. 检查健康状态：`curl http://localhost:8000/health`

### Q: Agent 返回"未获取到结果"？

1. 检查 LLM API 密钥是否正确配置
2. 检查网络连接是否正常
3. 查看 Agent 日志

### Q: 文件操作不生效？

1. 确保使用 `./test_dir` 目录进行文件操作
2. 检查容器是否有正确的卷挂载
3. 验证宿主机目录权限

### Q: 如何清理 Docker 环境？

```powershell
# 停止所有服务
docker-compose down

# 删除镜像
docker-compose down --rmi all

# 删除数据卷
docker-compose down -v

# 完全清理
docker system prune -a
```

## 许可证

MIT License

## 作者

DevMate Team
