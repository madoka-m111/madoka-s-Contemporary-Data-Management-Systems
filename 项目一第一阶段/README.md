# 基于 MongoDB 的问卷系统

## 项目简介

本项目是一个简化版的在线问卷系统。系统允许注册用户创建问卷，通过链接分发问卷，其他用户填写，系统统计问卷结果。

本项目使用 **MongoDB** 作为后端数据库，**Flask** 作为后端框架，前端使用纯 HTML/CSS/JS 实现。

## 项目结构

```
survey_system/
├── README.md                          # 项目说明文档
├── requirements.txt                   # Python依赖包列表
├── .env.example                       # 环境变量示例文件
├── .gitignore                         # Git忽略文件
├── run.py                             # Flask应用入口
│
├── config/
│   ├── __init__.py
│   └── settings.py                    # 配置文件（数据库连接、端口等）
│
├── app/
│   ├── __init__.py                    # Flask应用初始化
│   ├── models/                        # MongoDB数据模型层
│   │   ├── __init__.py
│   │   ├── user.py                    # 用户模型
│   │   ├── survey.py                  # 问卷模型
│   │   ├── question.py                # 题目模型
│   │   └── response.py                # 回答记录模型
│   │
│   ├── routes/                        # 路由层（API接口）
│   │   ├── __init__.py
│   │   ├── auth_routes.py             # 注册/登录接口
│   │   ├── survey_routes.py           # 问卷创建/管理接口
│   │   ├── fill_routes.py             # 填写问卷接口
│   │   └── stats_routes.py            # 统计结果接口
│   │
│   ├── services/                      # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py            # 用户服务
│   │   ├── survey_service.py          # 问卷服务
│   │   ├── question_service.py        # 题目服务
│   │   ├── validation_service.py      # 答案校验服务
│   │   ├── jump_service.py            # 跳转逻辑服务
│   │   ├── response_service.py        # 回答服务
│   │   └── stats_service.py           # 统计服务
│   │
│   ├── utils/                         # 工具函数
│   │   ├── __init__.py
│   │   ├── validators.py              # 通用校验函数
│   │   └── response_util.py           # 统一响应格式
│   │
│   └── static/                        # 前端静态文件
│       ├── css/style.css
│       ├── js/
│       └── index.html
│
├── frontend/                          # 前端页面
│   ├── login.html                     # 登录页
│   ├── register.html                  # 注册页
│   ├── dashboard.html                 # 问卷管理页
│   ├── create.html                    # 创建问卷页
│   ├── edit.html                      # 编辑问卷页
│   ├── survey.html                    # 填写问卷页
│   └── stats.html                     # 统计结果页
│
├── templates/                         # Jinja2模板
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── survey_create.html
│   ├── survey_fill.html
│   └── survey_stats.html
│
├── tests/                             # 测试用例
│   ├── __init__.py
│   ├── conftest.py                    # pytest配置
│   ├── test_auth.py                   # 用户注册登录测试
│   ├── test_survey_create.py          # 创建问卷测试
│   ├── test_question_add.py           # 添加题目测试
│   ├── test_jump_logic.py             # 跳转逻辑测试
│   ├── test_validation.py             # 校验测试
│   ├── test_submit.py                 # 提交问卷测试
│   └── test_stats.py                  # 统计测试
│
├── scripts/
│   ├── init_db.py                     # 初始化数据库脚本
│   └── seed_data.py                   # 测试数据填充脚本
│
└── docs/
    ├── 数据库设计.md                   # MongoDB Schema设计文档
    ├── API说明.md                      # 接口文档
    ├── 测试用例.md                     # 测试用例文档
    ├── AI使用日志.md                   # AI使用过程记录
    └── 项目完成报告.md                 # 项目完成报告
```

## 技术栈

- **后端语言**: Python 3.13
- **后端框架**: Flask 3.0.0
- **数据库**: MongoDB 8.3.11
- **认证**: Flask-JWT-Extended
- **前端**: HTML5 + CSS3 + 原生 JavaScript，Chart.js（统计图表）
- **测试**: pytest 8.2.0，mongomock（MongoDB 模拟）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 MongoDB

确保本地已安装 MongoDB 并运行在默认端口 27017：

```bash
# Windows
mongod --dbpath D:\mongodb-data --port 27017
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

### 4. 启动应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动。

> 注意：请通过 `http://localhost:5000/login.html` 访问，不要直接双击 HTML 文件，也不要用 VS Code Live Server 打开后再请求接口。前端已兼容这两种情况，会自动把接口指向 `http://localhost:5000/api`。

### 登录/注册提示“网络错误”时

按顺序检查：

1. 页面地址是否为 `http://localhost:5000/login.html`（或 `http://localhost:5000`）。
2. 浏览器访问 `http://localhost:5000/health`，应返回 `{"status":"ok"}`。
3. MongoDB 是否正在运行（Windows 服务或 `mongod` 进程）。
4. 启动后端的终端是否有报错，必要时重启：

   ```bash
   python run.py
   ```

5. 如果 Flask 使用了其他端口（例如 5001），在浏览器控制台执行：

   ```js
   localStorage.setItem('survey_api_base', 'http://localhost:5001');
   location.reload();
   ```

   恢复默认：

   ```js
   localStorage.removeItem('survey_api_base');
   ```

6. 编辑页若提示“问卷 ID 缺失或无效”，请返回首页重新点击“编辑”，不要手动修改地址栏中的 `id`；正常地址应形如 `edit.html?id=24位十六进制ID`。

现在登录/注册失败时会显示具体请求地址和 HTTP 状态，便于定位是后端未启动、地址错误还是接口返回异常。

## 主要功能

### 用户模块
- 用户注册与登录（JWT 认证）
- 查看自己创建的问卷列表

### 问卷模块
- 创建问卷（标题、描述、截止时间、匿名设置等）
- 发布/撤回/关闭问卷
- 获取问卷访问链接（`/survey/<link_code>`）
- 截止时间到达后自动拒绝开始填写、提交和公开链接访问
- 仅草稿状态允许修改问卷和题目
- 删除问卷

### 题目模块
- 支持 9 种题型：单选、多选、下拉、单行文本、多行文本、数字、评分、日期、文件上传
- 动态添加/编辑/删除/排序题目
- 设置必填、选项、校验规则、跳转逻辑
- 多选题可设置最少/最多选择数，或“必须选择数”（精确数量，与最少/最多选择数互斥）
- 文本填空题可设置最少/最多字数；数字填空题可设置最小值/最大值及“仅允许整数”
- 限制条件使用与跳转逻辑一致的折叠卡片，支持独立保存/清除；存在未保存的限制草稿时会拦截整卷保存
- 填写页会校验多选题选择数量、文本字数和数字范围/整数要求，后端提交时再次兜底

### 跳转逻辑
- 根据单选/多选/数字填空结果进行条件跳转
- 支持等于/不等于/包含/大于/小于条件
- 支持跳转到/隐藏/显示动作
- 配置卡片支持收起/显示，选择源题目或修改条件时保持当前展开状态，不会自动收起
- 每个跳转逻辑卡片提供“保存跳转逻辑”按钮：修改后先显示未保存状态，点击保存并校验通过后才生效；编辑页会立即持久化到当前题目，创建页在保存整份问卷后生效
- 跳转规则存储在数据库中，不写死在代码里

### 填写模块
- 支持匿名填写与登录后填写；关闭匿名时强制登录
- 按顺序回答题目，支持自动跳转
- 实时必填校验、文本长度/数字范围前端校验与服务端全量校验
- 草稿自动保存，刷新或重新进入后可恢复
- 可收集填写人邮箱，前后端均校验邮箱格式
- 已跳过的题目即使携带旧答案也会在服务端丢弃

### 统计模块
- 问卷总览（已提交回答数、完成率、平均耗时）
- 每日提交趋势图（折线图）
- 各题型统计（柱状图/环形图/数值分布）
- 导出回答数据（JSON/CSV/Excel，包含收集到的邮箱）

## 测试

```bash
pytest tests/ -v
```

当前共 71 个自动化测试，覆盖认证、问卷/题目 CRUD、状态机、截止时间、匿名限制、跳转逻辑、答案校验、草稿、提交、统计与导出。

## 文档

- `docs/数据库设计.md` - MongoDB Schema 设计
- `docs/API说明.md` - API 接口文档
- `docs/测试用例.md` - 测试用例说明
- `docs/AI使用日志.md` - AI 使用过程记录
- `docs/项目完成报告.md` - 实验报告与项目完成报告
- `docs/项目完成报告.docx` - 实验报告 Word 排版版（由 Markdown 转换生成）
