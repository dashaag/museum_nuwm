// frontend/src/pages/admin/categories/AdminCategoriesPage.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import apiClient from '../../../config/api';
import CategoryForm from '../../../components/admin/CategoryForm'; // Adjusted path
import './AdminCategoriesPage.css'; // To be created

interface Category {
  id: number;
  name: string;
  description?: string;
}

const AdminCategoriesPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  const fetchCategories = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<Category[]>('/categories/');
      setCategories(response.data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
      const errorMessage = apiClient.isAxiosError(err) && err.response?.data?.detail 
        ? err.response.data.detail 
        : 'Failed to load categories.';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const handleCategoryCreated = (newCategory: Category) => {
    setCategories(prev => [...prev, newCategory].sort((a, b) => a.name.localeCompare(b.name)));
    setShowForm(false);
  };

  const handleCategoryUpdated = (updatedCategory: Category) => {
    setCategories(prev => 
      prev.map(cat => (cat.id === updatedCategory.id ? updatedCategory : cat))
        .sort((a, b) => a.name.localeCompare(b.name))
    );
    setShowForm(false);
    setEditingCategory(null);
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setShowForm(true);
  };

  const handleDelete = async (categoryId: number) => {
    if (window.confirm('Are you sure you want to delete this category? This action cannot be undone.')) {
      try {
        await apiClient.delete(`/categories/${categoryId}`);
        toast.success('Category deleted successfully.');
        setCategories(prev => prev.filter(cat => cat.id !== categoryId));
      } catch (err) {
        console.error('Failed to delete category:', err);
        const errorMessage = apiClient.isAxiosError(err) && err.response?.data?.detail 
          ? err.response.data.detail 
          : 'Failed to delete category.';
        toast.error(errorMessage);
      }
    }
  };

  const openAddNewForm = () => {
    setEditingCategory(null);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingCategory(null);
  }

  if (isLoading && categories.length === 0) { // Show loading only on initial load
    return <div className="container"><p className="has-text-centered">Loading categories...</p></div>;
  }

  return (
    <div className="admin-categories-page container section">
      <div className="level">
        <div className="level-left">
          <h1 className="title">Manage Categories</h1>
        </div>
        <div className="level-right">
          <button className="button is-primary" onClick={openAddNewForm}>
            <span className="icon is-small"><i className="fas fa-plus"></i></span>
            <span>Add New Category</span>
          </button>
        </div>
      </div>

      {error && <div className="notification is-danger is-light">{error}</div>}

      {showForm && (
        <CategoryForm
          existingCategory={editingCategory}
          onCategoryCreated={handleCategoryCreated}
          onCategoryUpdated={handleCategoryUpdated}
          onCancel={handleCancelForm}
        />
      )}

      {!isLoading && categories.length === 0 && !showForm && (
        <div className="notification is-info is-light">
          No categories found. Click "Add New Category" to get started.
        </div>
      )}
      
      {categories.length > 0 && (
        <div className="categories-list-container box">
          <h2 className="subtitle">Existing Categories ({categories.length})</h2>
          <table className="table is-fullwidth is-striped is-hoverable">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(category => (
                <tr key={category.id}>
                  <td data-label="Name">{category.name}</td>
                  <td data-label="Description">{category.description || <span className="has-text-grey-light">N/A</span>}</td>
                  <td data-label="Actions">
                    <div className="buttons are-small">
                      <button className="button is-info is-outlined" onClick={() => handleEdit(category)}>
                        <span className="icon"><i className="fas fa-edit"></i></span>
                        <span>Edit</span>
                      </button>
                      <button className="button is-danger is-outlined" onClick={() => handleDelete(category.id)}>
                        <span className="icon"><i className="fas fa-trash-alt"></i></span>
                        <span>Delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminCategoriesPage;
