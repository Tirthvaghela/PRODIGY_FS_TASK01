import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Lock, Eye, EyeOff, CheckCircle, AlertTriangle } from 'lucide-react';
import axios from 'axios';

const PasswordReset = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    new_password: '',
    confirm_password: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    new: false,
    confirm: false
  });
  const [loading, setLoading] = useState(false);
  const [validating, setValidating] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [tokenValid, setTokenValid] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    validateToken();
  }, [token]);

  const validateToken = async () => {
    try {
      const response = await axios.get(`/api/auth/validate-reset-token/${token}/`);
      setTokenValid(response.data.valid);
      setUserEmail(response.data.email);
    } catch (error) {
      setTokenValid(false);
      setError('Invalid or expired reset link');
    } finally {
      setValidating(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords({
      ...showPasswords,
      [field]: !showPasswords[field]
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/reset-password/', {
        token,
        new_password: formData.new_password,
        confirm_password: formData.confirm_password
      });
      
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  if (validating) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <div>Validating reset link...</div>
        </div>
      </div>
    );
  }

  if (!tokenValid) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
          <AlertTriangle size={64} style={{ color: 'var(--error-red)', marginBottom: '24px' }} />
          <h1>Invalid Reset Link</h1>
          <p style={{ color: 'var(--medium-gray)', marginBottom: '32px' }}>
            This password reset link is invalid or has expired. Please request a new one.
          </p>
          <Link to="/login" className="btn btn-primary">
            Back to Login
          </Link>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
          <CheckCircle size={64} style={{ color: 'var(--success-green)', marginBottom: '24px' }} />
          <h1>Password Reset Successful!</h1>
          <p style={{ color: 'var(--medium-gray)', marginBottom: '32px' }}>
            Your password has been successfully reset. You can now log in with your new password.
          </p>
          <p style={{ color: 'var(--medium-gray)', fontSize: '14px' }}>
            Redirecting to login page in 3 seconds...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <Lock size={64} style={{ color: 'var(--custom-blue)', marginBottom: '16px' }} />
          <h1>Reset Your Password</h1>
          <p style={{ color: 'var(--medium-gray)', fontSize: '16px' }}>
            Enter a new password for <strong>{userEmail}</strong>
          </p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="new_password">New Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPasswords.new ? 'text' : 'password'}
                id="new_password"
                name="new_password"
                value={formData.new_password}
                onChange={handleChange}
                required
                minLength={8}
                style={{
                  width: '100%',
                  padding: '12px 40px 12px 12px',
                  border: '2px solid var(--border-light)',
                  borderRadius: '8px',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
                placeholder="Enter your new password (min 8 characters)"
              />
              <button
                type="button"
                onClick={() => togglePasswordVisibility('new')}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '4px'
                }}
              >
                {showPasswords.new ? <EyeOff size={20} color="var(--medium-gray)" /> : <Eye size={20} color="var(--medium-gray)" />}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="confirm_password">Confirm New Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPasswords.confirm ? 'text' : 'password'}
                id="confirm_password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '12px 40px 12px 12px',
                  border: '2px solid var(--border-light)',
                  borderRadius: '8px',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
                placeholder="Confirm your new password"
              />
              <button
                type="button"
                onClick={() => togglePasswordVisibility('confirm')}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '4px'
                }}
              >
                {showPasswords.confirm ? <EyeOff size={20} color="var(--medium-gray)" /> : <Eye size={20} color="var(--medium-gray)" />}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary" 
            disabled={loading}
            style={{ width: '100%', marginBottom: '24px' }}
          >
            {loading ? 'Resetting Password...' : 'Reset Password'}
          </button>

          <div style={{ textAlign: 'center' }}>
            <Link 
              to="/login" 
              style={{ 
                color: 'var(--custom-blue)', 
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Back to Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PasswordReset;