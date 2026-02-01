import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = false;

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Axios interceptor for token refresh
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return axios(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh');
      
      if (refreshToken) {
        try {
          const response = await axios.post('/api/token/refresh/', {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('access', access);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          
          processQueue(null, access);
          
          return axios(originalRequest);
        } catch (refreshError) {
          processQueue(refreshError, null);
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          delete axios.defaults.headers.common['Authorization'];
          window.location.href = '/login';
        }
      }
      
      isRefreshing = false;
    }
    
    return Promise.reject(error);
  }
);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [is2FAVerified, setIs2FAVerified] = useState(false);

  // Set up axios defaults
  useEffect(() => {
    const token = localStorage.getItem('access');
    const twoFAVerified = sessionStorage.getItem('2fa_verified') === 'true';
    setIs2FAVerified(twoFAVerified);
    
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Verify token and get user info
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get('/api/auth/profile/');
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      console.log('Attempting login with:', email);
      const response = await axios.post('/api/auth/login/', { email, password });
      console.log('Login response:', response.data);
      
      const { access, refresh, user: userData } = response.data;
      
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(userData);
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      console.error('Error response:', error.response?.data);
      
      const message = error.response?.data?.detail || 
                     error.response?.data?.non_field_errors?.[0] ||
                     'Login failed';
      return { success: false, error: message };
    }
  };

  const register = async (userData) => {
    try {
      console.log('Attempting registration with:', userData.email);
      const response = await axios.post('/api/auth/register/', userData);
      console.log('Registration response:', response.data);
      
      const { tokens, user: newUser, verification_required } = response.data;
      
      if (tokens && tokens.access && tokens.refresh) {
        localStorage.setItem('access', tokens.access);
        localStorage.setItem('refresh', tokens.refresh);
        axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`;
        setUser(newUser);
      }
      
      return { 
        success: true, 
        verification_required,
        message: response.data.message 
      };
    } catch (error) {
      console.error('Registration error:', error);
      console.error('Error response:', error.response?.data);
      
      const message = error.response?.data?.email?.[0] || 
                     error.response?.data?.username?.[0] ||
                     error.response?.data?.password?.[0] || 
                     error.response?.data?.non_field_errors?.[0] ||
                     'Registration failed';
      return { success: false, error: message };
    }
  };

  const verifyEmail = async (token) => {
    try {
      console.log('Verifying email with token:', token);
      const response = await axios.post('/api/auth/verify-email/', { token });
      console.log('Verification response:', response.data);
      
      const { access, refresh, user: userData } = response.data;
      
      if (access && refresh) {
        localStorage.setItem('access', access);
        localStorage.setItem('refresh', refresh);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        setUser(userData);
      }
      
      return { success: true, message: response.data.message };
    } catch (error) {
      console.error('Email verification error:', error);
      console.error('Error response:', error.response?.data);
      
      const message = error.response?.data?.error ||
                     error.response?.data?.token?.[0] || 
                     error.response?.data?.non_field_errors?.[0] ||
                     'Email verification failed';
      return { success: false, error: message };
    }
  };

  const resendVerification = async (email) => {
    try {
      const response = await axios.post('/api/auth/resend-verification/', { email });
      return { success: true, message: response.data.message };
    } catch (error) {
      const message = error.response?.data?.email?.[0] || 
                     error.response?.data?.non_field_errors?.[0] ||
                     'Failed to resend verification email';
      return { success: false, error: message };
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh');
      if (refreshToken) {
        await axios.post('/api/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      sessionStorage.removeItem('2fa_verified'); // Clear 2FA verification status
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      setIs2FAVerified(false);
    }
  };

  const mark2FAVerified = () => {
    sessionStorage.setItem('2fa_verified', 'true');
    setIs2FAVerified(true);
  };

  const clear2FAVerification = () => {
    sessionStorage.removeItem('2fa_verified');
    setIs2FAVerified(false);
  };

  const value = {
    user,
    login,
    register,
    logout,
    verifyEmail,
    resendVerification,
    loading,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    isVerified: user?.is_verified || false,
    is2FAVerified,
    mark2FAVerified,
    clear2FAVerification
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};