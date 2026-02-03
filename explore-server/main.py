#!/usr/bin/env python3
"""
FastAPI Server with Rate Limiting
A comprehensive FastAPI implementation with rate limiting capabilities
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from strawberry.fastapi import GraphQLRouter
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import uvicorn

# Import GraphQL schema and configuration
from graphql_schema import schema
from config import config

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    **config.get_cors_config()
)

# GraphQL endpoint with rate limiting
@app.post("/graphql")
@limiter.limit(config.GRAPHQL_RATE_LIMIT)
async def graphql_post(request: Request):
    """
    GraphQL POST endpoint for queries and mutations
    Rate limit: Configurable via GRAPHQL_RATE_LIMIT env var
    """
    try:
        body = await request.json()
        query = body.get("query", "")
        variables = body.get("variables", {})
        operation_name = body.get("operationName")
        
        # Execute GraphQL query using strawberry
        result = await schema.execute(
            query, 
            variable_values=variables,
            operation_name=operation_name,
            context_value={"request": request}
        )
        
        response_data = {"data": result.data}
        if result.errors:
            response_data["errors"] = [
                {"message": str(error), "locations": getattr(error, 'locations', None)}
                for error in result.errors
            ]
        
        return response_data
        
    except Exception as e:
        return {
            "errors": [{"message": f"GraphQL execution error: {str(e)}"}]
        }

@app.get("/graphql")
@limiter.limit("30/minute")
async def graphql_playground(request: Request):
    """
    GraphQL Playground (interactive GraphQL IDE)
    Rate limit: 30 requests per minute per IP
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
    </head>
    <body>
        <div id="root">
            <style>
                body { margin: 0; font-family: Arial, sans-serif; }
                #root { height: 100vh; }
                .playground { height: 100%; }
            </style>
            <div class="playground">
                <h1>GraphQL Playground</h1>
                <p>Use POST requests to /graphql for GraphQL operations</p>
                <h2>Sample Query:</h2>
                <pre>
query GetUsers {
  users(limit: 5) {
    id
    name
    email
    createdAt
  }
}
                </pre>
                <h2>Sample Mutation:</h2>
                <pre>
mutation CreateUser($userInput: UserInput!) {
  createUser(userInput: $userInput) {
    id
    name
    email
  }
}

# Variables:
{
  "userInput": {
    "name": "Test User",
    "email": "test@example.com"
  }
}
                </pre>
                <p><strong>Endpoint:</strong> <code>POST /graphql</code></p>
                <p><strong>Rate Limit:</strong> 15 requests per minute</p>
            </div>
        </div>
    </body>
    </html>
    """

# In-memory storage for demo purposes
data_store: Dict[str, Any] = {
    "users": {},
    "posts": {},
    "counters": {"requests": 0, "users": 0, "posts": 0}
}


@app.get("/")
@limiter.limit(config.DEFAULT_RATE_LIMIT)
async def root(request: Request):
    """
    Root endpoint with basic rate limiting
    Rate limit: Configurable via DEFAULT_RATE_LIMIT env var
    """
    data_store["counters"]["requests"] += 1
    return {
        "message": "Welcome to Explore Server!",
        "timestamp": datetime.now().isoformat(),
        "total_requests": data_store["counters"]["requests"],
        "rate_limit": config.DEFAULT_RATE_LIMIT
    }


@app.get("/health")
@limiter.limit("30/minute")
async def health_check(request: Request):
    """
    Health check endpoint
    Rate limit: 30 requests per minute per IP
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "Server is running",
        "rate_limit": "30 requests per minute"
    }


@app.get("/api/users")
@limiter.limit("20/minute")
async def get_users(request: Request, limit: int = 10, offset: int = 0):
    """
    Get users with pagination
    Rate limit: 20 requests per minute per IP
    """
    users_list = list(data_store["users"].values())
    paginated_users = users_list[offset:offset + limit]
    
    return {
        "users": paginated_users,
        "total": len(users_list),
        "limit": limit,
        "offset": offset,
        "rate_limit": "20 requests per minute"
    }


@app.post("/api/users")
@limiter.limit("5/minute")
async def create_user(request: Request, user_data: dict):
    """
    Create a new user
    Rate limit: 5 requests per minute per IP (stricter for write operations)
    """
    if not user_data.get("name") or not user_data.get("email"):
        raise HTTPException(status_code=400, detail="Name and email are required")
    
    user_id = f"user_{len(data_store['users']) + 1}"
    data_store["counters"]["users"] += 1
    
    new_user = {
        "id": user_id,
        "name": user_data["name"],
        "email": user_data["email"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data_store["users"][user_id] = new_user
    
    return {
        "message": "User created successfully",
        "user": new_user,
        "rate_limit": "5 requests per minute"
    }


@app.get("/api/users/{user_id}")
@limiter.limit("50/minute")
async def get_user(request: Request, user_id: str):
    """
    Get a specific user by ID
    Rate limit: 50 requests per minute per IP (higher for read operations)
    """
    if user_id not in data_store["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user": data_store["users"][user_id],
        "rate_limit": "50 requests per minute"
    }


@app.put("/api/users/{user_id}")
@limiter.limit("3/minute")
async def update_user(request: Request, user_id: str, user_data: dict):
    """
    Update a user
    Rate limit: 3 requests per minute per IP (very strict for updates)
    """
    if user_id not in data_store["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = data_store["users"][user_id]
    
    if "name" in user_data:
        user["name"] = user_data["name"]
    if "email" in user_data:
        user["email"] = user_data["email"]
    
    user["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "User updated successfully",
        "user": user,
        "rate_limit": "3 requests per minute"
    }


@app.delete("/api/users/{user_id}")
@limiter.limit("2/minute")
async def delete_user(request: Request, user_id: str):
    """
    Delete a user
    Rate limit: 2 requests per minute per IP (strictest for delete operations)
    """
    if user_id not in data_store["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = data_store["users"].pop(user_id)
    
    return {
        "message": "User deleted successfully",
        "deleted_user": deleted_user,
        "rate_limit": "2 requests per minute"
    }


@app.get("/api/posts")
@limiter.limit("25/minute")
async def get_posts(request: Request, author: Optional[str] = None):
    """
    Get posts, optionally filtered by author
    Rate limit: 25 requests per minute per IP
    """
    posts_list = list(data_store["posts"].values())
    
    if author:
        posts_list = [post for post in posts_list if post.get("author") == author]
    
    return {
        "posts": posts_list,
        "total": len(posts_list),
        "filter": {"author": author} if author else None,
        "rate_limit": "25 requests per minute"
    }


@app.post("/api/posts")
@limiter.limit("8/minute")
async def create_post(request: Request, post_data: dict):
    """
    Create a new post
    Rate limit: 8 requests per minute per IP
    """
    required_fields = ["title", "content", "author"]
    for field in required_fields:
        if not post_data.get(field):
            raise HTTPException(status_code=400, detail=f"{field} is required")
    
    post_id = f"post_{len(data_store['posts']) + 1}"
    data_store["counters"]["posts"] += 1
    
    new_post = {
        "id": post_id,
        "title": post_data["title"],
        "content": post_data["content"],
        "author": post_data["author"],
        "tags": post_data.get("tags", []),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data_store["posts"][post_id] = new_post
    
    return {
        "message": "Post created successfully",
        "post": new_post,
        "rate_limit": "8 requests per minute"
    }


@app.get("/api/slow-endpoint")
@limiter.limit("2/minute")
async def slow_endpoint(request: Request, delay: int = 2):
    """
    Simulated slow endpoint for testing
    Rate limit: 2 requests per minute per IP (strict due to resource intensity)
    """
    if delay > config.MAX_SLOW_OPERATION_DELAY:
        raise HTTPException(
            status_code=400, 
            detail=f"Maximum delay is {config.MAX_SLOW_OPERATION_DELAY} seconds"
        )
    
    await asyncio.sleep(delay)
    
    return {
        "message": f"Slow operation completed after {delay} seconds",
        "timestamp": datetime.now().isoformat(),
        "rate_limit": "2 requests per minute",
        "max_delay": config.MAX_SLOW_OPERATION_DELAY
    }


@app.get("/api/stats")
@limiter.limit("15/minute")
async def get_stats(request: Request):
    """
    Get server statistics
    Rate limit: 15 requests per minute per IP
    """
    return {
        "statistics": {
            "total_requests": data_store["counters"]["requests"],
            "total_users": len(data_store["users"]),
            "total_posts": len(data_store["posts"]),
            "users_created": data_store["counters"]["users"],
            "posts_created": data_store["counters"]["posts"]
        },
        "timestamp": datetime.now().isoformat(),
        "rate_limit": "15 requests per minute"
    }


@app.get("/api/rate-limit-info")
@limiter.limit(config.LOOSE_RATE_LIMIT)
async def rate_limit_info(request: Request):
    """
    Get information about rate limits for all endpoints
    Rate limit: 60 requests per minute per IP
    """
    rate_limits = {
        "endpoints": {
            "GET /": "10/minute",
            "GET /health": "30/minute",
            "GET /api/users": "20/minute",
            "POST /api/users": "5/minute",
            "GET /api/users/{id}": "50/minute",
            "PUT /api/users/{id}": "3/minute",
            "DELETE /api/users/{id}": "2/minute",
            "GET /api/posts": "25/minute",
            "POST /api/posts": "8/minute",
            "GET /api/slow-endpoint": "2/minute",
            "GET /api/stats": "15/minute",
            "GET /api/rate-limit-info": "60/minute",
            "POST /graphql": "15/minute",
            "GET /graphql": "30/minute (playground)",
            "GET /api/graphql-info": "60/minute"
        },
        "note": "Rate limits are per IP address per minute",
        "rate_limit": "60 requests per minute"
    }
    
@app.get("/api/graphql-info")
@limiter.limit("60/minute")
async def graphql_info(request: Request):
    """
    Get GraphQL schema information and examples
    Rate limit: 60 requests per minute per IP
    """
    return rate_limits


@app.get("/api/graphql-info")
@limiter.limit("60/minute")
async def graphql_info(request: Request):
    """
    Get GraphQL schema information and examples
    Rate limit: 60 requests per minute per IP
    """
    return {
        "graphql_endpoint": "/graphql",
        "methods": ["POST"],
        "playground": "/graphql (GET)",
        "rate_limit": "15 requests per minute",
        "schema_info": {
            "queries": [
                "users(limit, offset)",
                "user(userId)",
                "posts(author, limit)",
                "post(postId)",
                "searchUsers(query)",
                "searchPosts(query)",
                "serverStats"
            ],
            "mutations": [
                "createUser(userInput)",
                "updateUser(userId, userInput)",
                "deleteUser(userId)",
                "createPost(postInput)",
                "updatePost(postId, postInput)",
                "deletePost(postId)",
                "simulateSlowOperation(delay)"
            ]
        },
        "sample_query": {
            "query": "query { users(limit: 5) { id name email } }",
            "variables": {}
        },
        "sample_mutation": {
            "query": "mutation($input: UserInput!) { createUser(userInput: $input) { id name email } }",
            "variables": {
                "input": {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            }
        }
    }


# Custom exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code=429,
        content={
            "error": config.RATE_LIMIT_MESSAGE,
            "detail": f"Rate limit exceeded: {exc.detail}",
            "retry_after": f"Please wait {config.RETRY_AFTER_SECONDS} seconds before making another request",
            "timestamp": datetime.now().isoformat()
        }
    )
    response.headers["Retry-After"] = str(config.RETRY_AFTER_SECONDS)
    return response


if __name__ == "__main__":
    print("Starting Explore Server with Rate Limiting...")
    print(f"Server will be available at: http://{config.HOST}:{config.PORT}")
    print(f"API Documentation: http://{config.HOST}:{config.PORT}/docs")
    print(f"GraphQL Endpoint: http://{config.HOST}:{config.PORT}/graphql")
    print(f"Rate Limit Info: http://{config.HOST}:{config.PORT}/api/rate-limit-info")
    
    # Print configuration if debug mode
    if config.DEBUG:
        config.print_config()
    
    uvicorn.run(
        "main:app",
        **config.get_server_config()
    )