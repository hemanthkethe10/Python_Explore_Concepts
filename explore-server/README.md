# Explore Server - FastAPI with Rate Limiting & GraphQL

A comprehensive FastAPI server implementation featuring rate limiting, REST API, GraphQL endpoints, CRUD operations, and various endpoints for testing and exploration.

## 🚀 Features

### Rate Limiting
- **IP-based rate limiting** using SlowAPI
- **Different limits per endpoint** based on operation type
- **Custom rate limit exceeded handler** with proper HTTP 429 responses
- **Retry-After headers** for client guidance

### GraphQL API
- **Complete GraphQL implementation** using Strawberry GraphQL
- **Queries and Mutations** for users and posts
- **Search functionality** across users and posts
- **Server statistics** via GraphQL
- **Rate limited GraphQL endpoint** (15 requests/minute)
- **GraphQL Playground** for interactive testing

### REST API Endpoints with Rate Limits

| Endpoint | Method | Rate Limit | Description |
|----------|--------|------------|-------------|
| `/` | GET | 10/minute | Root endpoint |
| `/health` | GET | 30/minute | Health check |
| `/api/users` | GET | 20/minute | List users with pagination |
| `/api/users` | POST | 5/minute | Create user (stricter for writes) |
| `/api/users/{id}` | GET | 50/minute | Get specific user |
| `/api/users/{id}` | PUT | 3/minute | Update user (very strict) |
| `/api/users/{id}` | DELETE | 2/minute | Delete user (strictest) |
| `/api/posts` | GET | 25/minute | List posts |
| `/api/posts` | POST | 8/minute | Create post |
| `/api/slow-endpoint` | GET | 2/minute | Simulated slow operation |
| `/api/stats` | GET | 15/minute | Server statistics |
| `/api/rate-limit-info` | GET | 60/minute | Rate limit information |
| `/graphql` | GET/POST | 15/minute | GraphQL endpoint |

### GraphQL Operations

#### Queries
- `users(limit, offset)` - Get users with pagination
- `user(userId)` - Get specific user by ID
- `posts(author, limit)` - Get posts, optionally filtered by author
- `post(postId)` - Get specific post by ID
- `serverStats` - Get server statistics
- `searchUsers(query)` - Search users by name or email
- `searchPosts(query)` - Search posts by title or content

#### Mutations
- `createUser(userInput)` - Create a new user
- `updateUser(userId, userInput)` - Update existing user
- `deleteUser(userId)` - Delete a user
- `createPost(postInput)` - Create a new post
- `updatePost(postId, postInput)` - Update existing post
- `deletePost(postId)` - Delete a post
- `simulateSlowOperation(delay)` - Simulate slow operation

## 📦 Installation

### 1. Navigate to the explore-server directory
```bash
cd explore-server
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔗 Access Points

- **Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **GraphQL Endpoint**: http://localhost:8000/graphql
- **GraphQL Playground**: http://localhost:8000/graphql (GET request)
- **Rate Limit Info**: http://localhost:8000/api/rate-limit-info

## 🧪 Testing

### Testing Rate Limits (REST API)
```bash
# Run the REST API rate limit test script
python test_rate_limits.py
```

### Testing GraphQL
```bash
# Run the GraphQL test script
python test_graphql.py
```

### Manual Testing with curl

#### REST API
```bash
# Test basic endpoint (10/minute limit)
curl http://localhost:8000/

# Test user creation (5/minute limit)
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

#### GraphQL
```bash
# Test GraphQL query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { users(limit: 5) { id name email } }"
  }'

# Test GraphQL mutation
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: UserInput!) { createUser(userInput: $input) { id name email } }",
    "variables": {
      "input": {
        "name": "GraphQL User",
        "email": "graphql@example.com"
      }
    }
  }'
```

### Using Python requests
```python
import requests
import time

# Test rate limiting
url = "http://localhost:8000/"
for i in range(15):
    response = requests.get(url)
    print(f"Request {i+1}: Status {response.status_code}")
    if response.status_code == 429:
        print("Rate limit exceeded!")
        break
    time.sleep(1)
```

## 📊 GraphQL Examples

### Sample Queries

#### Get Users with Pagination
```graphql
query GetUsers($limit: Int, $offset: Int) {
  users(limit: $limit, offset: $offset) {
    id
    name
    email
    createdAt
    updatedAt
  }
}
```

#### Search Users
```graphql
query SearchUsers($query: String!) {
  searchUsers(query: $query) {
    id
    name
    email
  }
}
```

#### Get Posts by Author
```graphql
query GetPostsByAuthor($author: String, $limit: Int) {
  posts(author: $author, limit: $limit) {
    id
    title
    content
    author
    tags
    createdAt
  }
}
```

#### Complex Query (Multiple Operations)
```graphql
query ComplexQuery {
  users(limit: 3) {
    id
    name
    email
  }
  posts(limit: 3) {
    id
    title
    author
    tags
  }
  serverStats {
    totalUsers
    totalPosts
    timestamp
  }
}
```

### Sample Mutations

#### Create User
```graphql
mutation CreateUser($userInput: UserInput!) {
  createUser(userInput: $userInput) {
    id
    name
    email
    createdAt
    updatedAt
  }
}

# Variables:
{
  "userInput": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

#### Update User
```graphql
mutation UpdateUser($userId: String!, $userInput: UserUpdateInput!) {
  updateUser(userId: $userId, userInput: $userInput) {
    id
    name
    email
    updatedAt
  }
}

# Variables:
{
  "userId": "user_1",
  "userInput": {
    "name": "John Updated"
  }
}
```

#### Create Post
```graphql
mutation CreatePost($postInput: PostInput!) {
  createPost(postInput: $postInput) {
    id
    title
    content
    author
    tags
    createdAt
  }
}

# Variables:
{
  "postInput": {
    "title": "My First Post",
    "content": "This is the content of my first post",
    "author": "john@example.com",
    "tags": ["first", "post", "example"]
  }
}
```

## 📊 Rate Limiting Strategy

### Read Operations (Higher Limits)
- **GET /api/users/{id}**: 50/minute - Individual user lookups
- **GET /health**: 30/minute - Health checks
- **GET /api/posts**: 25/minute - Listing posts

### Write Operations (Lower Limits)
- **POST /api/posts**: 8/minute - Creating content
- **POST /api/users**: 5/minute - Creating users
- **PUT /api/users/{id}**: 3/minute - Updating users

### Destructive Operations (Strictest Limits)
- **DELETE /api/users/{id}**: 2/minute - Deleting users
- **GET /api/slow-endpoint**: 2/minute - Resource-intensive operations

## 🛡️ Rate Limiting Features

### IP-Based Limiting
- Rate limits are applied per IP address
- Uses `get_remote_address` to identify clients
- Supports both IPv4 and IPv6

### Custom Error Handling
- Returns HTTP 429 for rate limit exceeded
- Includes `Retry-After` header
- Provides detailed error messages with timestamps

### Middleware Integration
- Uses SlowAPI middleware for seamless integration
- Automatic rate limit enforcement
- No manual rate limit checking required

## 📈 Monitoring

### Statistics Endpoint
```bash
curl http://localhost:8000/api/stats
```

Returns:
```json
{
  "statistics": {
    "total_requests": 150,
    "total_users": 5,
    "total_posts": 3,
    "users_created": 5,
    "posts_created": 3
  },
  "timestamp": "2024-01-13T10:30:00",
  "rate_limit": "15 requests per minute"
}
```

## 🔧 Configuration

### Customizing Rate Limits
Edit the `@limiter.limit()` decorators in `main.py`:

```python
@app.get("/api/custom-endpoint")
@limiter.limit("100/hour")  # Custom rate limit
async def custom_endpoint(request: Request):
    return {"message": "Custom rate limited endpoint"}
```

### Rate Limit Formats
- `"10/minute"` - 10 requests per minute
- `"100/hour"` - 100 requests per hour
- `"1000/day"` - 1000 requests per day
- `"5/second"` - 5 requests per second

## 🚨 Error Responses

### Rate Limit Exceeded (429)
```json
{
  "error": "Rate limit exceeded",
  "detail": "Rate limit exceeded: 10 per 1 minute",
  "retry_after": "Please wait before making another request",
  "timestamp": "2024-01-13T10:30:00"
}
```

### Validation Error (400)
```json
{
  "detail": "Name and email are required"
}
```

### Not Found (404)
```json
{
  "detail": "User not found"
}
```

## 🎯 Use Cases

1. **API Rate Limiting Testing** - Test how applications handle rate limits
2. **Load Testing** - Simulate rate-limited environments
3. **Client Development** - Develop against rate-limited APIs
4. **Educational** - Learn about rate limiting implementations
5. **Prototyping** - Quick API prototyping with built-in protection

## 🔄 Development

### Adding New Endpoints
1. Define the endpoint function
2. Add appropriate rate limiting decorator
3. Include rate limit info in response
4. Update documentation

### Example:
```python
@app.get("/api/new-endpoint")
@limiter.limit("20/minute")
async def new_endpoint(request: Request):
    return {
        "message": "New endpoint",
        "rate_limit": "20 requests per minute"
    }
```

---

**Happy API exploring with rate limiting! 🚀**