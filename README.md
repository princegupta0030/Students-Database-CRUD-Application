# Student Database CRUD Application

This is a simple FastAPI project for a student database, designed for an internship assignment. It uses Python's built-in `sqlite3` module for database operations.

## Prerequisites
- Python 3.9+
- pip (Python package installer)

## Installation

1. Clone the repository and navigate into the project folder.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the FastAPI application locally, run:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Create a Student
- **Method:** `POST`
- **URL:** `/students`
- **Request Body:** JSON
  ```json
  {
    "name": "John Doe",
    "date_of_birth": "2000-01-01",
    "email": "john@example.com"
  }
  ```
- **Responses:**
  - `201 Created`: Student successfully created.
  - `400 Bad Request`: Email already registered.
  - `422 Unprocessable Entity`: Validation error (e.g., incorrect date format).

### 2. Retrieve All Students
- **Method:** `GET`
- **URL:** `/students`
- **Query Parameters (Optional):**
  - `name`: Filter by partial name match.
  - `email`: Filter by partial email match.
- **Responses:** `200 OK`

### 3. Retrieve a Specific Student
- **Method:** `GET`
- **URL:** `/students/{student_id}`
- **Responses:**
  - `200 OK`: Returns the student record.
  - `404 Not Found`: Student does not exist.

### 4. Update a Student
- **Method:** `PUT`
- **URL:** `/students/{student_id}`
- **Request Body:** JSON (requires all required fields like POST)
- **Responses:**
  - `200 OK`: Returns the updated student record.
  - `404 Not Found`: Student does not exist.
  - `400 Bad Request`: Email already registered to another user.

### 5. Delete a Student
- **Method:** `DELETE`
- **URL:** `/students/{student_id}`
- **Responses:**
  - `200 OK`: Returns a success message.
  - `404 Not Found`: Student does not exist.

## API Testing Instructions

You can test the API using tools like `curl`, Postman, or FastAPI's interactive docs.

**Using FastAPI Interactive Docs (Swagger UI):**
1. Start the application.
2. Open your browser and navigate to `http://127.0.0.1:8000/docs`.
3. You can interact with all available endpoints directly from this page.
