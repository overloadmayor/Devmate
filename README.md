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
   - 复制 `.env.example` 为 `.env`
   - 填入必要的 API 密钥（OpenAI、Tavily 等）

## 使用方法

### 启动服务

DevMate 需要启动两个服务：MCP Server 和主程序。

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

### 使用示例

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
├── config.toml               # 配置文件
├── pyproject.toml            # 项目配置
└── main.py                   # 主入口
|   ├── result/               # 运行结果截图
```

## 配置文件

配置文件位于 `config.toml`，包含以下部分：

```toml
[model]                 # 模型配置
[search]                # 搜索配置
[langsmith]            # LangSmith 配置（可选）
[skills]                # 技能配置
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

1. **API 密钥**：确保在 `.env` 文件中配置了必要的 API 密钥
2. **依赖版本**：建议使用 Python 3.13+ 以获得最佳兼容性
3. **MCP Server**：MCP Server 必须先于主程序启动
4. **线程 ID**：使用相同的线程 ID 可以保持对话记忆

## 常见问题

### Q: MCP Server 无法启动？

检查 `PYTHONPATH` 环境变量是否正确设置，确保指向 `d:\DevMate\src`。

### Q: Agent 返回"未获取到结果"？

检查 LLM API 密钥是否正确配置，以及网络连接是否正常。

### Q: 记忆功能不工作？

确保在同一线程中使用相同的 `thread_id`。

## 许可证

MIT License

## 作者

DevMate Team
