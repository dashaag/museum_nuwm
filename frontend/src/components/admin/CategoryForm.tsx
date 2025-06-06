// frontend/src/components/admin/CategoryForm.tsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import apiClient from '../../config/api';
import { isAxiosError } from 'axios'; // Correctly import isAxiosError
import './CategoryForm.css';

interface CategoryData {
  name: string;
  description?: string;
}

interface Category extends CategoryData {
  id: number;
}

interface CategoryFormProps {
  onCategoryCreated?: (category: Category) => void;
  onCategoryUpdated?: (category: Category) => void;
  existingCategory?: Category | null; // For editing
  onCancel?: () => void;
}

const CategoryForm: React.FC<CategoryFormProps> = ({
  onCategoryCreated,
  onCategoryUpdated,
  existingCategory,
  onCancel,
}) => {
  const [name, setName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const isEditing = !!existingCategory;

  useEffect(() => {
    if (isEditing && existingCategory) {
      setName(existingCategory.name);
      setDescription(existingCategory.description || '');
    } else {
      setName('');
      setDescription('');
    }
  }, [existingCategory, isEditing]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    const categoryData: CategoryData = {
      name,
      description: description || undefined,
    };

    try {
      if (isEditing && existingCategory) {
        const response = await apiClient.put<Category>(`/categories/${existingCategory.id}`, categoryData);
        toast.success(`Category "${response.data.name}" updated successfully!`);
        if (onCategoryUpdated) onCategoryUpdated(response.data);
      } else {
        const response = await apiClient.post<Category>('/categories/', categoryData);
        toast.success(`Category "${response.data.name}" created successfully!`);
        if (onCategoryCreated) onCategoryCreated(response.data);
        setName('');
        setDescription('');
      }
    } catch (err: unknown) {
      console.error('Failed to save category:', err);
      let errorMessage = 'Failed to save category. Please try again.';
      if (isAxiosError(err)) { // Use the imported isAxiosError
        if (err.response && err.response.data && err.response.data.detail) {
          errorMessage = typeof err.response.data.detail === 'string'
            ? err.response.data.detail
            : JSON.stringify(err.response.data.detail);
        } else if (err.message) {
          errorMessage = err.message;
        }
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`category-form-container ${isEditing ? 'editing' : 'creating'}`}>
      <h2 className="form-title">{isEditing ? 'Edit Category' : 'Add New Category'}</h2>
      {error && <div className="notification is-danger is-light">{error}</div>}
      <form onSubmit={handleSubmit} className="category-form">
        <div className="field">
          <label htmlFor="category-name" className="label">Category Name</label>
          <div className="control">
            <input
              type="text"
              id="category-name"
              className="input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Paintings, Sculptures"
              required
              disabled={isLoading}
            />
          </div>
        </div>

        <div className="field">
          <label htmlFor="category-description" className="label">Description (Optional)</label>
          <div className="control">
            <textarea
              id="category-description"
              className="textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="A brief description of the category"
              rows={3}
              disabled={isLoading}
            />
          </div>
        </div>

        <div className="field is-grouped">
          <div className="control">
            <button type="submit" className={`button is-primary ${isLoading ? 'is-loading' : ''}`} disabled={isLoading}>
              {isEditing ? 'Save Changes' : 'Add Category'}
            </button>
          </div>
          {onCancel && (
            <div className="control">
              <button type="button" className="button is-light" onClick={onCancel} disabled={isLoading}>
                Cancel
              </button>
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default CategoryForm;
