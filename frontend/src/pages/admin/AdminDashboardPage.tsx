import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';
import './AdminDashboardPage.css'; // Import the new CSS

const AdminDashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { logout: authLogout, user } = useAuth();

  const handleLogout = () => {
    authLogout();
    toast.info('Logged out successfully!');
    navigate('/admin/login');
  };

  return (
    // Added admin-dashboard-page class to the main container
    <div className="container section admin-dashboard-page">
      <div className="level">
        <div className="level-left">
          <div className="level-item">
            <h1 className="title">Admin Dashboard</h1>
          </div>
        </div>
        <div className="level-right">
          <div className="level-item">
            {/* Bulma classes are fine, custom CSS will target them */}
            <button onClick={handleLogout} className="button is-danger is-light">
              <span className="icon is-small"><i className="fas fa-sign-out-alt"></i></span>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
      
      <p className="subtitle">
        Welcome, {user?.email ? user.email : 'Admin'}! Manage your museum's content from here.
      </p>

      <div className="columns is-multiline mt-4">
        <div className="column is-one-third">
          {/* Replaced .box with .dashboard-card */}
          <div className="dashboard-card has-text-centered">
            <div> {/* Added a div to group content above button */}
              <span className="icon is-large has-text-info">
                <i className="fas fa-tags fa-3x"></i>
              </span>
              <h2 className="title is-4 mt-3">Categories</h2>
              <p className="mb-3">Organize art pieces by categories.</p>
            </div>
            <Link to="/admin/categories" className="button is-info is-fullwidth">
              Manage Categories
            </Link>
          </div>
        </div>

        <div className="column is-one-third">
          {/* Replaced .box with .dashboard-card */}
          <div className="dashboard-card has-text-centered">
            <div> {/* Added a div to group content above button */}
              <span className="icon is-large has-text-primary">
                <i className="fas fa-palette fa-3x"></i>
              </span>
              <h2 className="title is-4 mt-3">Art Pieces</h2>
              <p className="mb-3">Add, update, or remove art pieces.</p>
            </div>
            {/* Button styling will be handled by .dashboard-card .button.is-primary */}
            <button className="button is-primary is-fullwidth" disabled>
              Manage Art Pieces (Soon)
            </button>
          </div>
        </div>
        
        {/* Add more management sections as needed */}
        {/* Example:
        <div className="column is-one-third">
          <div className="dashboard-card has-text-centered">
            <div>
              <span className="icon is-large has-text-success">
                <i className="fas fa-users fa-3x"></i>
              </span>
              <h2 className="title is-4 mt-3">Users</h2>
              <p className="mb-3">Manage administrator accounts.</p>
            </div>
            <button className="button is-success is-fullwidth" disabled>
              Manage Users (Soon)
            </button>
          </div>
        </div>
        */}
      </div>

      <hr />
      {/* Button styling will be handled by .admin-dashboard-page .button.is-link */}
      <Link to="/" className="button is-link">
        <span className="icon is-small"><i className="fas fa-eye"></i></span>
        <span>View Public Site</span>
      </Link>
    </div>
  );
};

export default AdminDashboardPage;
