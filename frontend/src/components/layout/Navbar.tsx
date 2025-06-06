import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // We'll create this for basic styling

import { useAuth } from '../../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
    // Navigation to login page will be handled by ProtectedRoute or redirect in AuthContext if desired
    // For now, direct navigation or relying on AuthContext's effect is fine.
    // window.location.href = '/admin/login'; // Can be removed if logout in AuthContext handles redirection or if ProtectedRoute handles it
  };
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" className="navbar-item">Museum App</Link>
      </div>
      <div className="navbar-menu">
        <div className="navbar-start">
          <Link to="/" className="navbar-item">Home</Link>
          {/* Add other public links here if needed */}
        </div>
        <div className="navbar-end">
          {isAuthenticated ? (
            <>
              <Link to="/admin/dashboard" className="navbar-item">Dashboard</Link>
              <button onClick={handleLogout} className="navbar-item button is-light">Logout</button>
            </>
          ) : (
            <Link to="/admin/login" className="navbar-item">Admin Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
