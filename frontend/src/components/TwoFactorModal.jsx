import { useState, useEffect } from 'react';
import { X, Shield, Copy, Check, Smartphone, Key } from 'lucide-react';
import axios from 'axios';

const TwoFactorModal = ({ isOpen, onClose, onSuccess, is2FAEnabled }) => {
  const [step, setStep] = useState(1); // 1: Setup, 2: Verify, 3: Disable
  const [qrCode, setQrCode] = useState('');
  const [secret, setSecret] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [disablePassword, setDisablePassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (isOpen) {
      if (is2FAEnabled) {
        setStep(3); // Go to disable step
      } else {
        setStep(1); // Go to setup step
        setup2FA();
      }
    }
  }, [isOpen, is2FAEnabled]);

  const setup2FA = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/api/auth/setup-2fa/');
      setQrCode(response.data.qr_code);
      setSecret(response.data.secret);
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to setup 2FA');
    } finally {
      setLoading(false);
    }
  };

  const verify2FA = async () => {
    setLoading(true);
    setError('');
    try {
      await axios.post('/api/auth/verify-2fa-setup/', {
        code: verificationCode
      });
      onSuccess('2FA has been successfully enabled!');
      onClose();
      resetModal();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to verify 2FA code');
    } finally {
      setLoading(false);
    }
  };

  const disable2FA = async () => {
    setLoading(true);
    setError('');
    try {
      await axios.post('/api/auth/disable-2fa/', {
        current_password: disablePassword
      });
      onSuccess('2FA has been disabled for your account');
      onClose();
      resetModal();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to disable 2FA');
    } finally {
      setLoading(false);
    }
  };

  const copySecret = () => {
    navigator.clipboard.writeText(secret);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const resetModal = () => {
    setStep(1);
    setQrCode('');
    setSecret('');
    setVerificationCode('');
    setDisablePassword('');
    setError('');
    setCopied(false);
  };

  const handleClose = () => {
    onClose();
    resetModal();
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
        maxWidth: '600px',
        margin: '20px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', color: 'var(--text-dark)' }}>
            <Shield size={24} style={{ marginRight: '12px', color: 'var(--custom-blue)' }} />
            {is2FAEnabled ? 'Disable Two-Factor Authentication' : 'Enable Two-Factor Authentication'}
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

        {error && (
          <div className="alert alert-error" style={{ marginBottom: '20px' }}>
            {error}
          </div>
        )}

        {/* Step 1: Setup 2FA */}
        {step === 1 && !is2FAEnabled && (
          <div>
            <div style={{ textAlign: 'center', marginBottom: '24px' }}>
              <Smartphone size={48} style={{ color: 'var(--custom-blue)', marginBottom: '16px' }} />
              <h3 style={{ margin: '0 0 12px 0', color: 'var(--text-dark)' }}>Scan QR Code</h3>
              <p style={{ color: 'var(--medium-gray)', margin: 0 }}>
                Use your authenticator app (Google Authenticator, Authy, etc.) to scan this QR code
              </p>
            </div>

            {loading ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <div>Loading QR code...</div>
              </div>
            ) : qrCode && (
              <div>
                <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                  <img 
                    src={qrCode} 
                    alt="2FA QR Code" 
                    style={{ 
                      maxWidth: '200px', 
                      height: 'auto',
                      border: '2px solid var(--border-light)',
                      borderRadius: '8px'
                    }} 
                  />
                </div>

                <div style={{ 
                  backgroundColor: 'var(--background-light)', 
                  padding: '16px', 
                  borderRadius: '8px', 
                  marginBottom: '24px' 
                }}>
                  <h4 style={{ margin: '0 0 12px 0', display: 'flex', alignItems: 'center' }}>
                    <Key size={18} style={{ marginRight: '8px' }} />
                    Manual Entry Key
                  </h4>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <code style={{ 
                      flex: 1, 
                      padding: '8px 12px', 
                      backgroundColor: 'white', 
                      border: '1px solid var(--border-light)', 
                      borderRadius: '4px',
                      fontSize: '14px',
                      wordBreak: 'break-all'
                    }}>
                      {secret}
                    </code>
                    <button
                      onClick={copySecret}
                      className="btn btn-sm btn-secondary"
                      style={{ minWidth: '80px' }}
                    >
                      {copied ? <Check size={16} /> : <Copy size={16} />}
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                  <button
                    onClick={handleClose}
                    className="btn btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => setStep(2)}
                    className="btn btn-primary"
                  >
                    I've Added the Account
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Verify 2FA */}
        {step === 2 && (
          <div>
            <div style={{ textAlign: 'center', marginBottom: '24px' }}>
              <Shield size={48} style={{ color: 'var(--success-green)', marginBottom: '16px' }} />
              <h3 style={{ margin: '0 0 12px 0', color: 'var(--text-dark)' }}>Verify Setup</h3>
              <p style={{ color: 'var(--medium-gray)', margin: 0 }}>
                Enter the 6-digit code from your authenticator app to complete setup
              </p>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
                Verification Code
              </label>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '2px solid var(--border-light)',
                  borderRadius: '8px',
                  fontSize: '18px',
                  textAlign: 'center',
                  letterSpacing: '4px',
                  boxSizing: 'border-box'
                }}
                maxLength={6}
              />
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setStep(1)}
                className="btn btn-secondary"
                disabled={loading}
              >
                Back
              </button>
              <button
                onClick={verify2FA}
                className="btn btn-primary"
                disabled={loading || verificationCode.length !== 6}
              >
                {loading ? 'Verifying...' : 'Enable 2FA'}
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Disable 2FA */}
        {step === 3 && is2FAEnabled && (
          <div>
            <div style={{ textAlign: 'center', marginBottom: '24px' }}>
              <Shield size={48} style={{ color: 'var(--error-red)', marginBottom: '16px' }} />
              <h3 style={{ margin: '0 0 12px 0', color: 'var(--text-dark)' }}>Disable Two-Factor Authentication</h3>
              <p style={{ color: 'var(--medium-gray)', margin: 0 }}>
                Enter your password to disable 2FA. This will reduce your account security.
              </p>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
                Current Password
              </label>
              <input
                type="password"
                value={disablePassword}
                onChange={(e) => setDisablePassword(e.target.value)}
                placeholder="Enter your current password"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '2px solid var(--border-light)',
                  borderRadius: '8px',
                  fontSize: '16px',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            <div style={{ 
              backgroundColor: 'var(--error-light)', 
              padding: '16px', 
              borderRadius: '8px', 
              marginBottom: '24px',
              border: '1px solid var(--error-red)'
            }}>
              <p style={{ margin: 0, color: 'var(--error-red)', fontSize: '14px' }}>
                <strong>Warning:</strong> Disabling 2FA will make your account less secure. 
                You will only need your password to log in.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
              <button
                onClick={handleClose}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button
                onClick={disable2FA}
                className="btn btn-danger"
                disabled={loading || !disablePassword}
              >
                {loading ? 'Disabling...' : 'Disable 2FA'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TwoFactorModal;