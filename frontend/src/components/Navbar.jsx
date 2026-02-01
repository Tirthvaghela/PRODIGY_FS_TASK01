import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, Shield } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // Hide login/register buttons on auth pages
  const isAuthPage = ['/login', '/register', '/reset-password', '/verify-email', '/2fa-verification'].some(path => 
    location.pathname.startsWith(path)
  );

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Prodigy Auth
        </Link>
      </div>
      <div className="nav-links">
        {isAuthenticated && !location.pathname.startsWith('/2fa-verification') ? (
          <>
            <Link to="/dashboard" className="btn btn-secondary">
              Dashboard
            </Link>
            {isAdmin && (
              <Link to="/admin" className="btn btn-edit">
                <Shield size={18} />
                Admin
              </Link>
            )}
            <span>
              <User size={16} style={{ marginRight: '8px' }} />
              {user?.email}
              {user?.role === 'admin' && (
                <span style={{ 
                  marginLeft: '8px', 
                  padding: '2px 8px', 
                  background: '#f59e0b', 
                  color: 'white', 
                  borderRadius: '4px', 
                  fontSize: '12px' 
                }}>
                  ADMIN
                </span>
              )}
            </span>
            <button onClick={handleLogout} className="btn btn-danger">
              <LogOut size={18} />
              Logout
            </button>
          </>
        ) : isAuthenticated && location.pathname.startsWith('/2fa-verification') ? (
          // Show only user info and logout on 2FA page
          <>
            <span>
              <User size={16} style={{ marginRight: '8px' }} />
              {user?.email}
              {user?.role === 'admin' && (
                <span style={{ 
                  marginLeft: '8px', 
                  padding: '2px 8px', 
                  background: '#f59e0b', 
                  color: 'white', 
                  borderRadius: '4px', 
                  fontSize: '12px' 
                }}>
                  ADMIN
                </span>
              )}
            </span>
            <button onClick={handleLogout} className="btn btn-danger">
              <LogOut size={18} />
              Logout
            </button>
          </>
        ) : (
          !isAuthPage && (
            <>
              <Link to="/login" className="btn btn-primary">Login</Link>
              <Link to="/register" className="btn btn-info">Register</Link>
            </>
          )
        )}
      </div>
    </nav>
  );
};

export default Navbar;