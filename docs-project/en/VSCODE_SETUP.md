# VS Code 配置说明

本项目已配置完整的 VS Code 开发环境，支持一键运行 Django 项目。

## 📁 配置文件结构

```
.vscode/
├── launch.json          # 调试/运行配置（F5 快捷键）
├── settings.json        # 项目设置（Python 解释器、格式化等）
├── tasks.json           # 任务配置（Cmd+Shift+B 快捷键）
└── extensions.json      # 推荐扩展列表
```

---

## 🚀 一键运行方法

### 方法 1: 使用调试面板（推荐）

1. **打开调试面板：**
   - 快捷键：`F5` 或 `Cmd+Shift+D`（Mac）/ `Ctrl+Shift+D`（Windows）
   - 或点击左侧活动栏的"运行和调试"图标（▶️）

2. **选择运行配置：**
   在调试面板顶部下拉菜单中选择：
   - **Django Server** - 启动开发服务器（支持热重载）
   - **Django Server (No Reload)** - 启动服务器（不自动重载）
   - **Django Shell** - 启动 Django 交互式 Shell
   - **Generate Static Site** - 生成静态站点

3. **点击绿色运行按钮** 或按 `F5`

4. **自动操作：**
   - ✅ 激活 Conda 环境
   - ✅ 设置环境变量
   - ✅ 启动 Django 服务器
   - ✅ 在集成终端显示输出

### 方法 2: 使用任务（Tasks）

1. **打开命令面板：**
   - 快捷键：`Cmd+Shift+P`（Mac）/ `Ctrl+Shift+P`（Windows）

2. **输入并选择：**
   ```
   Tasks: Run Task
   ```

3. **选择任务：**
   - **Run Django Server** - 运行开发服务器
   - **Generate Static Site** - 生成静态站点
   - **Make Migrations** - 创建数据库迁移
   - **Migrate Database** - 应用数据库迁移
   - **Django Shell** - 启动交互式 Shell
   - **Create Superuser** - 创建管理员账号

4. **快捷键运行默认任务：**
   - `Cmd+Shift+B`（Mac）/ `Ctrl+Shift+B`（Windows）
   - 默认运行 "Run Django Server"

### 方法 3: 使用右键菜单

1. **打开 `manage.py` 文件**

2. **右键点击编辑器**

3. **选择 "Run Python File in Terminal"**

---

## 📝 配置文件详解

### 1. launch.json - 调试/运行配置

```json
{
    "name": "Django Server",           // 配置名称
    "type": "debugpy",                 // Python 调试器类型
    "request": "launch",               // 启动类型
    "program": "${workspaceFolder}/manage.py",  // 运行的文件
    "args": ["runserver", "8000"],     // 命令行参数
    "django": true,                    // 启用 Django 支持
    "console": "integratedTerminal",   // 在集成终端运行
    "env": {                           // 环境变量
        "PYTHONUNBUFFERED": "1",
        "DJANGO_SETTINGS_MODULE": "RunProject.settings"
    },
    "python": "${env:HOME}/miniconda3/envs/RunProject/bin/python"  // Python 解释器路径
}
```

**关键参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `program` | 要运行的 Python 文件 | `${workspaceFolder}/manage.py` |
| `args` | 传递给程序的参数 | `["runserver", "8000"]` |
| `django` | 启用 Django 特定功能 | `true` |
| `console` | 输出位置 | `integratedTerminal`（集成终端） |
| `python` | Python 解释器路径 | Conda 环境路径 |
| `env` | 环境变量 | Django 配置模块等 |

### 2. settings.json - 项目设置

```json
{
    // Python 解释器路径
    "python.defaultInterpreterPath": "${env:HOME}/miniconda3/envs/RunProject/bin/python",

    // Django 模板支持
    "files.associations": {
        "**/templates/**/*.html": "django-html"
    },

    // Emmet 支持 Django 模板
    "emmet.includeLanguages": {
        "django-html": "html"
    }
}
```

**主要功能：**
- ✅ 指定 Python 解释器（Conda 环境）
- ✅ Django 模板语法高亮
- ✅ Emmet 代码补全支持
- ✅ 自动排除 `__pycache__` 等文件

### 3. tasks.json - 任务配置

```json
{
    "label": "Run Django Server",      // 任务名称
    "type": "shell",                   // 类型：Shell 命令
    "command": "source ~/miniconda3/etc/profile.d/conda.sh && conda activate RunProject && python manage.py runserver",
    "group": {
        "kind": "build",               // 任务组
        "isDefault": true              // 默认任务（Cmd+Shift+B 触发）
    }
}
```

**任务列表：**
1. **Run Django Server** - 启动开发服务器（默认任务）
2. **Generate Static Site** - 生成静态站点
3. **Make Migrations** - 创建数据库迁移
4. **Migrate Database** - 应用数据库迁移
5. **Django Shell** - 启动交互式 Shell
6. **Create Superuser** - 创建管理员账号

---

## 🔧 必需的 VS Code 扩展

打开项目后，VS Code 会自动提示安装以下扩展（已配置在 `extensions.json`）：

### 核心扩展：

1. **Python** (`ms-python.python`)
   - Python 语言支持
   - 代码补全、Linting、调试

2. **Pylance** (`ms-python.vscode-pylance`)
   - 高级 Python 语言服务
   - 类型检查、导入建议

3. **Python Debugger** (`ms-python.debugpy`)
   - Python 调试器
   - 断点、变量查看

4. **Django** (`batisteo.vscode-django`)
   - Django 模板语法高亮
   - 代码片段（snippets）
   - 模板标签补全

### 可选扩展：

5. **Jinja** (`wholroyd.jinja`)
   - Jinja2/Django 模板支持

6. **Prettier** (`esbenp.prettier-vscode`)
   - 代码格式化（HTML/CSS/JS）

---

## 🎯 使用场景示例

### 场景 1: 启动开发服务器

**方式A - 调试面板：**
1. 按 `F5`
2. 选择 "Django Server"
3. 服务器启动在 http://127.0.0.1:8000

**方式B - 任务快捷键：**
1. 按 `Cmd+Shift+B`（Mac）或 `Ctrl+Shift+B`（Windows）
2. 自动运行默认任务 "Run Django Server"

**方式C - 命令面板：**
1. 按 `Cmd+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 "Run Django Server"

### 场景 2: 调试代码（设置断点）

1. **在代码行号左侧点击设置断点**（红点）
   - 例如：`app/views.py` 第 10 行

2. **按 `F5` 启动调试模式**
   - 选择 "Django Server"

3. **访问触发断点的 URL**
   - 例如：http://127.0.0.1:8000/articles/

4. **使用调试工具：**
   - **继续**（F5）- 继续执行
   - **单步跳过**（F10）- 执行下一行
   - **单步进入**（F11）- 进入函数内部
   - **单步跳出**（Shift+F11）- 跳出当前函数
   - **查看变量** - 左侧调试面板查看变量值

### 场景 3: 生成静态站点

**方式A - 调试面板：**
1. 按 `F5`
2. 选择 "Generate Static Site"
3. 查看终端输出

**方式B - 任务：**
1. 按 `Cmd+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 "Generate Static Site"

### 场景 4: 创建管理员账号

1. 按 `Cmd+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 "Create Superuser"
4. 在终端输入用户名、邮箱、密码

---

## ⚙️ 高级配置

### 修改服务器端口

编辑 `.vscode/launch.json`：
```json
"args": [
    "runserver",
    "8001"  // 改为 8001 端口
]
```

### 添加环境变量

编辑 `.env` 文件：
```bash
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

### 使用不同的 Django 配置文件

编辑 `.vscode/launch.json`：
```json
"env": {
    "DJANGO_SETTINGS_MODULE": "RunProject.settings.production"  // 使用生产配置
}
```

### 启用自动格式化

编辑 `.vscode/settings.json`：
```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black"
}
```

---

## 🆚 VS Code vs PyCharm 对比

| 特性 | VS Code | PyCharm |
|------|---------|---------|
| **一键运行** | ✅ F5 | ✅ Shift+F10 |
| **调试** | ✅ 断点、变量查看 | ✅ 更强大的调试工具 |
| **Django 支持** | ✅ 需安装扩展 | ✅ 原生支持 |
| **配置方式** | JSON 文件 | XML 文件 + 图形界面 |
| **启动速度** | ⚡ 快 | ⚠️ 较慢 |
| **内存占用** | 💚 低 | ⚠️ 高 |
| **代码补全** | ✅ Pylance | ✅ 更智能 |
| **重构工具** | ⚠️ 基础 | ✅ 强大 |
| **免费** | ✅ 完全免费 | ⚠️ 社区版/专业版 |
| **学习曲线** | 💚 较低 | ⚠️ 较高 |

---

## 🔍 故障排查

### 问题 1: 找不到 Python 模块

**症状：**
```
ModuleNotFoundError: No module named 'django'
```

**解决方案：**
1. 检查 `.vscode/launch.json` 中的 Python 路径：
```json
"python": "${env:HOME}/miniconda3/envs/RunProject/bin/python"
```

2. 验证 Conda 环境：
```bash
conda activate RunProject
python -c "import django; print(django.get_version())"
```

### 问题 2: 调试无法启动

**症状：**
点击 F5 没有反应或报错

**解决方案：**
1. 安装 Python 扩展：
   - 打开扩展面板（`Cmd+Shift+X`）
   - 搜索 "Python"
   - 安装 Microsoft 官方 Python 扩展

2. 安装 debugpy：
```bash
conda activate RunProject
pip install debugpy
```

### 问题 3: 终端无法激活 Conda

**症状：**
```
conda: command not found
```

**解决方案：**

编辑 `.vscode/tasks.json`，改用绝对路径：
```json
"command": "/Users/qihao/miniconda3/bin/conda activate RunProject && python manage.py runserver"
```

或者在 VS Code 设置中添加：
```json
{
    "terminal.integrated.profiles.osx": {
        "bash": {
            "path": "/bin/bash",
            "args": ["-l"]  // 加载登录 Shell
        }
    }
}
```

---

## 💡 快捷键速查

| 功能 | Mac | Windows/Linux |
|------|-----|---------------|
| 运行/调试 | `F5` | `F5` |
| 运行默认任务 | `Cmd+Shift+B` | `Ctrl+Shift+B` |
| 命令面板 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 调试面板 | `Cmd+Shift+D` | `Ctrl+Shift+D` |
| 集成终端 | `Cmd+J` | `Ctrl+J` |
| 切换断点 | `F9` | `F9` |
| 单步跳过 | `F10` | `F10` |
| 单步进入 | `F11` | `F11` |

---

## 📚 更多资源

- [VS Code Python 教程](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Django 教程](https://code.visualstudio.com/docs/python/tutorial-django)
- [VS Code 调试指南](https://code.visualstudio.com/docs/editor/debugging)
- [Django 官方文档](https://docs.djangoproject.com/)

---

## ✅ 配置验证清单

在使用前，请确认：

- [x] 已安装 Python 扩展
- [x] 已安装 Django 扩展（可选但推荐）
- [x] `.vscode/launch.json` 存在
- [x] `.vscode/settings.json` 存在
- [x] `.vscode/tasks.json` 存在
- [x] Python 解释器路径正确
- [x] Conda 环境已创建并安装依赖

**快速测试：**
```bash
# 1. 激活环境
conda activate RunProject

# 2. 测试 Django
python manage.py check

# 3. 如果上述命令成功，VS Code 配置就可以正常工作
```

---

**🎉 配置完成！现在可以在 VS Code 中一键运行 Django 项目了！**

按 `F5` 开始体验吧！
