import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { CheckCircle, XCircle, Mail, RefreshCw } from 'lucide-react';

const EmailVerification = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const { verifyEmail, resendVerification } = useAuth();
  const [status, setStatus] = useState('verifying'); // verifying, success, error
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  const [resending, setResending] = useState(false);

  useEffect(() => {
    if (token) {
      handleVerification();
    }
  }, [token]);

  const handleVerification = async () => {
    setStatus('verifying');
    const result = await verifyEmail(token);
    
    if (result.success) {
      setStatus('success');
      setMessage(result.message);
      setTimeout(() => {
        navigate('/dashboard');
      }, 3000);
    } else {
      setStatus('error');
      setMessage(result.error);
    }
  };

  const handleResendVerification = async (e) => {
    e.preventDefault();
    if (!email) return;
    
    setResending(true);
    const result = await resendVerification(email);
    
    if (result.success) {
      setMessage(result.message);
      setStatus('resent');
    } else {
      setMessage(result.error);
    }
    setResending(false);
  };

  return (
    <div className="container">
      <div className="auth-form" style={{ maxWidth: '600px', textAlign: 'center' }}>
        {status === 'verifying' && (
          <>
            <div style={{ marginBottom: '24px' }}>
              <RefreshCw size={48} style={{ color: 'var(--custom-blue)', animation: 'spin 1s linear infinite' }} />
            </div>
            <h2 style={{ marginBottom: '16px' }}>Verifying Your Email</h2>
            <p style={{ color: 'var(--medium-gray)' }}>
              Please wait while we verify your email address...
            </p>
          </>
        )}

        {status === 'success' && (
          <>
            <div style={{ marginBottom: '24px' }}>
              <CheckCircle size={48} style={{ color: 'var(--success-green)' }} />
            </div>
            <h2 style={{ marginBottom: '16px', color: 'var(--success-green)' }}>
              Email Verified Successfully!
            </h2>
            <div className="alert alert-success">
              {message}
            </div>
            <p style={{ color: 'var(--medium-gray)' }}>
              Redirecting to dashboard in 3 seconds...
            </p>
          </>
        )}

        {status === 'error' && (
          <>
            <div style={{ marginBottom: '24px' }}>
              <XCircle size={48} style={{ color: 'var(--error-red)' }} />
            </div>
            <h2 style={{ marginBottom: '16px', color: 'var(--error-red)' }}>
              Verification Failed
            </h2>
            <div className="alert alert-error">
              {message}
            </div>
            
            <div style={{ marginTop: '32px', textAlign: 'left' }}>
              <h3 style={{ marginBottom: '16px' }}>Need a new verification link?</h3>
              <form onSubmit={handleResendVerification}>
                <div className="form-group">
                  <label htmlFor="email">
                    <Mail size={18} style={{ marginRight: '8px' }} />
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="Enter your email address"
                  />
                </div>
                <button 
                  type="submit" 
                  className="btn btn-primary" 
                  disabled={resending}
                  style={{ width: '100%' }}
                >
                  {resending ? 'Sending...' : 'Resend Verification Email'}
                </button>
              </form>
            </div>
          </>
        )}

        {status === 'resent' && (
          <>
            <div style={{ marginBottom: '24px' }}>
              <Mail size={48} style={{ color: 'var(--custom-blue)' }} />
            </div>
            <h2 style={{ marginBottom: '16px', color: 'var(--custom-blue)' }}>
              Verification Email Sent
            </h2>
            <div className="alert alert-success">
              {message}
            </div>
            <p style={{ color: 'var(--medium-gray)' }}>
              Please check your email and click the verification link.
            </p>
          </>
        )}

        <div style={{ marginTop: '32px' }}>
          <button 
            onClick={() => navigate('/login')} 
            className="btn btn-secondary"
          >
            Back to Login
          </button>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default EmailVerification;