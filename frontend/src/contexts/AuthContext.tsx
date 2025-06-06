import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import apiClient from '../config/api'; // Assuming apiClient is set up for token injection

interface User {
  email?: string;
  // Add other user-related fields if needed, e.g., id, roles
}

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true); // Start with loading true
  const [user, setUser] = useState<User | null>(null);

  const login = (token: string) => {
    localStorage.setItem('authToken', token);
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      setUser({ email: payload.email }); // Assuming email is in the token payload
    } catch (e) {
      console.error('Failed to parse token or extract user info:', e);
      setUser(null);
    }
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    delete apiClient.defaults.headers.common['Authorization'];
    setIsAuthenticated(false);
    setUser(null);
  };

  const checkAuthStatus = async () => {
    setIsLoading(true);
    const token = localStorage.getItem('authToken');
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUser({ email: payload.email }); // Assuming email is in the token payload
      } catch (e) {
        console.error('Failed to parse token or extract user info during checkAuthStatus:', e);
        setUser(null); // Clear user if token is invalid or doesn't contain expected info
      }
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
      setUser(null);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, user, login, logout, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
