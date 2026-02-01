import { useAuth } from '../context/AuthContext';
import { User, Mail, Calendar, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const Dashboard = () => {
  const { user, isAdmin, isVerified, resendVerification } = useAuth();

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const handleResendVerification = async () => {
    if (user?.email) {
      const result = await resendVerification(user.email);
      if (result.success) {
        alert('Verification email sent! Please check your inbox.');
      } else {
        alert('Failed to send verification email: ' + result.error);
      }
    }
  };

  return (
    <div className="container">
      <h1>Dashboard</h1>
      
      <div className="dashboard-card">
        <h2 style={{ marginBottom: '24px', fontSize: '1.8rem' }}>
          Welcome back, {user?.username}!
        </h2>
        
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">
              <User size={32} style={{ color: 'var(--custom-blue)' }} />
            </div>
            <div className="stat-label">Profile</div>
            <p style={{ marginTop: '12px', color: 'var(--medium-gray)' }}>
              {user?.username}
            </p>
          </div>
          
          <div className="stat-card">
            <div className="stat-number">
              <Mail size={32} style={{ color: isVerified ? 'var(--success-green)' : 'var(--error-red)' }} />
            </div>
            <div className="stat-label">Email</div>
            <p style={{ marginTop: '12px', color: 'var(--medium-gray)' }}>
              {user?.email}
            </p>
            {isVerified ? (
              <span style={{ 
                fontSize: '12px', 
                color: 'var(--success-green)', 
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginTop: '8px'
              }}>
                <CheckCircle size={14} style={{ marginRight: '4px' }} />
                Verified
              </span>
            ) : (
              <span style={{ 
                fontSize: '12px', 
                color: 'var(--error-red)', 
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginTop: '8px'
              }}>
                <AlertTriangle size={14} style={{ marginRight: '4px' }} />
                Unverified
              </span>
            )}
          </div>
          
          <div className="stat-card">
            <div className="stat-number">
              <Shield size={32} style={{ color: 'var(--custom-orange)' }} />
            </div>
            <div className="stat-label">Role</div>
            <p style={{ marginTop: '12px', color: 'var(--medium-gray)' }}>
              {user?.role?.toUpperCase()}
            </p>
          </div>
          
          <div className="stat-card">
            <div className="stat-number">
              <Calendar size={32} style={{ color: 'var(--primary-blue)' }} />
            </div>
            <div className="stat-label">Member Since</div>
            <p style={{ marginTop: '12px', color: 'var(--medium-gray)' }}>
              {user?.date_joined ? formatDate(user.date_joined) : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Email Verification Status */}
      {isVerified ? (
        <div className="alert alert-success">
          <CheckCircle size={20} style={{ marginRight: '8px' }} />
          <strong>✓ Verified Account</strong> - Your email has been verified and your account is fully active.
        </div>
      ) : (
        <div className="dashboard-card" style={{ border: '2px solid var(--error-red)' }}>
          <h3 style={{ color: 'var(--error-red)', marginBottom: '16px', display: 'flex', alignItems: 'center' }}>
            <AlertTriangle size={24} style={{ marginRight: '8px' }} />
            Email Verification Required
          </h3>
          <p style={{ color: 'var(--medium-gray)', marginBottom: '24px' }}>
            Your account is not yet verified. Please check your email for a verification link, or request a new one below.
          </p>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button onClick={handleResendVerification} className="btn btn-primary">
              <Mail size={18} style={{ marginRight: '8px' }} />
              Resend Verification Email
            </button>
          </div>
        </div>
      )}

      {isAdmin && (
        <div className="dashboard-card">
          <h3 style={{ color: 'var(--custom-orange)', marginBottom: '16px' }}>
            <Shield size={24} style={{ marginRight: '8px' }} />
            Admin Access
          </h3>
          <p style={{ color: 'var(--medium-gray)', marginBottom: '24px' }}>
            You have administrator privileges. Access the admin panel for advanced features and user management.
          </p>
          <a href="/admin" className="btn btn-edit">
            Go to Admin Panel
          </a>
        </div>
      )}

      <div className="dashboard-card">
        <h3 style={{ marginBottom: '16px' }}>Account Security</h3>
        <p style={{ color: 'var(--medium-gray)', marginBottom: '24px' }}>
          Your account is secured with JWT authentication, password hashing, and email verification.
        </p>
        <div style={{ display: 'grid', gap: '16px', marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>JWT Authentication</span>
            <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>✓ Active</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Password Encryption</span>
            <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>✓ PBKDF2</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Email Verification</span>
            <span style={{ color: isVerified ? 'var(--success-green)' : 'var(--error-red)', fontWeight: '600' }}>
              {isVerified ? '✓ Verified' : '⚠ Pending'}
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Account Locking</span>
            <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Enabled</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;