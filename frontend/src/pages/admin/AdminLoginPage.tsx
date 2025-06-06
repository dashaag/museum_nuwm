import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiClient from '../../config/api';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';
import { isAxiosError } from 'axios'; // Import isAxiosError
import './AdminLoginPage.css'; // Import the new CSS file

const AdminLoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [email, setEmail] = useState<string>('admin@museum.com');
  const [password, setPassword] = useState<string>('Admin123!');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      const response = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      authLogin(response.data.access_token);
      toast.success('Login successful!');
      navigate('/admin/dashboard');
    } catch (error: unknown) {
      console.error('Login failed:', error);
      let errorMessage = 'Login failed. Please check your credentials.';

      if (isAxiosError(error)) {
        if (error.response && error.response.data && error.response.data.detail) {
          // Assuming 'detail' is the field your backend sends for specific error messages
          errorMessage = error.response.data.detail;
        } else if (error.message) {
          // Fallback to generic Axios error message if no specific detail
          errorMessage = `Login failed: ${error.message}`;
        }
      } else if (error instanceof Error) {
        // Handle other types of errors that have a message property
        errorMessage = `Login failed: ${error.message}`;
      }
      // If it's not an Axios error or a standard Error, the generic message will be used.
      toast.error(errorMessage);
    }
    setIsLoading(false);
  };

  return (
    <div className="admin-login-page">
      <div className="login-container">
        <h1>Admin Login</h1>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="e.g., admin@museum.com"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>
          <button type="submit" className="button" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <Link to="/" className="back-link">
          &larr; Back to Public Site
        </Link>
      </div>
    </div>
  );
};

export default AdminLoginPage;
