# API Documentation

This document provides detailed information about the Flask API endpoints.

## Base URL

- Development: `http://localhost:5000`
- Production: `https://your-domain.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Response Format

All API responses are in JSON format. Success responses typically include:

```json
{
  "message": "Success message",
  "data": { ... }
}
```

Error responses include:

```json
{
  "error": "Error message"
}
```

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2023-01-01T00:00:00"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

### Login

**POST** `/auth/login`

Authenticate user and receive tokens.

**Request Body:**
```json
{
  "username_or_email": "johndoe",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": { ... },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

### Refresh Token

**POST** `/auth/refresh`

Get a new access token using refresh token.

**Headers:** `Authorization: Bearer REFRESH_TOKEN`

**Response:**
```json
{
  "access_token": "new_jwt_token"
}
```

### Get Current User

**GET** `/auth/me`

Get current user information.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

**Response:**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2023-01-01T00:00:00",
  "last_login": "2023-01-01T00:00:00"
}
```

### Change Password

**POST** `/auth/change-password`

Change user password.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword"
}
```

### Logout

**POST** `/auth/logout`

Logout user (client should discard tokens).

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

## Post Endpoints

### Get All Posts

**GET** `/api/v1/posts`

Get paginated list of posts.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Posts per page (default: 10)
- `published_only` (bool): Only published posts (default: true)
- `tag` (string): Filter by tag slug

**Response:**
```json
{
  "posts": [
    {
      "id": "uuid",
      "title": "Post Title",
      "content": "Post content...",
      "excerpt": "Post excerpt",
      "slug": "post-title",
      "is_published": true,
      "published_at": "2023-01-01T00:00:00",
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-01T00:00:00",
      "author": { ... },
      "tags": [ ... ],
      "comment_count": 5
    }
  ],
  "total": 100,
  "pages": 10,
  "current_page": 1
}
```

### Create Post

**POST** `/api/v1/posts`

Create a new post.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

**Request Body:**
```json
{
  "title": "My New Post",
  "content": "This is the content of my new post.",
  "excerpt": "A brief excerpt",
  "is_published": true
}
```

**Response:**
```json
{
  "message": "Post created successfully",
  "post": { ... }
}
```

### Get Specific Post

**GET** `/api/v1/posts/{post_id}`

Get a specific post by ID.

**Response:**
```json
{
  "id": "uuid",
  "title": "Post Title",
  "content": "Post content...",
  "excerpt": "Post excerpt",
  "slug": "post-title",
  "is_published": true,
  "published_at": "2023-01-01T00:00:00",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00",
  "author": { ... },
  "tags": [ ... ],
  "comment_count": 5
}
```

### Update Post

**PUT** `/api/v1/posts/{post_id}`

Update an existing post.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "excerpt": "Updated excerpt",
  "is_published": true
}
```

### Delete Post

**DELETE** `/api/v1/posts/{post_id}`

Delete a post.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

## Tag Endpoints

### Get All Tags

**GET** `/api/v1/tags`

Get all tags.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Technology",
    "slug": "technology",
    "description": "Posts about technology",
    "created_at": "2023-01-01T00:00:00"
  }
]
```

### Create Tag

**POST** `/api/v1/tags`

Create a new tag.

**Headers:** `Authorization: Bearer ACCESS_TOKEN`

**Request Body:**
```json
{
  "name": "Technology",
  "description": "Posts about technology"
}
```

## Comment Endpoints

### Get Post Comments

**GET** `/api/v1/posts/{post_id}/comments`

Get comments for a specific post.

**Response:**
```json
[
  {
    "id": "uuid",
    "content": "Great post!",
    "is_approved": true,
    "author_name": "John Doe",
    "author_email": "john@example.com",
    "created_at": "2023-01-01T00:00:00",
    "post_id": "post_uuid",
    "user_id": "user_uuid"
  }
]
```

### Create Comment

**POST** `/api/v1/posts/{post_id}/comments`

Create a comment for a post.

**Request Body:**
```json
{
  "content": "This is a great post!",
  "author_name": "John Doe",
  "author_email": "john@example.com"
}
```

## Admin Endpoints

*Note: Admin endpoints require admin privileges.*

### Get All Users

**GET** `/api/v1/admin/users`

Get all users with pagination.

**Headers:** `Authorization: Bearer ADMIN_ACCESS_TOKEN`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Users per page (default: 20)

### Get All Comments

**GET** `/api/v1/admin/comments`

Get all comments for moderation.

**Headers:** `Authorization: Bearer ADMIN_ACCESS_TOKEN`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Comments per page (default: 20)
- `approved_only` (bool): Only approved comments (default: false)

### Approve Comment

**POST** `/api/v1/admin/comments/{comment_id}/approve`

Approve a comment.

**Headers:** `Authorization: Bearer ADMIN_ACCESS_TOKEN`

## Error Codes

- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Rate Limiting

*Note: Rate limiting can be implemented using Flask-Limiter.*

## CORS

The API supports CORS for cross-origin requests. Configure allowed origins in the `CORS_ORIGINS` environment variable.

## Pagination

Most list endpoints support pagination:

- `page`: Page number (1-based)
- `per_page`: Items per page
- Response includes: `total`, `pages`, `current_page`

## Filtering and Sorting

- Posts can be filtered by `published_only` and `tag`
- Comments can be filtered by `approved_only`
- Results are typically sorted by creation date (newest first)
