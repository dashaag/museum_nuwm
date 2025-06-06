import { Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/layout/Navbar';
import HomePage from './pages/public/HomePage';
import AdminLoginPage from './pages/admin/AdminLoginPage';
import AdminDashboardPage from './pages/admin/AdminDashboardPage';
import { AdminCategoriesPage } from './pages/admin';
import NotFoundPage from './pages/NotFoundPage'; 
import { ProtectedRoute } from './components/routing'; 

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        
        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLoginPage />} />
        {/* Protected Admin Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
          <Route path="/admin/categories" element={<AdminCategoriesPage />} />
          {/* Add other protected admin routes here, e.g., /admin/pieces */}
        </Route>
        
        {/* Not Found Route */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  );
}

export default App;
