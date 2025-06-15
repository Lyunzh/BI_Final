# BI 智能查询系统开发文档

## 项目概述

BI 智能查询系统是一个基于自然语言处理的数据分析工具，它能够将用户的自然语言查询转换为 SQL 语句，并执行查询返回结果。系统采用前后端分离架构，使用现代化的技术栈实现。

## 技术栈

### 后端
- Python 3.x
- Flask (Web 框架)
- DeepSeek API (AI 模型)
- MySQL (数据库)
- OpenManus (SQL 执行引擎)

### 前端
- React 18
- TypeScript
- Ant Design 5.x
- Axios (HTTP 客户端)

## 系统架构

### 后端架构
```
bi-backend/
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖
└── .env               # 环境变量配置
```

### 前端架构
```
bi-frontend/
├── src/
│   ├── App.tsx        # 主应用组件
│   └── index.tsx      # 应用入口
├── public/
│   └── index.html     # HTML 模板
├── package.json       # 项目配置和依赖
└── tsconfig.json      # TypeScript 配置
```

## 功能模块

### 1. 自然语言转 SQL
- 接口：`POST /api/generate-sql`
- 功能：将用户的自然语言查询转换为 SQL 语句
- 实现：使用 DeepSeek API 进行自然语言处理
- 输入：自然语言查询文本
- 输出：生成的 SQL 语句

### 2. SQL 执行
- 接口：`POST /api/execute-sql`
- 功能：执行 SQL 查询并返回结果
- 实现：使用 OpenManus 执行 SQL
- 输入：SQL 语句
- 输出：查询结果和分析

### 3. 前端界面
- 查询输入：支持多行文本输入
- SQL 预览：显示生成的 SQL 语句
- 结果展示：格式化显示查询结果
- 状态反馈：加载状态、错误提示等

## 数据库设计

### news_behavior_wide 表
```sql
CREATE TABLE news_behavior_wide (
  event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  news_id VARCHAR(255) NOT NULL,
  title VARCHAR(500) NOT NULL,
  content LONGTEXT,
  category VARCHAR(20) NOT NULL,
  topic VARCHAR(50) NOT NULL,
  title_length SMALLINT UNSIGNED NOT NULL,
  content_length MEDIUMINT UNSIGNED NOT NULL,
  news_create_time DATETIME(6) NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  event_type ENUM('IMPRESSION','CLICK') NOT NULL,
  event_time DATETIME(6) NOT NULL
)
```

## 重要设计
Openmanus tools设计：
- sql engine tools
- machine learning tools