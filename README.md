# Museum Art Website

This project is a full-stack web application for a museum, allowing public users to view art pieces and managers to perform CRUD operations on them.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React (Vite + TypeScript)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT

## Project Structure

```
/museum-app
├── backend/         # FastAPI application
├── frontend/        # React application
├── docker-compose.yml
└── README.md
```

## Setup and Running the Application

1.  **Clone the repository (if applicable) or ensure you have the project files.**

2.  **Prerequisites:**
    *   Docker and Docker Compose installed.

3.  **Environment Variables:**
    *   The backend requires a `.env` file in the `backend/` directory. Create one based on `backend/.env.example`.
    *   Copy `backend/.env.example` to `backend/.env` and update the `SECRET_KEY` and any other necessary variables.
      ```bash
      cp backend/.env.example backend/.env
      ```

4.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```
    To view logs:
    ```bash
    docker-compose logs -f
    ```

5.  **Accessing the application:**
    *   Frontend (Public & Admin): [http://localhost:5173](http://localhost:5173)
    *   Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Seeding the Database

The database will be seeded automatically when the backend container starts up for the first time if `INIT_DB=true` in `backend/.env`.

## API Endpoints

-   `POST /api/auth/login`
-   `GET /api/categories/`
-   `GET /api/pieces/`
-   `POST /api/pieces/` (Manager only)
-   `GET /api/pieces/{piece_id}`
-   `PUT /api/pieces/{piece_id}` (Manager only)
-   `DELETE /api/pieces/{piece_id}` (Manager only)

## Sample API Requests (using curl or httpie)

### Login as Manager

```bash
# Using httpie
http post :8000/api/auth/login email=admin@museum.com password=Admin123!

# Using curl
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d 'username=admin@museum.com&password=Admin123!' http://localhost:8000/api/auth/login
```

### Fetch Categories

```bash
http :8000/api/categories/
curl http://localhost:8000/api/categories/
```

### Fetch All Art Pieces (Public)

```bash
http :8000/api/pieces/
curl http://localhost:8000/api/pieces/
```

### Create Art Piece (Manager - replace YOUR_JWT_TOKEN)

*Get the token from the login response.*

```bash
# Using httpie
http post :8000/api/pieces/ name='New Art' description='A beautiful new piece' category_id=1 image_url='http://example.com/image.jpg' "Authorization:Bearer YOUR_JWT_TOKEN"

# Using curl
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d '{"name": "New Art", "description": "A beautiful new piece", "category_id": 1, "image_url": "http://example.com/image.jpg"}' http://localhost:8000/api/pieces/
```

### Update Art Piece (Manager - replace YOUR_JWT_TOKEN and piece_id)

```bash
# Using httpie
http put :8000/api/pieces/1 name='Updated Art Name' "Authorization:Bearer YOUR_JWT_TOKEN"

# Using curl
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d '{"name": "Updated Art Name"}' http://localhost:8000/api/pieces/1
```

### Delete Art Piece (Manager - replace YOUR_JWT_TOKEN and piece_id)

```bash
# Using httpie
http delete :8000/api/pieces/1 "Authorization:Bearer YOUR_JWT_TOKEN"

# Using curl
curl -X DELETE -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/pieces/1
```
