# Flask API Boilerplate

A flexible and production-ready Flask API boilerplate with authentication, database models, testing, and deployment configurations.

## Features

- **Authentication & Authorization**: JWT-based authentication with user management
- **Database Models**: User, Post, Tag, and Comment models with relationships
- **RESTful API**: Complete CRUD operations with pagination and filtering
- **Testing**: Comprehensive test suite with pytest
- **Database Migrations**: Flask-Migrate for database schema management
- **Configuration**: Environment-based configuration for different deployments
- **Security**: Password hashing, CORS support, and input validation
- **Documentation**: API documentation and setup guides
- **Deployment**: Docker and production deployment configurations

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── main/              # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth/              # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   └── api/               # API blueprint
│       ├── __init__.py
│       └── routes.py
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_api.py
├── migrations/            # Database migrations
├── app.py                 # Application factory
├── run.py                 # Development server
├── wsgi.py               # Production server
├── config.py             # Configuration classes
├── requirements.txt      # Python dependencies
├── pytest.ini           # Test configuration
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
└── README.md            # This file
```

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd flask-api-boilerplate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
# Set your database URL, secret keys, etc.
```

### 3. Database Setup

```bash
# Initialize database migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 4. Run the Application

```bash
# Development server
python run.py

# Or using Flask CLI
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout user
- `POST /auth/change-password` - Change password

### Posts

- `GET /api/v1/posts` - Get all posts (with pagination)
- `POST /api/v1/posts` - Create a new post (authenticated)
- `GET /api/v1/posts/<id>` - Get specific post
- `PUT /api/v1/posts/<id>` - Update post (authenticated)
- `DELETE /api/v1/posts/<id>` - Delete post (authenticated)

### Tags

- `GET /api/v1/tags` - Get all tags
- `POST /api/v1/tags` - Create new tag (authenticated)

### Comments

- `GET /api/v1/posts/<post_id>/comments` - Get post comments
- `POST /api/v1/posts/<post_id>/comments` - Create comment

### Admin (Admin only)

- `GET /api/v1/admin/users` - Get all users
- `GET /api/v1/admin/comments` - Get all comments
- `POST /api/v1/admin/comments/<id>/approve` - Approve comment

## Database Models

### User
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `first_name`, `last_name` (String)
- `is_active`, `is_admin` (Boolean)
- `created_at`, `updated_at`, `last_login` (DateTime)

### Post
- `id` (UUID, Primary Key)
- `title`, `content`, `excerpt` (String/Text)
- `slug` (String, Unique)
- `is_published` (Boolean)
- `published_at`, `created_at`, `updated_at` (DateTime)
- `user_id` (Foreign Key to User)

### Tag
- `id` (UUID, Primary Key)
- `name`, `slug` (String, Unique)
- `description` (Text)
- `created_at` (DateTime)

### Comment
- `id` (UUID, Primary Key)
- `content` (Text)
- `is_approved` (Boolean)
- `author_name`, `author_email` (String)
- `created_at` (DateTime)
- `post_id` (Foreign Key to Post)
- `user_id` (Foreign Key to User, Optional)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Configuration

The application supports multiple environments:

- **Development**: SQLite database, debug mode enabled
- **Testing**: In-memory SQLite database
- **Production**: PostgreSQL/MySQL database, optimized settings
- **Docker**: Production settings with proxy support

### Environment Variables

Key environment variables (see `env.example`):

- `FLASK_ENV` - Environment (development, production, testing)
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `DATABASE_URL` - Database connection string
- `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` - Email configuration
- `CORS_ORIGINS` - Allowed CORS origins

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in production mode
docker-compose -f docker-compose.prod.yml up
```

### Manual Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## Development

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8
```

### Database Migrations

```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## API Usage Examples

### Register User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "johndoe",
    "password": "securepassword"
  }'
```

### Create Post (Authenticated)

```bash
curl -X POST http://localhost:5000/api/v1/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "excerpt": "A brief excerpt",
    "is_published": true
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please open an issue in the repository.
