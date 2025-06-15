# BI 智能分析系统

这是一个基于自然语言查询的智能数据分析系统，支持通过聊天界面进行数据查询和分析。

## 功能特点

- 自然语言转SQL查询
- 智能数据分析
- 可视化图表展示
- 实时聊天界面

## 系统要求

- Node.js 14+
- Python 3.8+
- MySQL 8.0+
- OpenManus CLI

## 安装步骤

### 前端

```bash
cd bi-frontend
npm install
npm start
```

### 后端

```bash
cd bi-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 使用说明

1. 启动前端和后端服务
2. 在浏览器中访问 http://localhost:3000
3. 在聊天界面输入您的查询
4. 系统会生成相应的SQL语句
5. 确认执行后，系统会返回分析结果和可视化图表

## 配置说明

1. 确保已安装并配置好OpenManus CLI
2. 在bi-backend目录下创建.env文件，配置数据库连接信息：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

## 注意事项

- 请确保OpenManus CLI已正确安装并配置
- 数据库连接信息请妥善保管
- 建议在生产环境中使用HTTPS 