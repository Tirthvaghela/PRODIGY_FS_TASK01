import { useState, useEffect } from 'react';
import { X, Mail, Send, AlertCircle, CheckCircle, Shield, User, Key } from 'lucide-react';
import axios from 'axios';

const ForgotPasswordModal = ({ isOpen, onClose, onSuccess, prefilledEmail = '' }) => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showEmailInput, setShowEmailInput] = useState(false);
  const [resetMethod, setResetMethod] = useState('email'); // 'email', 'username', 'alternative'
  const [username, setUsername] = useState('');
  const [securityAnswer, setSecurityAnswer] = useState('');

  useEffect(() => {
    if (prefilledEmail) {
      setEmail(prefilledEmail);
      setShowEmailInput(false);
    } else {
      setShowEmailInput(true);
    }
  }, [prefilledEmail]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      let response;
      
      if (resetMethod === 'email') {
        response = await axios.post('/api/auth/forgot-password/', { email });
      } else if (resetMethod === 'username') {
        response = await axios.post('/api/auth/forgot-password-username/', { username });
      } else if (resetMethod === 'alternative') {
        response = await axios.post('/api/auth/forgot-password-alternative/', { 
          email, 
          username, 
          security_answer: securityAnswer 
        });
      }
      
      // Handle successful response
      if (response.data.email_sent || response.data.temp_password_sent) {
        setSuccess(response.data.message);
        onSuccess(response.data.message);
        // Auto close after 4 seconds
        setTimeout(() => {
          handleClose();
        }, 4000);
      }
    } catch (error) {
      if (error.response?.status === 404) {
        setError(error.response.data.error || 'Account not found');
      } else if (error.response?.status === 400) {
        setError(error.response.data.error || 'Invalid request');
      } else {
        setError(error.response?.data?.error || 'Failed to process request. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    onClose();
    setEmail(prefilledEmail || '');
    setUsername('');
    setSecurityAnswer('');
    setError('');
    setSuccess('');
    setShowEmailInput(!prefilledEmail);
    setResetMethod('email');
  };

  const handleChangeEmail = () => {
    setShowEmailInput(true);
    setError('');
    setSuccess('');
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '12px',
        padding: '32px',
        width: '100%',
        maxWidth: '500px',
        margin: '20px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', color: 'var(--text-dark)' }}>
            <Mail size={24} style={{ marginRight: '12px', color: 'var(--custom-blue)' }} />
            Reset Password
          </h2>
          <button
            onClick={handleClose}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '8px',
              borderRadius: '6px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={20} color="var(--medium-gray)" />
          </button>
        </div>

        {/* Reset Method Selection */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            <button
              onClick={() => setResetMethod('email')}
              style={{
                flex: 1,
                padding: '8px 12px',
                border: `2px solid ${resetMethod === 'email' ? 'var(--custom-blue)' : 'var(--border-light)'}`,
                borderRadius: '6px',
                background: resetMethod === 'email' ? '#f0f9ff' : 'white',
                color: resetMethod === 'email' ? 'var(--custom-blue)' : 'var(--medium-gray)',
                fontSize: '14px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Mail size={16} style={{ marginRight: '6px' }} />
              Email Reset
            </button>
            <button
              onClick={() => setResetMethod('username')}
              style={{
                flex: 1,
                padding: '8px 12px',
                border: `2px solid ${resetMethod === 'username' ? 'var(--custom-blue)' : 'var(--border-light)'}`,
                borderRadius: '6px',
                background: resetMethod === 'username' ? '#f0f9ff' : 'white',
                color: resetMethod === 'username' ? 'var(--custom-blue)' : 'var(--medium-gray)',
                fontSize: '14px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <User size={16} style={{ marginRight: '6px' }} />
              Username
            </button>
            <button
              onClick={() => setResetMethod('alternative')}
              style={{
                flex: 1,
                padding: '8px 12px',
                border: `2px solid ${resetMethod === 'alternative' ? 'var(--custom-blue)' : 'var(--border-light)'}`,
                borderRadius: '6px',
                background: resetMethod === 'alternative' ? '#f0f9ff' : 'white',
                color: resetMethod === 'alternative' ? 'var(--custom-blue)' : 'var(--medium-gray)',
                fontSize: '14px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Key size={16} style={{ marginRight: '6px' }} />
              Security Q
            </button>
          </div>
        </div>

        {!showEmailInput && prefilledEmail && resetMethod === 'email' ? (
          // Auto-send mode with prefilled email
          <div>
            <div style={{
              backgroundColor: '#f0f9ff',
              border: '1px solid #bae6fd',
              borderRadius: '8px',
              padding: '16px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center'
            }}>
              <Shield size={18} style={{ marginRight: '12px', color: '#0369a1' }} />
              <div>
                <div style={{ fontSize: '14px', fontWeight: '600', color: '#0369a1', marginBottom: '4px' }}>
                  Ready to send password reset
                </div>
                <div style={{ fontSize: '13px', color: '#0369a1' }}>
                  We'll send a reset link to: <strong>{email}</strong>
                </div>
              </div>
            </div>

            {error && (
              <div style={{
                backgroundColor: '#fee2e2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '20px',
                display: 'flex',
                alignItems: 'center',
                color: '#dc2626'
              }}>
                <AlertCircle size={18} style={{ marginRight: '8px', flexShrink: 0 }} />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div style={{
                backgroundColor: '#d1fae5',
                border: '1px solid #a7f3d0',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '20px',
                display: 'flex',
                alignItems: 'center',
                color: '#065f46'
              }}>
                <CheckCircle size={18} style={{ marginRight: '8px', flexShrink: 0 }} />
                <span>{success}</span>
              </div>
            )}

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'space-between' }}>
              <button
                type="button"
                onClick={handleChangeEmail}
                className="btn btn-secondary"
                disabled={loading || success}
                style={{ flex: 1 }}
              >
                Use Different Method
              </button>
              
              {!success && (
                <button
                  onClick={handleSubmit}
                  className="btn btn-primary"
                  disabled={loading}
                  style={{ flex: 2 }}
                >
                  {loading ? (
                    'Sending Reset Link...'
                  ) : (
                    <>
                      <Send size={18} style={{ marginRight: '8px' }} />
                      Send Reset Link
                    </>
                  )}
                </button>
              )}
              
              {success && (
                <button
                  onClick={handleClose}
                  className="btn btn-primary"
                  style={{ flex: 2 }}
                >
                  Close
                </button>
              )}
            </div>
          </div>
        ) : (
          // Manual input mode
          <div>
            {resetMethod === 'email' && (
              <p style={{ color: 'var(--medium-gray)', marginBottom: '24px', lineHeight: '1.6' }}>
                Enter your email address and we'll send you a reset link instantly.
              </p>
            )}
            {resetMethod === 'username' && (
              <p style={{ color: 'var(--medium-gray)', marginBottom: '24px', lineHeight: '1.6' }}>
                Enter your username and we'll send a temporary password to your registered email.
              </p>
            )}
            {resetMethod === 'alternative' && (
              <p style={{ color: 'var(--medium-gray)', marginBottom: '24px', lineHeight: '1.6' }}>
                Answer the security question to get a temporary password.
              </p>
            )}

            {error && (
              <div style={{
                backgroundColor: '#fee2e2',
                border: '1px solid #fecaca',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '20px',
                display: 'flex',
                alignItems: 'center',
                color: '#dc2626'
              }}>
                <AlertCircle size={18} style={{ marginRight: '8px', flexShrink: 0 }} />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div style={{
                backgroundColor: '#d1fae5',
                border: '1px solid #a7f3d0',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '20px',
                display: 'flex',
                alignItems: 'center',
                color: '#065f46'
              }}>
                <CheckCircle size={18} style={{ marginRight: '8px', flexShrink: 0 }} />
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              {(resetMethod === 'email' || resetMethod === 'alternative') && (
                <div style={{ marginBottom: '20px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid var(--border-light)',
                      borderRadius: '8px',
                      fontSize: '16px',
                      boxSizing: 'border-box'
                    }}
                    placeholder="Enter your email address"
                    disabled={loading || success}
                  />
                </div>
              )}

              {(resetMethod === 'username' || resetMethod === 'alternative') && (
                <div style={{ marginBottom: '20px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
                    Username
                  </label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid var(--border-light)',
                      borderRadius: '8px',
                      fontSize: '16px',
                      boxSizing: 'border-box'
                    }}
                    placeholder="Enter your username"
                    disabled={loading || success}
                  />
                </div>
              )}

              {resetMethod === 'alternative' && (
                <div style={{ marginBottom: '20px' }}>
                  <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
                    Security Question: What is your username?
                  </label>
                  <input
                    type="text"
                    value={securityAnswer}
                    onChange={(e) => setSecurityAnswer(e.target.value)}
                    required
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: '2px solid var(--border-light)',
                      borderRadius: '8px',
                      fontSize: '16px',
                      boxSizing: 'border-box'
                    }}
                    placeholder="Enter your username as the answer"
                    disabled={loading || success}
                  />
                </div>
              )}

              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={handleClose}
                  className="btn btn-secondary"
                  disabled={loading}
                >
                  {success ? 'Close' : 'Cancel'}
                </button>
                {!success && (
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading || 
                      (resetMethod === 'email' && !email) ||
                      (resetMethod === 'username' && !username) ||
                      (resetMethod === 'alternative' && (!email || !username || !securityAnswer))
                    }
                  >
                    {loading ? (
                      resetMethod === 'email' ? 'Sending Link...' : 'Generating Password...'
                    ) : (
                      <>
                        <Send size={18} style={{ marginRight: '8px' }} />
                        {resetMethod === 'email' ? 'Send Reset Link' : 'Get Temporary Password'}
                      </>
                    )}
                  </button>
                )}
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default ForgotPasswordModal;