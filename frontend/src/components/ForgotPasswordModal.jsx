import { useState } from 'react';
import { X, Mail, Send } from 'lucide-react';
import axios from 'axios';

const ForgotPasswordModal = ({ isOpen, onClose, onSuccess }) => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/forgot-password/', { email });
      onSuccess(response.data.message);
      onClose();
      setEmail('');
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to send reset email');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    onClose();
    setEmail('');
    setError('');
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
            Forgot Password
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

        <p style={{ color: 'var(--medium-gray)', marginBottom: '24px', lineHeight: '1.6' }}>
          Enter your email address and we'll send you a link to reset your password.
        </p>

        {error && (
          <div className="alert alert-error" style={{ marginBottom: '20px' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '24px' }}>
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
            />
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={handleClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !email}
            >
              {loading ? (
                'Sending...'
              ) : (
                <>
                  <Send size={18} style={{ marginRight: '8px' }} />
                  Send Reset Link
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordModal;