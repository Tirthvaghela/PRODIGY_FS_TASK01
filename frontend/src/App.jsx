import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import EmailVerification from './pages/EmailVerification';
import EmailViewer from './pages/EmailViewer';
import ApiTest from './pages/ApiTest';
import TwoFactorVerification from './pages/TwoFactorVerification';
import PasswordReset from './pages/PasswordReset';

function AppContent() {
  const { user, loading, is2FAVerified } = useAuth();
  
  if (loading) {
    return <div className="loading">Initializing Prodigy Auth...</div>;
  }

  // Helper function to check if user needs 2FA verification
  const needs2FAVerification = user && !is2FAVerified;

  return (
    <>
      <Navbar />
      <Routes>
        <Route 
          path="/login" 
          element={user ? (needs2FAVerification ? <Navigate to="/2fa-verification" replace /> : <Navigate to="/dashboard" replace />) : <Login />} 
        />
        <Route 
          path="/register" 
          element={user ? (needs2FAVerification ? <Navigate to="/2fa-verification" replace /> : <Navigate to="/dashboard" replace />) : <Register />} 
        />
        <Route 
          path="/verify-email/:token" 
          element={<EmailVerification />} 
        />
        <Route 
          path="/reset-password/:token" 
          element={<PasswordReset />} 
        />
        <Route 
          path="/2fa-verification" 
          element={user ? <TwoFactorVerification /> : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/emails" 
          element={<EmailViewer />} 
        />
        <Route 
          path="/test" 
          element={<ApiTest />} 
        />
        <Route 
          path="/dashboard" 
          element={user ? (needs2FAVerification ? <Navigate to="/2fa-verification" replace /> : <Dashboard />) : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/admin" 
          element={user ? (needs2FAVerification ? <Navigate to="/2fa-verification" replace /> : <AdminPanel />) : <Navigate to="/login" replace />} 
        />
        <Route 
          path="/" 
          element={<Navigate to={user ? (needs2FAVerification ? "/2fa-verification" : "/dashboard") : "/login"} replace />} 
        />
      </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true
        }}
      >
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;