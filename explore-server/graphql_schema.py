#!/usr/bin/env python3
"""
GraphQL Schema Definition
Defines GraphQL types, queries, and mutations for the Explore Server
"""

import strawberry
from typing import List, Optional
from datetime import datetime
import asyncio

# GraphQL Types
@strawberry.type
class User:
    id: str
    name: str
    email: str
    created_at: str
    updated_at: str

@strawberry.type
class Post:
    id: str
    title: str
    content: str
    author: str
    tags: List[str]
    created_at: str
    updated_at: str

@strawberry.type
class ServerStats:
    total_requests: int
    total_users: int
    total_posts: int
    users_created: int
    posts_created: int
    timestamp: str

@strawberry.type
class OperationResult:
    success: bool
    message: str
    data: Optional[str] = None

# Input Types
@strawberry.input
class UserInput:
    name: str
    email: str

@strawberry.input
class UserUpdateInput:
    name: Optional[str] = None
    email: Optional[str] = None

@strawberry.input
class PostInput:
    title: str
    content: str
    author: str
    tags: Optional[List[str]] = None

@strawberry.input
class PostUpdateInput:
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

# GraphQL Queries
@strawberry.type
class Query:
    @strawberry.field
    async def users(self, limit: int = 10, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        # Import here to avoid circular imports
        from main import data_store
        
        users_list = list(data_store["users"].values())
        paginated_users = users_list[offset:offset + limit]
        
        return [
            User(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                created_at=user["created_at"],
                updated_at=user["updated_at"]
            )
            for user in paginated_users
        ]
    
    @strawberry.field
    async def user(self, user_id: str) -> Optional[User]:
        """Get a specific user by ID"""
        from main import data_store
        
        user_data = data_store["users"].get(user_id)
        if not user_data:
            return None
        
        return User(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"]
        )
    
    @strawberry.field
    async def posts(self, author: Optional[str] = None, limit: int = 10) -> List[Post]:
        """Get all posts, optionally filtered by author"""
        from main import data_store
        
        posts_list = list(data_store["posts"].values())
        
        if author:
            posts_list = [post for post in posts_list if post.get("author") == author]
        
        # Apply limit
        posts_list = posts_list[:limit]
        
        return [
            Post(
                id=post["id"],
                title=post["title"],
                content=post["content"],
                author=post["author"],
                tags=post.get("tags", []),
                created_at=post["created_at"],
                updated_at=post["updated_at"]
            )
            for post in posts_list
        ]
    
    @strawberry.field
    async def post(self, post_id: str) -> Optional[Post]:
        """Get a specific post by ID"""
        from main import data_store
        
        post_data = data_store["posts"].get(post_id)
        if not post_data:
            return None
        
        return Post(
            id=post_data["id"],
            title=post_data["title"],
            content=post_data["content"],
            author=post_data["author"],
            tags=post_data.get("tags", []),
            created_at=post_data["created_at"],
            updated_at=post_data["updated_at"]
        )
    
    @strawberry.field
    async def server_stats(self) -> ServerStats:
        """Get server statistics"""
        from main import data_store
        
        return ServerStats(
            total_requests=data_store["counters"]["requests"],
            total_users=len(data_store["users"]),
            total_posts=len(data_store["posts"]),
            users_created=data_store["counters"]["users"],
            posts_created=data_store["counters"]["posts"],
            timestamp=datetime.now().isoformat()
        )
    
    @strawberry.field
    async def search_users(self, query: str) -> List[User]:
        """Search users by name or email"""
        from main import data_store
        
        query_lower = query.lower()
        matching_users = []
        
        for user_data in data_store["users"].values():
            if (query_lower in user_data["name"].lower() or 
                query_lower in user_data["email"].lower()):
                matching_users.append(User(
                    id=user_data["id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    created_at=user_data["created_at"],
                    updated_at=user_data["updated_at"]
                ))
        
        return matching_users
    
    @strawberry.field
    async def search_posts(self, query: str) -> List[Post]:
        """Search posts by title or content"""
        from main import data_store
        
        query_lower = query.lower()
        matching_posts = []
        
        for post_data in data_store["posts"].values():
            if (query_lower in post_data["title"].lower() or 
                query_lower in post_data["content"].lower()):
                matching_posts.append(Post(
                    id=post_data["id"],
                    title=post_data["title"],
                    content=post_data["content"],
                    author=post_data["author"],
                    tags=post_data.get("tags", []),
                    created_at=post_data["created_at"],
                    updated_at=post_data["updated_at"]
                ))
        
        return matching_posts

# GraphQL Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, user_input: UserInput) -> User:
        """Create a new user"""
        from main import data_store
        
        user_id = f"user_{len(data_store['users']) + 1}"
        data_store["counters"]["users"] += 1
        
        new_user = {
            "id": user_id,
            "name": user_input.name,
            "email": user_input.email,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        data_store["users"][user_id] = new_user
        
        return User(
            id=new_user["id"],
            name=new_user["name"],
            email=new_user["email"],
            created_at=new_user["created_at"],
            updated_at=new_user["updated_at"]
        )
    
    @strawberry.mutation
    async def update_user(self, user_id: str, user_input: UserUpdateInput) -> Optional[User]:
        """Update an existing user"""
        from main import data_store
        
        if user_id not in data_store["users"]:
            return None
        
        user = data_store["users"][user_id]
        
        if user_input.name is not None:
            user["name"] = user_input.name
        if user_input.email is not None:
            user["email"] = user_input.email
        
        user["updated_at"] = datetime.now().isoformat()
        
        return User(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"],
            updated_at=user["updated_at"]
        )
    
    @strawberry.mutation
    async def delete_user(self, user_id: str) -> OperationResult:
        """Delete a user"""
        from main import data_store
        
        if user_id not in data_store["users"]:
            return OperationResult(
                success=False,
                message=f"User with ID {user_id} not found"
            )
        
        deleted_user = data_store["users"].pop(user_id)
        
        return OperationResult(
            success=True,
            message=f"User {deleted_user['name']} deleted successfully",
            data=user_id
        )
    
    @strawberry.mutation
    async def create_post(self, post_input: PostInput) -> Post:
        """Create a new post"""
        from main import data_store
        
        post_id = f"post_{len(data_store['posts']) + 1}"
        data_store["counters"]["posts"] += 1
        
        new_post = {
            "id": post_id,
            "title": post_input.title,
            "content": post_input.content,
            "author": post_input.author,
            "tags": post_input.tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        data_store["posts"][post_id] = new_post
        
        return Post(
            id=new_post["id"],
            title=new_post["title"],
            content=new_post["content"],
            author=new_post["author"],
            tags=new_post["tags"],
            created_at=new_post["created_at"],
            updated_at=new_post["updated_at"]
        )
    
    @strawberry.mutation
    async def update_post(self, post_id: str, post_input: PostUpdateInput) -> Optional[Post]:
        """Update an existing post"""
        from main import data_store
        
        if post_id not in data_store["posts"]:
            return None
        
        post = data_store["posts"][post_id]
        
        if post_input.title is not None:
            post["title"] = post_input.title
        if post_input.content is not None:
            post["content"] = post_input.content
        if post_input.tags is not None:
            post["tags"] = post_input.tags
        
        post["updated_at"] = datetime.now().isoformat()
        
        return Post(
            id=post["id"],
            title=post["title"],
            content=post["content"],
            author=post["author"],
            tags=post["tags"],
            created_at=post["created_at"],
            updated_at=post["updated_at"]
        )
    
    @strawberry.mutation
    async def delete_post(self, post_id: str) -> OperationResult:
        """Delete a post"""
        from main import data_store
        
        if post_id not in data_store["posts"]:
            return OperationResult(
                success=False,
                message=f"Post with ID {post_id} not found"
            )
        
        deleted_post = data_store["posts"].pop(post_id)
        
        return OperationResult(
            success=True,
            message=f"Post '{deleted_post['title']}' deleted successfully",
            data=post_id
        )
    
    @strawberry.mutation
    async def simulate_slow_operation(self, delay: int = 2) -> OperationResult:
        """Simulate a slow operation for testing"""
        from main import config
        
        if delay > config.MAX_SLOW_OPERATION_DELAY:
            return OperationResult(
                success=False,
                message=f"Maximum delay is {config.MAX_SLOW_OPERATION_DELAY} seconds"
            )
        
        await asyncio.sleep(delay)
        
        return OperationResult(
            success=True,
            message=f"Slow operation completed after {delay} seconds",
            data=str(delay)
        )

# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)