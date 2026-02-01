import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';
import { Users, Shield, CheckCircle, AlertCircle, Mail, Settings, Activity, Lock, Unlock, RefreshCw, Check, ArrowUp, ArrowDown } from 'lucide-react';
import axios from 'axios';

const AdminPanel = () => {
  const { isAdmin, user } = useAuth();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [recentUsers, setRecentUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [actionLoading, setActionLoading] = useState({});

  useEffect(() => {
    if (isAdmin) {
      fetchAdminData();
    }
  }, [isAdmin]);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [dashboardResponse, usersResponse] = await Promise.all([
        axios.get('/api/auth/admin/dashboard/'),
        axios.get('/api/auth/admin/users/')
      ]);
      
      setStats(dashboardResponse.data.stats);
      setRecentUsers(dashboardResponse.data.recent_users || []);
      setUsers(usersResponse.data.users || []);
      setError('');
    } catch (error) {
      setError('Failed to fetch admin data');
      console.error('Admin data error:', error);
    } finally {
      setLoading(false);
    }
  };

  const setUserActionLoading = (userId, action, loading) => {
    setActionLoading(prev => ({
      ...prev,
      [`${userId}-${action}`]: loading
    }));
  };

  const sendVerificationEmail = async (userId) => {
    setUserActionLoading(userId, 'email', true);
    try {
      await axios.post('/api/auth/admin/send-verification/', { user_id: userId });
      alert('Verification email sent successfully!');
    } catch (error) {
      alert('Failed to send verification email');
    } finally {
      setUserActionLoading(userId, 'email', false);
    }
  };

  const toggleUserStatus = async (userId) => {
    const targetUser = users.find(u => u.id === userId);
    if (!targetUser) return;

    const action = targetUser.is_active ? 'deactivate' : 'activate';
    const confirmMessage = `Are you sure you want to ${action} this user?\n\nThe user will receive an email notification.`;
    
    if (!confirm(confirmMessage)) return;

    setUserActionLoading(userId, 'toggle', true);
    try {
      const response = await axios.post('/api/auth/admin/toggle-user-status/', { user_id: userId });
      fetchAdminData(); // Refresh data
      alert(`${response.data.message || `User ${action}d successfully!`}\n\nEmail notification sent to user.`);
    } catch (error) {
      const errorMsg = error.response?.data?.error || `Failed to ${action} user`;
      alert(`Error: ${errorMsg}`);
      console.error('Toggle user status error:', error);
    } finally {
      setUserActionLoading(userId, 'toggle', false);
    }
  };

  const resetFailedAttempts = async (userId) => {
    setUserActionLoading(userId, 'reset', true);
    try {
      await axios.post('/api/auth/admin/reset-failed-attempts/', { user_id: userId });
      fetchAdminData(); // Refresh data
    } catch (error) {
      alert('Failed to reset failed attempts');
    } finally {
      setUserActionLoading(userId, 'reset', false);
    }
  };

  const changeUserRole = async (userId, newRole) => {
    if (userId === user?.id && newRole === 'user') {
      alert('You cannot demote yourself from admin!');
      return;
    }

    const confirmMessage = newRole === 'admin' 
      ? 'Are you sure you want to promote this user to admin?\n\nThe user will receive an email notification.' 
      : 'Are you sure you want to demote this admin to regular user?\n\nThe user will receive an email notification.';
    
    if (!confirm(confirmMessage)) return;

    setUserActionLoading(userId, 'role', true);
    try {
      const response = await axios.post('/api/auth/admin/change-user-role/', { 
        user_id: userId, 
        role: newRole 
      });
      fetchAdminData(); // Refresh data
      alert(`${response.data.message || `User role changed to ${newRole} successfully!`}\n\nEmail notification sent to user.`);
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to change user role';
      alert(`Error: ${errorMsg}`);
      console.error('Role change error:', error);
    } finally {
      setUserActionLoading(userId, 'role', false);
    }
  };

  const verifyUser = async (userId) => {
    if (!confirm('Are you sure you want to manually verify this user?')) return;

    setUserActionLoading(userId, 'verify', true);
    try {
      const response = await axios.post('/api/auth/admin/verify-user/', { user_id: userId });
      fetchAdminData(); // Refresh data
      alert(response.data.message || 'User verified successfully!');
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to verify user';
      alert(`Error: ${errorMsg}`);
      console.error('Verify user error:', error);
    } finally {
      setUserActionLoading(userId, 'verify', false);
    }
  };

  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading admin panel...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Admin Control Panel</h1>
      
      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={fetchAdminData} className="btn btn-sm" style={{ marginLeft: '12px' }}>
            <RefreshCw size={16} /> Retry
          </button>
        </div>
      )}

      {/* Admin Header */}
      <div className="dashboard-card">
        <h2 style={{ marginBottom: '16px', fontSize: '1.8rem' }}>
          <Shield size={28} style={{ marginRight: '12px' }} />
          Welcome, Administrator {user?.username}
        </h2>
        <p style={{ color: 'var(--medium-gray)', marginBottom: '20px' }}>
          Manage users, monitor system activity, and configure security settings.
        </p>
        
        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '12px', borderBottom: '2px solid var(--border-light)', paddingBottom: '12px' }}>
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-secondary'}`}
          >
            <Activity size={18} style={{ marginRight: '8px' }} />
            Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('users')}
            className={`btn ${activeTab === 'users' ? 'btn-primary' : 'btn-secondary'}`}
          >
            <Users size={18} style={{ marginRight: '8px' }} />
            User Management
          </button>
          <button 
            onClick={() => setActiveTab('system')}
            className={`btn ${activeTab === 'system' ? 'btn-primary' : 'btn-secondary'}`}
          >
            <Settings size={18} style={{ marginRight: '8px' }} />
            System Status
          </button>
        </div>
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && stats && (
        <>
          {/* Statistics Grid */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">
                <Users size={32} style={{ color: 'var(--custom-blue)' }} />
              </div>
              <div className="stat-label">Total Users</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--custom-blue)', marginTop: '8px' }}>
                {stats.total_users}
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                <CheckCircle size={32} style={{ color: 'var(--success-green)' }} />
              </div>
              <div className="stat-label">Verified Users</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--success-green)', marginTop: '8px' }}>
                {stats.verified_users}
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                <Shield size={32} style={{ color: 'var(--custom-orange)' }} />
              </div>
              <div className="stat-label">Admin Users</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--custom-orange)', marginTop: '8px' }}>
                {stats.admin_users}
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                <AlertCircle size={32} style={{ color: 'var(--error-red)' }} />
              </div>
              <div className="stat-label">Unverified</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--error-red)', marginTop: '8px' }}>
                {stats.unverified_users}
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                <Lock size={32} style={{ color: 'var(--warning-yellow)' }} />
              </div>
              <div className="stat-label">Inactive Users</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--warning-yellow)', marginTop: '8px' }}>
                {stats.inactive_users || 0}
              </div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                <AlertCircle size={32} style={{ color: 'var(--error-red)' }} />
              </div>
              <div className="stat-label">Locked Accounts</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--error-red)', marginTop: '8px' }}>
                {stats.locked_accounts || 0}
              </div>
            </div>
          </div>

          {/* Recent Users */}
          {recentUsers.length > 0 && (
            <div className="dashboard-card">
              <h3 style={{ marginBottom: '16px' }}>Recent Registrations</h3>
              <div style={{ display: 'grid', gap: '12px' }}>
                {recentUsers.map((user) => (
                  <div key={user.id} style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    padding: '12px',
                    background: 'var(--background-light)',
                    borderRadius: '8px'
                  }}>
                    <div>
                      <strong>{user.email}</strong>
                      <span style={{ color: 'var(--medium-gray)', marginLeft: '12px' }}>
                        {user.role === 'admin' ? 'Admin' : 'User'}
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span style={{ 
                        color: user.is_verified ? 'var(--success-green)' : 'var(--error-red)',
                        fontSize: '14px'
                      }}>
                        {user.is_verified ? 'Verified' : 'Unverified'}
                      </span>
                      <span style={{ color: 'var(--medium-gray)', fontSize: '14px' }}>
                        {new Date(user.date_joined).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="dashboard-card">
            <h3 style={{ marginBottom: '16px' }}>Quick Actions</h3>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <a href="/admin" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <Settings size={18} style={{ marginRight: '8px' }} />
                Django Admin
              </a>
              <button onClick={() => setActiveTab('users')} className="btn btn-edit">
                <Users size={18} style={{ marginRight: '8px' }} />
                Manage Users
              </button>
              <button onClick={fetchAdminData} className="btn btn-info">
                <RefreshCw size={18} style={{ marginRight: '8px' }} />
                Refresh Data
              </button>
            </div>
          </div>
        </>
      )}

      {/* Users Management Tab */}
      {activeTab === 'users' && (
        <div className="dashboard-card">
          <h3 style={{ marginBottom: '20px' }}>User Management ({users.length} users)</h3>
          
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border-light)' }}>
                  <th style={{ padding: '12px', textAlign: 'left', minWidth: '200px' }}>User</th>
                  <th style={{ padding: '12px', textAlign: 'center', minWidth: '150px' }}>Role</th>
                  <th style={{ padding: '12px', textAlign: 'center', minWidth: '120px' }}>Status</th>
                  <th style={{ padding: '12px', textAlign: 'center', minWidth: '100px' }}>Joined</th>
                  <th style={{ padding: '12px', textAlign: 'center', minWidth: '200px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((userData) => (
                  <tr key={userData.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '12px' }}>
                      <div>
                        <strong>{userData.email}</strong>
                        <div style={{ fontSize: '14px', color: 'var(--medium-gray)' }}>
                          @{userData.username}
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: '12px',
                          fontWeight: 'bold',
                          background: userData.role === 'admin' ? 'var(--error-red)' : 'var(--success-green)',
                          color: 'white'
                        }}>
                          {userData.role === 'admin' ? 'ADMIN' : 'USER'}
                        </span>
                        <button
                          onClick={() => changeUserRole(userData.id, userData.role === 'admin' ? 'user' : 'admin')}
                          disabled={actionLoading[`${userData.id}-role`]}
                          className={`btn btn-sm ${userData.role === 'admin' ? 'btn-warning' : 'btn-info'}`}
                          title={userData.role === 'admin' ? 'Demote to User' : 'Promote to Admin'}
                          style={{ minWidth: '80px', padding: '4px 8px', fontSize: '11px' }}
                        >
                          {actionLoading[`${userData.id}-role`] ? (
                            <RefreshCw size={12} className="spinning" />
                          ) : userData.role === 'admin' ? (
                            <>
                              <ArrowDown size={12} style={{ marginRight: '4px' }} />
                              Demote
                            </>
                          ) : (
                            <>
                              <ArrowUp size={12} style={{ marginRight: '4px' }} />
                              Promote
                            </>
                          )}
                        </button>
                      </div>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                        <span style={{ 
                          color: userData.is_verified ? 'var(--success-green)' : 'var(--error-red)',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}>
                          {userData.is_verified ? 'Verified' : 'Unverified'}
                        </span>
                        <span style={{ 
                          color: userData.is_active ? 'var(--success-green)' : 'var(--error-red)',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}>
                          {userData.is_active ? 'Active' : 'Inactive'}
                        </span>
                        {userData.is_locked && (
                          <span style={{ color: 'var(--error-red)', fontSize: '14px', fontWeight: '600' }}>
                            Locked
                          </span>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: '12px', fontSize: '14px', color: 'var(--medium-gray)', textAlign: 'center' }}>
                      {new Date(userData.date_joined).toLocaleDateString()}
                    </td>
                    <td style={{ padding: '12px' }}>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', justifyContent: 'center' }}>
                        {!userData.is_verified && (
                          <>
                            <button 
                              onClick={() => sendVerificationEmail(userData.id)}
                              disabled={actionLoading[`${userData.id}-email`]}
                              className="btn btn-sm btn-info"
                              title="Send verification email"
                            >
                              {actionLoading[`${userData.id}-email`] ? (
                                <RefreshCw size={12} className="spinning" />
                              ) : (
                                <Mail size={12} />
                              )}
                            </button>
                            <button 
                              onClick={() => verifyUser(userData.id)}
                              disabled={actionLoading[`${userData.id}-verify`]}
                              className="btn btn-sm btn-success"
                              title="Manually verify user"
                            >
                              {actionLoading[`${userData.id}-verify`] ? (
                                <RefreshCw size={12} className="spinning" />
                              ) : (
                                <Check size={12} />
                              )}
                            </button>
                          </>
                        )}
                        <button 
                          onClick={() => toggleUserStatus(userData.id)}
                          disabled={actionLoading[`${userData.id}-toggle`] || userData.id === user?.id}
                          className={`btn btn-sm ${userData.is_active ? 'btn-danger' : 'btn-success'}`}
                          title={userData.id === user?.id ? 'Cannot deactivate yourself' : (userData.is_active ? 'Deactivate user' : 'Activate user')}
                        >
                          {actionLoading[`${userData.id}-toggle`] ? (
                            <RefreshCw size={12} className="spinning" />
                          ) : userData.is_active ? (
                            <Lock size={12} />
                          ) : (
                            <Unlock size={12} />
                          )}
                        </button>
                        {userData.failed_login_attempts > 0 && (
                          <button 
                            onClick={() => resetFailedAttempts(userData.id)}
                            disabled={actionLoading[`${userData.id}-reset`]}
                            className="btn btn-sm btn-warning"
                            title="Reset failed login attempts"
                          >
                            {actionLoading[`${userData.id}-reset`] ? (
                              <RefreshCw size={12} className="spinning" />
                            ) : (
                              <RefreshCw size={12} />
                            )}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* System Status Tab */}
      {activeTab === 'system' && stats && (
        <div className="dashboard-card">
          <h3 style={{ marginBottom: '16px' }}>System Status</h3>
          <div style={{ display: 'grid', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Authentication System</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Online</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>JWT Token Service</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Active</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Database Connection</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Connected</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Email Service</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>SMTP Active</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>Account Locking</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Enabled</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>CORS Configuration</span>
              <span style={{ color: 'var(--success-green)', fontWeight: '600' }}>Configured</span>
            </div>
            
            {/* System Statistics */}
            <div style={{ marginTop: '20px', padding: '16px', background: 'var(--background-light)', borderRadius: '8px' }}>
              <h4 style={{ marginBottom: '12px' }}>System Statistics</h4>
              <div style={{ display: 'grid', gap: '8px', fontSize: '14px' }}>
                <div>Total Users: <strong>{stats.total_users}</strong></div>
                <div>Verified: <strong>{stats.verified_users}</strong></div>
                <div>Unverified: <strong>{stats.unverified_users}</strong></div>
                <div>Admins: <strong>{stats.admin_users}</strong></div>
                <div>Inactive Users: <strong>{stats.inactive_users || 0}</strong> <span style={{ color: 'var(--medium-gray)', fontSize: '12px' }}>(Admin deactivated)</span></div>
                <div>Locked Accounts: <strong>{stats.locked_accounts || 0}</strong> <span style={{ color: 'var(--medium-gray)', fontSize: '12px' }}>(Failed login attempts)</span></div>
                <div>Recent Registrations (7 days): <strong>{stats.recent_registrations || 0}</strong></div>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default AdminPanel;