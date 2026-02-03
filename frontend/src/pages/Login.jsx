import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, LogIn } from 'lucide-react';
import ForgotPasswordModal from '../components/ForgotPasswordModal';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      navigate('/2fa-verification');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  const handleForgotPasswordSuccess = (message) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(''), 5000);
  };

  return (
    <div className="container">
      <h1>Welcome Back</h1>
      
      <form onSubmit={handleSubmit} className="auth-form">
        {successMessage && (
          <div className="alert alert-success">
            {successMessage}
          </div>
        )}
        
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="email">
            <Mail size={18} style={{ marginRight: '8px' }} />
            Email Address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="Enter your email"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">
            <Lock size={18} style={{ marginRight: '8px' }} />
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="Enter your password"
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={loading}
          style={{ width: '100%', marginBottom: '24px' }}
        >
          {loading ? (
            'Signing In...'
          ) : (
            <>
              <LogIn size={18} style={{ marginRight: '8px' }} />
              Sign In
            </>
          )}
        </button>

        <div style={{ textAlign: 'center', marginBottom: '16px' }}>
          <button
            type="button"
            onClick={() => setShowForgotPasswordModal(true)}
            className="btn btn-secondary"
          >
            <Mail size={18} style={{ marginRight: '8px' }} />
            Forgot Password?
          </button>
        </div>

        <div style={{ textAlign: 'center' }}>
          <p style={{ color: 'var(--medium-gray)' }}>
            Don't have an account?{' '}
            <Link 
              to="/register" 
              style={{ 
                color: 'var(--custom-blue)', 
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Sign up here
            </Link>
          </p>
        </div>
      </form>

      {/* Forgot Password Modal */}
      <ForgotPasswordModal
        isOpen={showForgotPasswordModal}
        onClose={() => setShowForgotPasswordModal(false)}
        onSuccess={handleForgotPasswordSuccess}
        prefilledEmail={formData.email}
      />
    </div>
  );
};

export default Login;