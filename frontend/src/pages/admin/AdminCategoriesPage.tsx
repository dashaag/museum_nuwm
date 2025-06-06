import React, { useState, useEffect, useCallback } from 'react';
import { AxiosError } from 'axios';
import { Link } from 'react-router-dom';
import apiClient from '../../config/api';
import { toast } from 'react-toastify';

// Define a type for the category structure
interface Category {
  id: number;
  name: string;
  description?: string; // Optional description
}

const AdminCategoriesPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // States for managing form inputs (new/edit category)
  const [currentName, setCurrentName] = useState('');
  const [currentDescription, setCurrentDescription] = useState('');
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  const fetchCategories = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await apiClient.get<Category[]>('/categories/');
      setCategories(response.data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
      setError('Failed to load categories. Please try again.');
      // Only show toast for refresh errors if categories were already loaded once
      if (categories.length > 0) {
        toast.error('Failed to refresh categories.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [categories]);

  useEffect(() => {
    if (categories.length === 0) {
      fetchCategories();
    }
  }, [fetchCategories, categories.length]);

  const resetForm = () => {
    setCurrentName('');
    setCurrentDescription('');
    setEditingCategory(null);
  };

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const categoryData = { name: currentName, description: currentDescription };

    if (!currentName.trim()) {
      toast.error('Category name cannot be empty.');
      return;
    }

    try {
      if (editingCategory) {
        // Update existing category
        await apiClient.put(`/categories/${editingCategory.id}`, categoryData);
        toast.success(`Category '${currentName}' updated successfully.`);
      } else {
        // Create new category
        await apiClient.post('/categories/', categoryData);
        toast.success(`Category '${currentName}' added successfully.`);
      }
      resetForm();
      fetchCategories(); // Refresh the list
    } catch (err) {
      console.error('Failed to save category:', err);
      let errorMessage = 'Failed to save category. Please check input and try again.';
      if (err instanceof AxiosError && err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      toast.error(errorMessage);
    }
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setCurrentName(category.name);
    setCurrentDescription(category.description || '');
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to form for editing
  };

  const handleDelete = async (categoryId: number, categoryName: string) => {
    if (window.confirm(`Are you sure you want to delete the category '${categoryName}'? This action cannot be undone.`)) {
      try {
        await apiClient.delete(`/categories/${categoryId}`);
        toast.success(`Category '${categoryName}' deleted successfully.`);
        fetchCategories(); // Refresh the list
        if (editingCategory && editingCategory.id === categoryId) {
          resetForm(); // Clear form if the deleted category was being edited
        }
      } catch (err) {
        console.error('Failed to delete category:', err);
        let errorMessage = 'Failed to delete category.';
      if (err instanceof AxiosError && err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
        toast.error(errorMessage);
      }
    }
  };

  // Show loading indicator only on initial load or if explicitly set during refresh
  if (isLoading && categories.length === 0) return <div className="container section"><p>Loading categories...</p></div>;
  // Show main error message only if categories failed to load initially
  if (error && categories.length === 0) return <div className="container section"><p className="has-text-danger">{error}</p></div>;

  return (
    <div className="container section">
      <h1 className="title">Manage Categories</h1>
      <p className="subtitle">Add, edit, or delete art categories.</p>
      
      <div className="box mb-5">
        <h2 className="title is-4 has-text-centered mb-4">{editingCategory ? 'Edit Category' : 'Add New Category'}</h2>
        <form onSubmit={handleFormSubmit}>
          <div className="field">
            <label className="label" htmlFor="categoryName">Name <span className="has-text-danger">*</span></label>
            <div className="control has-icons-left">
              <input 
                id="categoryName"
                className="input" 
                type="text" 
                placeholder="e.g., Renaissance Art" 
                value={currentName} 
                onChange={(e) => setCurrentName(e.target.value)} 
                required 
              />
              <span className="icon is-small is-left">
                <i className="fas fa-tag"></i>
              </span>
            </div>
          </div>
          <div className="field">
            <label className="label" htmlFor="categoryDescription">Description</label>
            <div className="control has-icons-left">
              <textarea 
                id="categoryDescription"
                className="textarea" 
                placeholder="A brief description of the category (optional)"
                value={currentDescription}
                onChange={(e) => setCurrentDescription(e.target.value)}
                rows={3}
              ></textarea>
               <span className="icon is-small is-left" style={{alignItems: 'flex-start', paddingTop: '0.5em'}}>
                <i className="fas fa-align-left"></i>
              </span>
            </div>
          </div>
          <div className="field is-grouped mt-4">
            <div className="control">
              <button type="submit" className={`button is-primary ${isLoading ? 'is-loading' : ''}`} disabled={isLoading}>
                <span className="icon is-small">
                  <i className={`fas ${editingCategory ? 'fa-save' : 'fa-plus'}`}></i>
                </span>
                <span>{editingCategory ? 'Update Category' : 'Add Category'}</span>
              </button>
            </div>
            {editingCategory && (
              <div className="control">
                <button type="button" className="button is-light" onClick={resetForm} disabled={isLoading}>
                   <span className="icon is-small">
                    <i className="fas fa-times"></i>
                  </span>
                  <span>Cancel Edit</span>
                </button>
              </div>
            )}
          </div>
        </form>
      </div>

      <h2 className="title is-4">Existing Categories</h2>
      {isLoading && categories.length > 0 && <div className="notification is-light"><span className="icon"><i className="fas fa-spinner fa-pulse"></i></span> Refreshing categories...</div>}
      {categories.length === 0 && !isLoading ? (
        <div className="notification is-warning">
          No categories found. You can add some using the form above.
        </div>
      ) : (
        <div className="table-container">
          <table className="table is-striped is-fullwidth is-hoverable is-narrow">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th className="has-text-centered">Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(category => (
                <tr key={category.id}>
                  <td>{category.id}</td>
                  <td>{category.name}</td>
                  <td>{category.description || <span className="has-text-grey-light">N/A</span>}</td>
                  <td className="has-text-centered">
                    <button 
                      onClick={() => handleEdit(category)} 
                      className="button is-small is-info mr-2"
                      title="Edit Category"
                      disabled={isLoading}
                    >
                      <span className="icon is-small"><i className="fas fa-edit"></i></span>
                      <span>Edit</span>
                    </button>
                    <button 
                      onClick={() => handleDelete(category.id, category.name)} 
                      className="button is-small is-danger"
                      title="Delete Category"
                      disabled={isLoading}
                    >
                      <span className="icon is-small"><i className="fas fa-trash-alt"></i></span>
                      <span>Delete</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <hr />
      <Link to="/admin/dashboard" className="button is-link is-light mt-3">
        <span className="icon is-small">
          <i className="fas fa-arrow-left"></i>
        </span>
        <span>Back to Dashboard</span>
      </Link>
    </div>
  );
};

export default AdminCategoriesPage;
