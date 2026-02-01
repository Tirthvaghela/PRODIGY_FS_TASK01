import { useState, useEffect } from 'react';
import { Mail, RefreshCw, ExternalLink } from 'lucide-react';

const EmailViewer = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);

  const mockEmails = [
    {
      id: 1,
      subject: 'Verify Your Prodigy Auth Account',
      to: 'user@example.com',
      date: new Date().toISOString(),
      content: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <div style="background: linear-gradient(135deg, #4979fe 0%, #f7931e 100%); padding: 20px; text-align: center;">
            <h1 style="color: white; margin: 0;">Prodigy Auth</h1>
          </div>
          <div style="padding: 30px; background: #f9f9f9;">
            <h2 style="color: #333;">Welcome!</h2>
            <p style="color: #666; line-height: 1.6;">
              Thank you for registering with Prodigy Auth. Please verify your email address to activate your account.
            </p>
            <div style="text-align: center; margin: 30px 0;">
              <a href="http://localhost:5173/verify-email/sample-token/" 
                 style="background: #4979fe; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
                Verify Email Address
              </a>
            </div>
            <p style="color: #999; font-size: 14px;">
              If the button doesn't work, copy and paste this link: http://localhost:5173/verify-email/sample-token/
            </p>
            <p style="color: #999; font-size: 14px;">
              This link will expire in 24 hours.
            </p>
          </div>
        </div>
      `
    }
  ];

  useEffect(() => {
    setEmails(mockEmails);
  }, []);

  const refreshEmails = () => {
    setLoading(true);
    setTimeout(() => {
      setEmails(mockEmails);
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="container">
      <h1>Development Email Viewer</h1>
      
      <div className="dashboard-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <h2 style={{ margin: 0 }}>
            <Mail size={24} style={{ marginRight: '8px' }} />
            Sent Emails
          </h2>
          <button onClick={refreshEmails} className="btn btn-secondary" disabled={loading}>
            <RefreshCw size={18} style={{ marginRight: '8px' }} />
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>

        <div className="alert alert-success">
          <strong>Development Mode:</strong> Emails are displayed here instead of being sent to real email addresses.
          Check the Django server console for the actual verification links.
        </div>

        {emails.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--medium-gray)' }}>
            <Mail size={48} style={{ marginBottom: '16px' }} />
            <p>No emails sent yet. Register a new user to see verification emails here.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '16px' }}>
            {emails.map((email) => (
              <div key={email.id} className="dashboard-card" style={{ margin: 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                  <div>
                    <h3 style={{ margin: 0, marginBottom: '8px' }}>{email.subject}</h3>
                    <p style={{ color: 'var(--medium-gray)', margin: 0, fontSize: '14px' }}>
                      To: {email.to} • {new Date(email.date).toLocaleString()}
                    </p>
                  </div>
                  <ExternalLink size={20} style={{ color: 'var(--custom-blue)' }} />
                </div>
                
                <div 
                  style={{ 
                    border: '1px solid var(--border-light)', 
                    borderRadius: '8px', 
                    padding: '16px',
                    background: 'var(--pure-white)',
                    maxHeight: '300px',
                    overflow: 'auto'
                  }}
                  dangerouslySetInnerHTML={{ __html: email.content }}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-card">
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button 
            onClick={() => window.open('http://localhost:5173/verify-email/70215126-e590-4cb6-b7a8-814bf443f690/', '_blank')}
            className="btn btn-primary"
          >
            Test Verification Link
          </button>
          <button 
            onClick={() => window.location.href = '/register'}
            className="btn btn-info"
          >
            Register New User
          </button>
          <button 
            onClick={() => window.location.href = '/login'}
            className="btn btn-secondary"
          >
            Go to Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmailViewer;