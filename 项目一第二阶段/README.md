# 基于 MongoDB 的问卷系统

## 项目简介

本项目是一个简化版的在线问卷系统。系统允许注册用户创建问卷，通过链接分发问卷，其他用户填写，系统统计问卷结果。

本项目使用 **MongoDB** 作为后端数据库，**Flask** 作为后端框架，前端使用纯 HTML/CSS/JS 实现。

第二阶段在第一阶段基础上增加了题目库、题目版本、共享、发布锁定、问卷复制和跨问卷统计等功能，旧问卷与旧答卷保持兼容。

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
│   │   ├── question_bank.py           # 题目身份/版本/题库模型（第二阶段）
│   │   └── response.py                # 回答记录模型
│   │
│   ├── routes/                        # 路由层（API接口）
│   │   ├── __init__.py
│   │   ├── auth_routes.py             # 注册/登录接口
│   │   ├── survey_routes.py           # 问卷创建/管理接口
│   │   ├── fill_routes.py             # 填写问卷接口
│   │   ├── question_bank_routes.py    # 题目库/版本/共享/统计接口（第二阶段）
│   │   └── stats_routes.py            # 统计结果接口
│   │
│   ├── services/                      # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py            # 用户服务
│   │   ├── survey_service.py          # 问卷服务
│   │   ├── question_service.py        # 题目服务
│   │   ├── question_bank_service.py   # 题目库/版本/共享业务逻辑（第二阶段）
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
│   ├── question_bank.html              # 题目库管理页（第二阶段）
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
│   ├── test_first_phase.py            # 第一阶段功能回归测试
│   ├── test_question_bank.py          # 题目库/版本/共享/跨问卷统计测试
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
    └── 关键逻辑说明.md                 # 关键逻辑说明
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
- 题目一旦发布过即锁定（撤回后仍锁定），需要继续编辑时复制为新草稿
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

## 第二阶段新增功能

本阶段的核心设计是把“题目身份”和“题目内容”分离：`question_families` 保存稳定身份，`question_versions` 保存不可变版本，问卷中的 `questions` 保存内容快照。这样既能让同一道题被多份问卷复用，又能保证题库后续升版不影响旧问卷和旧答卷。

### 题目库与复用

- 每个用户自动拥有“我的题库”，并可创建、重命名、删除自定义题库
- 同一道题可加入多个题库；从题库移除只解除归集，不删除题目本身
- 新建或编辑问卷时，可从题库选择最新版本或历史版本，支持一次批量加入多道题
- 题库题目按“本人创建 / 被共享 / 公开”范围检索，默认题库不会再遮蔽共享题
- 从题库加入问卷时复制题目内容，并记录 `bank_family_id`、`bank_question_id`、`bank_version` 来源字段

### 版本管理与恢复

- 修改题库题目时只追加新版本，历史版本不可变，避免覆盖旧内容
- 支持查看版本历史、查看当前版本号，以及恢复任意历史版本
- 恢复旧版本不会删除后续版本，而是追加一个新版本并记录 `restored_from_version_id`
- 同一题目的不同版本可同时被不同问卷使用，各问卷内容互不影响
- 问卷保存的是题目内容快照，题库后续升版不会改变已保存问卷

### 共享与派生

- 题目作者可按用户名共享题目，也可将题目设为公开
- 被共享者可查看、引用题目，或将题目复制为自己的题目（fork）
- 被共享者不能修改原题；题目始终保留原作者和来源版本信息
- 共享题默认出现在“全部可用题目”中，切换到自己的题库不会丢失共享题入口

### 发布锁定与问卷复制

- 发布问卷时记录 `published_at`，并将题目永久锁定
- 撤回为草稿后 `published_at` 仍然保留，题目继续锁定，避免旧答卷与题目内容错位
- 只有从未发布过的草稿允许新增、修改、删除、排序题目或从题库选题
- 需要继续编辑已发布问卷时，可复制为新草稿；复制会重建题目 ID，并重写 `jump_logic` 中的源/目标题目引用
- 副本不继承发布状态，可以继续编辑；原问卷、原题目和旧回答保持不变

### 使用情况与跨问卷统计

- 可按题目反查其被哪些问卷使用，并显示各问卷使用的版本、状态和回答数
- 支持单题跨问卷统计，输出总体、按版本、按问卷三种口径
- 总体统计按 `response_id` 去重，避免同一份回答因多个版本重复计数
- 问卷作者可查看自己问卷的统计；被共享者只能统计自己创建的问卷
- 题目库页面提供版本历史、使用情况和跨问卷统计弹窗，避免主列表过于拥挤

### 前端入口

- 新增 `frontend/question_bank.html` 题目库管理页，包含题库列表、题目卡片、搜索和范围筛选
- `dashboard.html` 增加“题目库管理”入口和每份问卷的“复制为新版本”按钮
- `create.html`、`edit.html` 增加“从题库添加题目”弹窗、题库版本标签和发布锁定提示
- 编辑页读取 `questions_locked`，对已发布或曾发布后撤回的问卷禁用题目编辑入口

新增接口统一位于 `/api/question-bank`，覆盖题目与版本、共享与恢复、题库管理、使用情况和单题统计。

## 测试

```bash
pytest tests/ -v
```

当前共 80 个自动化测试，覆盖认证、问卷/题目 CRUD、状态机、截止时间、匿名限制、跳转逻辑、答案校验、草稿、提交、统计与导出；其中第二阶段新增 9 个题目库、版本恢复、共享权限、发布锁定和跨问卷统计测试。

## 文档

- `docs/数据库设计.md` - MongoDB Schema 设计
- `docs/API说明.md` - API 接口文档
- `docs/测试用例.md` - 测试用例说明
- `docs/AI使用日志.md` - AI 使用过程记录
- `docs/关键逻辑说明.md` - 关键逻辑说明
