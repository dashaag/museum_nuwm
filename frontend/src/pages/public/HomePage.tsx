import React, { useState, useEffect } from 'react';
import apiClient from '../../config/api';
import { Link } from 'react-router-dom';
import './HomePage.css'; // Import the new CSS file

// Interfaces (Category, PieceOfArt - remain the same)
interface Category {
  id: number;
  name: string;
  description?: string;
}

interface PieceOfArt {
  id: number;
  name: string;
  description?: string;
  image_url: string;
  category_id: number;
  category?: Category;
  created_at: string;
  updated_at?: string;
}

const HomePage: React.FC = () => {
  const [pieces, setPieces] = useState<PieceOfArt[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPieces = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiClient.get<PieceOfArt[]>('/pieces/');
        setPieces(response.data);
      } catch (err) {
        console.error('Failed to fetch pieces of art:', err);
        setError('Failed to load art pieces. Please try refreshing the page.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPieces();
  }, []);

  if (isLoading) {
    return (
      <div className="container section has-text-centered">
        {/* Using global .title and .progress styles from App.css */}
        <p className="title is-4">Loading art collection...</p>
        <progress className="progress is-large is-info" max="100">60%</progress>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container section has-text-centered">
        <p className="title is-4 has-text-danger">Error</p>
        <p>{error}</p>
        {/* Using global .button style from App.css */}
        <button className="button mt-4" onClick={() => window.location.reload()}>Try Again</button>
      </div>
    );
  }

  return (
    // Use the new class for the section
    <div className="container section art-collection-section">
      {/* Use the new class for the title */}
      <h1 className="title has-text-centered art-collection-title">Explore Our Art Collection</h1>
      {pieces.length === 0 ? (
        // Use the new class for the notification
        <div className="notification is-warning has-text-centered no-art-notification">
          <p className="title is-5">No art pieces to display at the moment.</p>
          <p>Please check back later or contact support if you believe this is an error.</p>
        </div>
      ) : (
        <div className="columns is-multiline is-variable is-4-tablet is-3-desktop"> {/* Added is-variable for spacing */}
          {pieces.map(piece => (
            <div key={piece.id} className="column is-one-third-tablet is-one-quarter-desktop"> {/* More responsive columns */}
              {/* Use the new class for the card */}
              <div className="card art-card">
                <div className="card-image">
                  <figure className="image is-4by3">
                    {/* img style for object-fit is good, also covered by art-card .card-image img in CSS */}
                    <img src={piece.image_url} alt={piece.name} />
                  </figure>
                </div>
                <div className="card-content">
                  <div className="media">
                    <div className="media-content">
                      <p className="title is-5">{piece.name}</p> {/* Adjusted title size */}
                      {piece.category && (
                        <p className="subtitle is-6">
                          <Link to={`/categories/${piece.category.id}`}>{piece.category.name}</Link>
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="content">
                    {piece.description ? (
                        piece.description.length > 100 ? `${piece.description.substring(0, 97)}...` : piece.description
                    ) : 'No description available.'}
                    <br />
                    <small>Added: {new Date(piece.created_at).toLocaleDateString()}</small>
                  </div>
                </div>
                {/* Optional: Card footer for View Details link */}
                {/* <footer className="card-footer">
                  <Link to={`/art/${piece.id}`} className="card-footer-item">View Details</Link>
                </footer> */}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HomePage;

