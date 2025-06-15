import React, { useState } from 'react';
import { Button, Input, Card, message, Spin } from 'antd';
import { SendOutlined, CheckOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const API_BASE_URL = 'http://localhost:5000';

interface QueryResult {
  analysis?: string;
  execution_time?: number;
  [key: string]: any;
}

function App() {
  const [query, setQuery] = useState<string>('');
  const [sql, setSql] = useState<string>('');
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate-sql`, {
        query: query
      });
      setSql(response.data.sql);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '未知错误';
      setError('生成SQL时发生错误：' + errorMessage);
      message.error('生成SQL时发生错误');
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async () => {
    if (!sql) return;
    
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_BASE_URL}/api/execute-sql`, {
        sql: sql
      });
      setResult(response.data);
      message.success('查询执行成功');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '未知错误';
      setError('执行SQL时发生错误：' + errorMessage);
      message.error('执行SQL时发生错误');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '24px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '24px' }}>
        BI 智能查询系统
      </h1>
      
      <Card style={{ marginBottom: '24px' }}>
        <TextArea
          rows={4}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="请输入您的查询需求"
          style={{ marginBottom: '16px' }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSubmit}
          loading={loading}
          disabled={!query.trim()}
        >
          生成SQL
        </Button>
      </Card>

      {sql && (
        <Card style={{ marginBottom: '24px' }}>
          <h3>生成的SQL语句：</h3>
          <Card type="inner" style={{ marginBottom: '16px', backgroundColor: '#f5f5f5' }}>
            <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>
              {sql}
            </pre>
          </Card>
          <Button
            type="primary"
            icon={<CheckOutlined />}
            onClick={handleExecute}
            loading={loading}
            style={{ backgroundColor: '#52c41a', borderColor: '#52c41a' }}
          >
            确认执行
          </Button>
        </Card>
      )}

      {loading && (
        <div style={{ textAlign: 'center', margin: '24px 0' }}>
          <Spin size="large" />
        </div>
      )}

      {error && (
        <Card style={{ marginBottom: '24px', backgroundColor: '#fff2f0' }}>
          <p style={{ color: '#ff4d4f', margin: 0 }}>{error}</p>
        </Card>
      )}

      {result && (
        <Card>
          <h3>查询结果：</h3>
          <Card type="inner" style={{ backgroundColor: '#f5f5f5' }}>
            <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </Card>
        </Card>
      )}
    </div>
  );
}

export default App; 