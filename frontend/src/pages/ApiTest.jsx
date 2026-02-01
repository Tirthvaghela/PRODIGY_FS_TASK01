import { useState } from 'react';
import axios from 'axios';

const ApiTest = () => {
  const [testResults, setTestResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const runTests = async () => {
    setLoading(true);
    const results = [];

    // Test 1: Backend connectivity
    try {
      const response = await axios.get('/api/auth/profile/');
      results.push({ test: 'Backend Connection', status: 'success', message: 'Connected' });
    } catch (error) {
      if (error.response?.status === 401) {
        results.push({ test: 'Backend Connection', status: 'success', message: 'Connected (401 expected)' });
      } else {
        results.push({ test: 'Backend Connection', status: 'error', message: error.message });
      }
    }

    // Test 2: Registration endpoint
    try {
      const testUser = {
        email: `test${Date.now()}@example.com`,
        username: `test${Date.now()}`,
        password: 'TestPass123!',
        password_confirm: 'TestPass123!'
      };
      
      const response = await axios.post('/api/auth/register/', testUser);
      results.push({ test: 'Registration Endpoint', status: 'success', message: 'Working' });
    } catch (error) {
      results.push({ test: 'Registration Endpoint', status: 'error', message: error.response?.data || error.message });
    }

    // Test 3: Login endpoint
    try {
      const response = await axios.post('/api/auth/login/', {
        email: 'admin@prodigyauth.com',
        password: 'ProdigyAdmin123!'
      });
      results.push({ test: 'Login Endpoint', status: 'success', message: 'Working' });
    } catch (error) {
      results.push({ test: 'Login Endpoint', status: 'error', message: error.response?.data || error.message });
    }

    setTestResults(results);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>API Connection Test</h1>
      
      <div className="dashboard-card">
        <h2>Test API Endpoints</h2>
        <button onClick={runTests} className="btn btn-primary" disabled={loading}>
          {loading ? 'Running Tests...' : 'Run API Tests'}
        </button>
        
        {testResults.length > 0 && (
          <div style={{ marginTop: '24px' }}>
            <h3>Test Results:</h3>
            {testResults.map((result, index) => (
              <div 
                key={index} 
                className={`alert ${result.status === 'success' ? 'alert-success' : 'alert-error'}`}
                style={{ marginBottom: '12px' }}
              >
                <strong>{result.test}:</strong> {JSON.stringify(result.message)}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-card">
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <a href="/login" className="btn btn-secondary">Go to Login</a>
          <a href="/register" className="btn btn-info">Go to Register</a>
          <a href="http://127.0.0.1:8000/admin/" target="_blank" className="btn btn-edit">Django Admin</a>
        </div>
      </div>
    </div>
  );
};

export default ApiTest;