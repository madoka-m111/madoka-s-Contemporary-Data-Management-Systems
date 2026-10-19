# API 接口文档

## 基础信息

- **Base URL**: `http://localhost:5000/api`
- **认证方式**: JWT Bearer Token
- **Content-Type**: `application/json`

---

## 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

错误响应:
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

---

## 认证相关

### 注册
```
POST /auth/register
```

**请求体:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**响应:**
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": { "id": "...", "username": "...", "email": "..." },
    "access_token": "jwt_token"
  }
}
```

---

### 登录
```
POST /auth/login
```

**请求体:**
```json
{
  "username": "string",
  "password": "string"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": { "id": "...", "username": "...", "email": "..." },
    "access_token": "jwt_token"
  }
}
```

---

### 获取当前用户信息
```
GET /auth/me
Headers: Authorization: Bearer <token>
```

---

## 用户相关

### 获取我的问卷列表
```
GET /surveys
Headers: Authorization: Bearer <token>
Query: status=draft|published|closed, page=1, per_page=10
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "...",
        "title": "...",
        "status": "draft",
        "created_at": "...",
        "response_count": 0
      }
    ],
    "total": 1,
    "page": 1,
    "per_page": 10
  }
}
```

---

## 问卷相关

### 创建问卷
```
POST /surveys
Headers: Authorization: Bearer <token>
```

**请求体:**
```json
{
  "title": "string",
  "description": "string",
  "settings": {
    "allow_anonymous": true,
    "show_progress": true,
    "one_per_user": false,
    "collect_email": false
  },
  "deadline": "2026-12-31T23:59:59Z"
}
```

---

### 获取问卷详情
```
GET /surveys/:id
Headers: Authorization: Bearer <token> (可选，公开问卷无需)
```

---

### 更新问卷基本信息
```
PUT /surveys/:id
Headers: Authorization: Bearer <token>
```

**请求体:**
```json
{
  "title": "string",
  "description": "string",
  "settings": { ... },
  "deadline": "2026-12-31T23:59:59Z"
}
```

---

### 发布问卷
```
POST /surveys/:id/publish
Headers: Authorization: Bearer <token>
```

---

### 关闭问卷
```
POST /surveys/:id/close
Headers: Authorization: Bearer <token>
```

---

### 撤回问卷（已发布 -> 草稿）
```
POST /surveys/:id/unpublish
Headers: Authorization: Bearer <token>
```

---

### 删除问卷
```
DELETE /surveys/:id
Headers: Authorization: Bearer <token>
```

---

### 通过链接码访问问卷（公开）
```
GET /surveys/link/:linkCode
```
无需认证，返回问卷基本信息和题目列表用于填写

---

### 获取公开问卷列表
```
GET /surveys/public
Query: page=1, per_page=10, keyword=搜索词
```

---

## 题目相关

### 添加题目
```
POST /surveys/:id/questions
Headers: Authorization: Bearer <token>
```

**请求体:**
```json
{
  "title": "string",
  "type": "single_choice|multiple_choice|dropdown|text|textarea|number|rating|date|file",
  "order": 0,
  "required": false,
  "options": ["选项A", "选项B"],
  "validation": { "min_length": 1, "max_length": 500 },
  "jump_logic": {
    "condition": "equals",
    "value": "选项A",
    "target_question_id": "...",
    "action": "skip_to"
  }
}
```

---

### 批量添加题目
```
POST /surveys/:id/questions/batch
Headers: Authorization: Bearer <token>
```

**请求体:**
```json
{
  "questions": [ { ... }, { ... } ]
}
```

---

### 修改题目
```
PUT /questions/:id
Headers: Authorization: Bearer <token>
```

**请求体:** 同添加题目，字段均为可选

---

### 删除题目
```
DELETE /questions/:id
Headers: Authorization: Bearer <token>
```

---

### 调整题目顺序
```
PUT /surveys/:id/questions/reorder
Headers: Authorization: Bearer <token>
```

**请求体:**
```json
{
  "question_orders": [
    { "id": "...", "order": 0 },
    { "id": "...", "order": 1 }
  ]
}
```

---

### 获取问卷所有题目
```
GET /surveys/:id/questions
Headers: Authorization: Bearer <token> (可选)
```

---

## 填写相关

### 开始填写（创建回答记录）
```
POST /fill/surveys/:id/start
Headers: Authorization: Bearer <token> (匿名可选)
Body: {}
```
若问卷设置 `allow_anonymous=false`，必须携带有效 token；截止或关闭时返回 400。

**响应:**
```json
{
  "code": 201,
  "data": { "response_id": "...", "started_at": "..." }
}
```

---

### 保存答案（草稿/自动保存）
```
PUT /fill/responses/:responseId/draft
Headers: Authorization: Bearer <token> (匿名可选)
```
只能修改本人创建的回答记录；已提交或已结束的回答不能继续保存草稿。请求体:
```json
{
  "answers": {
    "question_id_1": "选项A",
    "question_id_2": ["选项A", "选项C"]
  }
}
```

---

### 获取当前填写进度
```
GET /fill/responses/:responseId
Headers: Authorization: Bearer <token> (匿名可选)
```
返回回答状态、已保存答案与开始/提交时间；只能查看本人创建的回答记录。

---

### 提交问卷
```
POST /fill/surveys/:id/submit
Headers: Authorization: Bearer <token> (匿名可选)
```

**请求体:**
```json
{
  "response_id": "已创建的回答ID",
  "answers": {
    "question_id_1": "选项A",
    "question_id_2": ["选项A", "选项C"]
  },
  "email": "user@example.com"
}
```
`email` 仅在问卷设置 `collect_email=true` 时保存，填写时必须符合邮箱格式，否则返回 422。

---

### 校验答案
```
GET /fill/surveys/:id/validate
Headers: Authorization: Bearer <token> (可选)
Query: answers={...} (JSON字符串)
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "valid": true,
    "errors": {
      "question_id_1": "此题为必填项"
    }
  }
}
```

---

## 统计相关

### 问卷整体统计
```
GET /stats/surveys/:id
Headers: Authorization: Bearer <token>
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "total_responses": 100,
    "completion_rate": 0.85,
    "avg_duration_seconds": 120,
    "daily_trend": [
      { "date": "2024-01-01", "count": 10 },
      { "date": "2024-01-02", "count": 15 }
    ]
  }
}
```

---

### 单题统计
```
GET /stats/questions/:id
Headers: Authorization: Bearer <token>
```

**响应 (选择题):**
```json
{
  "code": 200,
  "data": {
    "question_id": "...",
    "type": "single_choice",
    "total_answers": 85,
    "skip_count": 15,
    "options": [
      { "text": "选项A", "count": 40, "percentage": 47.1 },
      { "text": "选项B", "count": 30, "percentage": 35.3 },
      { "text": "选项C", "count": 15, "percentage": 17.6 }
    ]
  }
}
```

**响应 (文本题):**
```json
{
  "code": 200,
  "data": {
    "question_id": "...",
    "type": "text",
    "total_answers": 85,
    "skip_count": 15,
    "answers": ["回答1", "回答2", "..."]
  }
}
```

**响应 (数字/评分题):**
```json
{
  "code": 200,
  "data": {
    "question_id": "...",
    "type": "number",
    "total_answers": 85,
    "skip_count": 15,
    "avg": 42.5,
    "min": 10,
    "max": 100,
    "median": 40,
    "distribution": [
      { "range": "0-20", "count": 10 },
      { "range": "21-40", "count": 25 },
      { "range": "41-60", "count": 30 },
      { "range": "61-80", "count": 15 },
      { "range": "81-100", "count": 5 }
    ]
  }
}
```

---

### 导出回答数据
```
GET /stats/surveys/:id/export
Headers: Authorization: Bearer <token>
Query: format=csv|json|xlsx
```

---

## 错误码

| Code | 说明 |
|------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证/Token失效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 冲突(如重复提交) |
| 422 | 数据校验失败 |
| 500 | 服务器内部错误 |