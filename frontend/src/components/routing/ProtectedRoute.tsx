import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    // You might want to render a loading spinner or a blank page while checking auth status
    return <div>Loading...</div>; 
  }

  if (!isAuthenticated) {
    // Redirect them to the /admin/login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the homepage.
    return <Navigate to="/admin/login" replace />;
  }

  return <Outlet />; // Render the child route's element
};

export default ProtectedRoute;
