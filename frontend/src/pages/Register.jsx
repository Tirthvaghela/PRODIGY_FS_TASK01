import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, UserPlus, CheckCircle } from 'lucide-react';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    password_confirm: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [showVerificationMessage, setShowVerificationMessage] = useState(false);
  
  const { register } = useAuth();
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
    setSuccess('');

    if (formData.password !== formData.password_confirm) {
      setError("Passwords don't match");
      setLoading(false);
      return;
    }

    const result = await register(formData);
    
    if (result.success) {
      setSuccess(result.message);
      if (result.verification_required) {
        setShowVerificationMessage(true);
      } else {
        navigate('/dashboard');
      }
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  if (showVerificationMessage) {
    return (
      <div className="container">
        <div className="auth-form" style={{ textAlign: 'center' }}>
          <div style={{ marginBottom: '24px' }}>
            <CheckCircle size={48} style={{ color: 'var(--success-green)' }} />
          </div>
          <h1 style={{ color: 'var(--success-green)', marginBottom: '24px' }}>
            Registration Successful!
          </h1>
          <div className="alert alert-success">
            {success}
          </div>
          <div style={{ marginTop: '24px', padding: '20px', background: 'var(--light-gray)', borderRadius: '8px' }}>
            <h3 style={{ marginBottom: '16px' }}>Next Steps:</h3>
            <ol style={{ textAlign: 'left', color: 'var(--medium-gray)' }}>
              <li>Check your email inbox</li>
              <li>Click the verification link we sent you</li>
              <li>Your account will be activated automatically</li>
            </ol>
          </div>
          <div style={{ marginTop: '24px' }}>
            <Link to="/login" className="btn btn-primary">
              Go to Login
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Create Account</h1>
      
      <form onSubmit={handleSubmit} className="auth-form">
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            {success}
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
          <label htmlFor="username">
            <User size={18} style={{ marginRight: '8px' }} />
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            placeholder="Choose a username"
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
            placeholder="Create a strong password"
            minLength="8"
          />
          <small style={{ color: 'var(--medium-gray)', fontSize: '12px', marginTop: '4px', display: 'block' }}>
            Password must be at least 8 characters long
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="password_confirm">
            <Lock size={18} style={{ marginRight: '8px' }} />
            Confirm Password
          </label>
          <input
            type="password"
            id="password_confirm"
            name="password_confirm"
            value={formData.password_confirm}
            onChange={handleChange}
            required
            placeholder="Confirm your password"
            minLength="8"
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={loading}
          style={{ width: '100%', marginBottom: '24px' }}
        >
          {loading ? (
            'Creating Account...'
          ) : (
            <>
              <UserPlus size={18} style={{ marginRight: '8px' }} />
              Create Account
            </>
          )}
        </button>

        <div style={{ textAlign: 'center' }}>
          <p style={{ color: 'var(--medium-gray)' }}>
            Already have an account?{' '}
            <Link 
              to="/login" 
              style={{ 
                color: 'var(--custom-blue)', 
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Sign in here
            </Link>
          </p>
        </div>

        <div style={{ marginTop: '24px', padding: '16px', background: 'var(--light-gray)', borderRadius: '8px' }}>
          <p style={{ fontSize: '14px', color: 'var(--medium-gray)', margin: 0 }}>
            <strong>Note:</strong> You'll receive a verification email after registration. 
            Please check your inbox and click the verification link to activate your account.
          </p>
        </div>
      </form>
    </div>
  );
};

export default Register;