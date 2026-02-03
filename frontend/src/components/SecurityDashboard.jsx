import { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Clock, Mail, CheckCircle } from 'lucide-react';
import axios from 'axios';

const SecurityDashboard = () => {
  const [securityInfo, setSecurityInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportSuccess, setReportSuccess] = useState(false);

  useEffect(() => {
    fetchSecurityInfo();
  }, []);

  const fetchSecurityInfo = async () => {
    try {
      const response = await axios.get('/api/auth/password-reset-activity/');
      setSecurityInfo(response.data);
    } catch (error) {
      console.error('Failed to fetch security info:', error);
    } finally {
      setLoading(false);
    }
  };

  const reportSuspiciousActivity = async () => {
    setReportLoading(true);
    try {
      const response = await axios.post('/api/auth/report-suspicious-reset/', {
        details: 'User reported unexpected password reset emails'
      });
      setReportSuccess(true);
      setTimeout(() => setReportSuccess(false), 5000);
    } catch (error) {
      console.error('Failed to report suspicious activity:', error);
    } finally {
      setReportLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div>Loading security information...</div>
      </div>
    );
  }

  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      maxWidth: '600px',
      margin: '20px auto'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '24px' }}>
        <Shield size={24} style={{ marginRight: '12px', color: 'var(--custom-blue)' }} />
        <h2 style={{ margin: 0, color: 'var(--text-dark)' }}>Account Security</h2>
      </div>

      {/* Security Status */}
      <div style={{
        backgroundColor: '#f0f9ff',
        border: '1px solid #bae6fd',
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '20px'
      }}>
        <h3 style={{ margin: '0 0 12px 0', color: '#0369a1', display: 'flex', alignItems: 'center' }}>
          <CheckCircle size={18} style={{ marginRight: '8px' }} />
          Password Reset Protection Active
        </h3>
        <div style={{ fontSize: '14px', color: '#0369a1', lineHeight: '1.5' }}>
          Your account is protected against password reset abuse with multiple security layers.
        </div>
      </div>

      {/* Current Status */}
      <div style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '16px', color: 'var(--text-dark)' }}>Current Status</h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div style={{
            backgroundColor: securityInfo?.has_recent_reset ? '#fef3c7' : '#f0fdf4',
            border: `1px solid ${securityInfo?.has_recent_reset ? '#fcd34d' : '#bbf7d0'}`,
            borderRadius: '8px',
            padding: '12px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
              <Clock size={16} style={{ 
                marginRight: '8px', 
                color: securityInfo?.has_recent_reset ? '#d97706' : '#16a34a' 
              }} />
              <span style={{ 
                fontSize: '14px', 
                fontWeight: '600',
                color: securityInfo?.has_recent_reset ? '#d97706' : '#16a34a'
              }}>
                Recent Reset
              </span>
            </div>
            <div style={{ fontSize: '12px', color: '#6b7280' }}>
              {securityInfo?.has_recent_reset ? 'Active cooldown period' : 'No recent requests'}
            </div>
          </div>

          <div style={{
            backgroundColor: securityInfo?.email_attempts_today > 0 ? '#fef3c7' : '#f0fdf4',
            border: `1px solid ${securityInfo?.email_attempts_today > 0 ? '#fcd34d' : '#bbf7d0'}`,
            borderRadius: '8px',
            padding: '12px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '4px' }}>
              <Mail size={16} style={{ 
                marginRight: '8px', 
                color: securityInfo?.email_attempts_today > 0 ? '#d97706' : '#16a34a' 
              }} />
              <span style={{ 
                fontSize: '14px', 
                fontWeight: '600',
                color: securityInfo?.email_attempts_today > 0 ? '#d97706' : '#16a34a'
              }}>
                Attempts Today
              </span>
            </div>
            <div style={{ fontSize: '12px', color: '#6b7280' }}>
              {securityInfo?.email_attempts_today || 0} / {securityInfo?.max_attempts_per_hour || 2} per hour
            </div>
          </div>
        </div>
      </div>

      {/* Security Features */}
      <div style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '16px', color: 'var(--text-dark)' }}>Protection Features</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {securityInfo?.security_info && Object.entries(securityInfo.security_info).map(([key, value]) => (
            <div key={key} style={{
              display: 'flex',
              alignItems: 'center',
              padding: '8px 12px',
              backgroundColor: '#f9fafb',
              borderRadius: '6px',
              border: '1px solid #e5e7eb'
            }}>
              <CheckCircle size={16} style={{ marginRight: '12px', color: '#16a34a' }} />
              <div>
                <div style={{ fontSize: '14px', fontWeight: '500', color: 'var(--text-dark)' }}>
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
                <div style={{ fontSize: '12px', color: '#6b7280' }}>
                  {value}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Report Suspicious Activity */}
      <div style={{
        backgroundColor: '#fef2f2',
        border: '1px solid #fecaca',
        borderRadius: '8px',
        padding: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
          <AlertTriangle size={18} style={{ marginRight: '8px', color: '#dc2626' }} />
          <h4 style={{ margin: 0, color: '#dc2626' }}>Received Unexpected Reset Emails?</h4>
        </div>
        
        <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '12px', lineHeight: '1.5' }}>
          If you received password reset emails that you didn't request, someone might be trying to access your account. 
          Report this to enhance your account security.
        </p>
        
        {reportSuccess ? (
          <div style={{
            backgroundColor: '#d1fae5',
            border: '1px solid #a7f3d0',
            borderRadius: '6px',
            padding: '8px 12px',
            display: 'flex',
            alignItems: 'center',
            color: '#065f46'
          }}>
            <CheckCircle size={16} style={{ marginRight: '8px' }} />
            <span style={{ fontSize: '14px' }}>
              Thank you for reporting. Enhanced security is now active for 24 hours.
            </span>
          </div>
        ) : (
          <button
            onClick={reportSuspiciousActivity}
            disabled={reportLoading}
            style={{
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              padding: '8px 16px',
              fontSize: '14px',
              cursor: reportLoading ? 'not-allowed' : 'pointer',
              opacity: reportLoading ? 0.6 : 1
            }}
          >
            {reportLoading ? 'Reporting...' : 'Report Suspicious Activity'}
          </button>
        )}
      </div>
    </div>
  );
};

export default SecurityDashboard;