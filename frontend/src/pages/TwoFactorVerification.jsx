import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, ArrowLeft, RefreshCw } from 'lucide-react';
import TwoFactorModal from '../components/TwoFactorModal';
import axios from 'axios';

const TwoFactorVerification = () => {
  const [verificationCode, setVerificationCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [is2FAEnabled, setIs2FAEnabled] = useState(false);
  const [showSetupModal, setShowSetupModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  const { user, logout, mark2FAVerified } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    check2FAStatus();
  }, []);

  const check2FAStatus = async () => {
    try {
      const response = await axios.get('/api/auth/2fa-status/');
      setIs2FAEnabled(response.data.is_2fa_enabled);
    } catch (error) {
      console.error('Failed to check 2FA status:', error);
    }
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    
    if (!is2FAEnabled) {
      // If 2FA is not enabled, mark as verified and redirect to dashboard
      mark2FAVerified();
      navigate('/dashboard');
      return;
    }

    if (!verificationCode || verificationCode.length !== 6) {
      setError('Please enter a valid 6-digit code');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await axios.post('/api/auth/verify-2fa-login/', {
        code: verificationCode
      });
      
      // Mark 2FA as verified in the session
      mark2FAVerified();
      
      // If verification successful, proceed to dashboard
      navigate('/dashboard');
    } catch (error) {
      setError(error.response?.data?.error || 'Invalid verification code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSkipFor2FASetup = () => {
    // Only allow skipping for regular users, not admins
    if (user?.role === 'admin') {
      setError('Administrators must enable 2FA for security. Please set up 2FA to continue.');
      return;
    }
    
    if (!is2FAEnabled) {
      mark2FAVerified();
      navigate('/dashboard');
    }
  };

  const handleSetupSuccess = (message) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(''), 5000);
    check2FAStatus();
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="container">
      <div style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <Shield size={64} style={{ color: 'var(--custom-blue)', marginBottom: '16px' }} />
          <h1>Two-Factor Authentication</h1>
          <p style={{ color: 'var(--medium-gray)', fontSize: '16px' }}>
            {is2FAEnabled 
              ? 'Enter the 6-digit code from your authenticator app to continue'
              : 'Enhance your account security by setting up two-factor authentication'
            }
          </p>
        </div>

        {successMessage && (
          <div className="alert alert-success" style={{ marginBottom: '20px' }}>
            {successMessage}
          </div>
        )}

        {is2FAEnabled ? (
          // 2FA Verification Form
          <form onSubmit={handleVerifyCode} className="auth-form">
            {error && (
              <div className="alert alert-error">
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="code">Verification Code</label>
              <input
                type="text"
                id="code"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                className="code-input"
                maxLength={6}
                required
                style={{
                  fontSize: '24px',
                  letterSpacing: '8px',
                  textAlign: 'center',
                  padding: '16px',
                  fontFamily: 'monospace'
                }}
              />
            </div>

            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading || verificationCode.length !== 6}
              style={{ width: '100%', marginBottom: '16px' }}
            >
              {loading ? (
                <>
                  <RefreshCw size={18} style={{ marginRight: '8px' }} className="spinning" />
                  Verifying...
                </>
              ) : (
                <>
                  <Shield size={18} style={{ marginRight: '8px' }} />
                  Verify & Continue
                </>
              )}
            </button>

            <div style={{ textAlign: 'center' }}>
              <button
                type="button"
                onClick={handleLogout}
                className="btn btn-secondary"
                style={{ marginRight: '12px' }}
              >
                <ArrowLeft size={18} style={{ marginRight: '8px' }} />
                Back to Login
              </button>
            </div>
          </form>
        ) : (
          // 2FA Setup Options
          <div className="auth-form">
            <div style={{ 
              backgroundColor: user?.role === 'admin' ? 'var(--error-red-light)' : 'var(--background-light)', 
              padding: '24px', 
              borderRadius: '12px', 
              marginBottom: '24px',
              textAlign: 'center',
              border: user?.role === 'admin' ? '2px solid var(--error-red)' : 'none'
            }}>
              <Shield size={48} style={{ 
                color: user?.role === 'admin' ? 'var(--error-red)' : 'var(--warning-yellow)', 
                marginBottom: '16px' 
              }} />
              <h3 style={{ margin: '0 0 12px 0', color: 'var(--text-dark)' }}>
                {user?.role === 'admin' ? '2FA Required for Administrators' : '2FA Not Enabled'}
              </h3>
              <p style={{ color: 'var(--medium-gray)', margin: 0 }}>
                {user?.role === 'admin' 
                  ? 'As an administrator, you must enable two-factor authentication to access the system. This is required for security compliance.'
                  : 'Your account is not protected with two-factor authentication. We recommend enabling 2FA for enhanced security.'
                }
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', flexDirection: 'column' }}>
              <button
                onClick={() => setShowSetupModal(true)}
                className="btn btn-primary"
                style={{ width: '100%' }}
              >
                <Shield size={18} style={{ marginRight: '8px' }} />
                Set Up 2FA Now
              </button>
              
              {user?.role !== 'admin' && (
                <button
                  onClick={handleSkipFor2FASetup}
                  className="btn btn-secondary"
                  style={{ width: '100%' }}
                >
                  Skip for Now
                </button>
              )}
              
              {user?.role === 'admin' && (
                <p style={{ 
                  color: 'var(--error-red)', 
                  fontSize: '14px', 
                  textAlign: 'center',
                  margin: '8px 0 0 0',
                  fontWeight: '500'
                }}>
                  2FA setup is mandatory for administrator accounts
                </p>
              )}
            </div>

            <div style={{ textAlign: 'center', marginTop: '24px' }}>
              <button
                type="button"
                onClick={handleLogout}
                className="btn btn-secondary"
              >
                <ArrowLeft size={18} style={{ marginRight: '8px' }} />
                Back to Login
              </button>
            </div>
          </div>
        )}

        <div style={{ 
          marginTop: '32px', 
          padding: '20px', 
          backgroundColor: 'var(--background-light)', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <p style={{ color: 'var(--medium-gray)', fontSize: '14px', margin: 0 }}>
            <strong>Logged in as:</strong> {user?.email}
          </p>
        </div>
      </div>

      {/* 2FA Setup Modal */}
      <TwoFactorModal
        isOpen={showSetupModal}
        onClose={() => setShowSetupModal(false)}
        onSuccess={handleSetupSuccess}
        is2FAEnabled={is2FAEnabled}
      />
    </div>
  );
};

export default TwoFactorVerification;