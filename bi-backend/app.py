from flask import Flask, request, jsonify
from flask_cors import CORS
import pexpect
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# API配置 - 注意：你应该从环境变量中获取API密钥，而不是硬编码在代码中
DEEPSEEK_API_KEY = "sk-c48759e60b744128964eba312240bbe5"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_sql_with_deepseek(query: str) -> str:
    """使用DeepSeek API生成SQL"""
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建提示词
    prompt = f"""基于以下数据库表结构：
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
    
    请根据以下需求生成SQL查询语句：{query}
    只返回SQL语句，不要包含其他解释。"""
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个SQL专家，负责将自然语言转换为SQL查询语句。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def ask_openmanus(user_input: str) -> str:
    """调用OpenManus CLI执行SQL"""
    try:
        # 确保路径正确，假设OpenManus/main.py在项目根目录下
        child = pexpect.spawn('python OpenManus/main.py', encoding='utf-8', timeout=30)
        child.expect('Enter your prompt:')
        child.sendline(user_input)
        child.expect(pexpect.EOF, timeout=300)
        output = child.before
        child.close()
        return output.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/api/generate-sql', methods=['POST'])
def generate_sql():
    """生成SQL查询"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON格式'}), 400
    
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': '查询不能为空'}), 400
        
    sql = generate_sql_with_deepseek(query)
    
    return jsonify({
        'sql': sql,
        'message': 'SQL生成成功，请确认是否执行'
    })

@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    """执行SQL查询"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求体必须为JSON格式'}), 400
    
    sql = data.get('sql', '')
    
    if not sql:
        return jsonify({'error': 'SQL语句不能为空'}), 400
        
    prompt = f"执行以下SQL查询并返回结果：{sql}"
    response = ask_openmanus(prompt)
    
    try:
        # 尝试解析OpenManus返回的JSON格式结果
        result = json.loads(response)
        return jsonify(result)
    except json.JSONDecodeError:
        # 如果不是JSON格式，直接返回文本
        return jsonify({
            'analysis': response,
            'execution_time': 0  # 如果无法解析执行时间，返回0
        })

@app.route('/')
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

if __name__ == '__main__':
    # 确保端口未被占用，可以使用默认的5000端口
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port, host='0.0.0.0')