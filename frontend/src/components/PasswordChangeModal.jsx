import { useState } from 'react';
import { X, Eye, EyeOff, Lock } from 'lucide-react';
import axios from 'axios';

const PasswordChangeModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      await axios.post('/api/auth/change-password/', formData);
      onSuccess('Password changed successfully!');
      onClose();
      setFormData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to change password');
    } finally {
      setLoading(false);
    }
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
            <Lock size={24} style={{ marginRight: '12px', color: 'var(--custom-blue)' }} />
            Change Password
          </h2>
          <button
            onClick={onClose}
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

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
              Current Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPasswords.current ? 'text' : 'password'}
                name="current_password"
                value={formData.current_password}
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
                placeholder="Enter your current password"
              />
              <button
                type="button"
                onClick={() => togglePasswordVisibility('current')}
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
                {showPasswords.current ? <EyeOff size={20} color="var(--medium-gray)" /> : <Eye size={20} color="var(--medium-gray)" />}
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
              New Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPasswords.new ? 'text' : 'password'}
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

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: 'var(--text-dark)' }}>
              Confirm New Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPasswords.confirm ? 'text' : 'password'}
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

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Changing...' : 'Change Password'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PasswordChangeModal;