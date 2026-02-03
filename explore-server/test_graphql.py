#!/usr/bin/env python3
"""
GraphQL Testing Script
Test GraphQL queries and mutations for the Explore Server
"""

import requests
import json
from datetime import datetime

class GraphQLTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def execute_query(self, query, variables=None):
        """
        Execute a GraphQL query or mutation
        
        Args:
            query (str): GraphQL query or mutation
            variables (dict): Variables for the query
            
        Returns:
            dict: Response data
        """
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            response = self.session.post(self.graphql_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def test_user_queries(self):
        """Test user-related GraphQL queries"""
        print("\n" + "="*60)
        print("Testing User Queries")
        print("="*60)
        
        # Test: Get all users
        query = """
        query GetUsers($limit: Int, $offset: Int) {
            users(limit: $limit, offset: $offset) {
                id
                name
                email
                createdAt
                updatedAt
            }
        }
        """
        
        print("\n1. Testing: Get all users")
        result = self.execute_query(query, {"limit": 5, "offset": 0})
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test: Search users
        search_query = """
        query SearchUsers($query: String!) {
            searchUsers(query: $query) {
                id
                name
                email
            }
        }
        """
        
        print("\n2. Testing: Search users")
        result = self.execute_query(search_query, {"query": "admin"})
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_user_mutations(self):
        """Test user-related GraphQL mutations"""
        print("\n" + "="*60)
        print("Testing User Mutations")
        print("="*60)
        
        # Test: Create user
        create_mutation = """
        mutation CreateUser($userInput: UserInput!) {
            createUser(userInput: $userInput) {
                id
                name
                email
                createdAt
                updatedAt
            }
        }
        """
        
        print("\n1. Testing: Create user")
        user_data = {
            "name": "GraphQL Test User",
            "email": "graphql@example.com"
        }
        result = self.execute_query(create_mutation, {"userInput": user_data})
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Extract user ID for further tests
        user_id = None
        if 'data' in result and result['data']['createUser']:
            user_id = result['data']['createUser']['id']
            print(f"Created user ID: {user_id}")
        
        if user_id:
            # Test: Get specific user
            get_user_query = """
            query GetUser($userId: String!) {
                user(userId: $userId) {
                    id
                    name
                    email
                    createdAt
                    updatedAt
                }
            }
            """
            
            print(f"\n2. Testing: Get user by ID ({user_id})")
            result = self.execute_query(get_user_query, {"userId": user_id})
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # Test: Update user
            update_mutation = """
            mutation UpdateUser($userId: String!, $userInput: UserUpdateInput!) {
                updateUser(userId: $userId, userInput: $userInput) {
                    id
                    name
                    email
                    updatedAt
                }
            }
            """
            
            print(f"\n3. Testing: Update user ({user_id})")
            update_data = {"name": "Updated GraphQL User"}
            result = self.execute_query(update_mutation, {
                "userId": user_id,
                "userInput": update_data
            })
            print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_post_operations(self):
        """Test post-related GraphQL operations"""
        print("\n" + "="*60)
        print("Testing Post Operations")
        print("="*60)
        
        # Test: Create post
        create_post_mutation = """
        mutation CreatePost($postInput: PostInput!) {
            createPost(postInput: $postInput) {
                id
                title
                content
                author
                tags
                createdAt
                updatedAt
            }
        }
        """
        
        print("\n1. Testing: Create post")
        post_data = {
            "title": "GraphQL Test Post",
            "content": "This is a test post created via GraphQL",
            "author": "GraphQL Tester",
            "tags": ["graphql", "test", "api"]
        }
        result = self.execute_query(create_post_mutation, {"postInput": post_data})
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test: Get all posts
        get_posts_query = """
        query GetPosts($author: String, $limit: Int) {
            posts(author: $author, limit: $limit) {
                id
                title
                content
                author
                tags
                createdAt
            }
        }
        """
        
        print("\n2. Testing: Get all posts")
        result = self.execute_query(get_posts_query, {"limit": 10})
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test: Search posts
        search_posts_query = """
        query SearchPosts($query: String!) {
            searchPosts(query: $query) {
                id
                title
                content
                author
                tags
            }
        }
        """
        
        print("\n3. Testing: Search posts")
        result = self.execute_query(search_posts_query, {"query": "GraphQL"})
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_server_stats(self):
        """Test server statistics query"""
        print("\n" + "="*60)
        print("Testing Server Statistics")
        print("="*60)
        
        stats_query = """
        query GetServerStats {
            serverStats {
                totalRequests
                totalUsers
                totalPosts
                usersCreated
                postsCreated
                timestamp
            }
        }
        """
        
        print("\nTesting: Get server statistics")
        result = self.execute_query(stats_query)
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_slow_operation(self):
        """Test slow operation mutation"""
        print("\n" + "="*60)
        print("Testing Slow Operation")
        print("="*60)
        
        slow_mutation = """
        mutation SimulateSlowOperation($delay: Int!) {
            simulateSlowOperation(delay: $delay) {
                success
                message
                data
            }
        }
        """
        
        print("\nTesting: Simulate slow operation (2 seconds)")
        start_time = datetime.now()
        result = self.execute_query(slow_mutation, {"delay": 2})
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"Result: {json.dumps(result, indent=2)}")
        print(f"Actual duration: {duration:.2f} seconds")
    
    def test_complex_query(self):
        """Test a complex GraphQL query with multiple fields"""
        print("\n" + "="*60)
        print("Testing Complex Query")
        print("="*60)
        
        complex_query = """
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
        """
        
        print("\nTesting: Complex query with multiple fields")
        result = self.execute_query(complex_query)
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_error_handling(self):
        """Test GraphQL error handling"""
        print("\n" + "="*60)
        print("Testing Error Handling")
        print("="*60)
        
        # Test: Invalid query
        print("\n1. Testing: Invalid query syntax")
        invalid_query = "query { invalid syntax }"
        result = self.execute_query(invalid_query)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test: Non-existent user
        print("\n2. Testing: Query non-existent user")
        get_user_query = """
        query GetUser($userId: String!) {
            user(userId: $userId) {
                id
                name
                email
            }
        }
        """
        result = self.execute_query(get_user_query, {"userId": "non_existent_user"})
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Test: Invalid mutation input
        print("\n3. Testing: Invalid mutation input")
        create_user_mutation = """
        mutation CreateUser($userInput: UserInput!) {
            createUser(userInput: $userInput) {
                id
                name
                email
            }
        }
        """
        # Missing required fields
        result = self.execute_query(create_user_mutation, {"userInput": {}})
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def run_comprehensive_test(self):
        """Run all GraphQL tests"""
        print("🚀 Starting Comprehensive GraphQL Testing")
        print("=" * 80)
        
        # Check if server is running
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and accessible")
            else:
                print(f"⚠️  Server responded with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to server: {e}")
            print("Please start the server with: python main.py")
            return
        
        # Run all tests
        try:
            self.test_user_queries()
            self.test_user_mutations()
            self.test_post_operations()
            self.test_server_stats()
            self.test_slow_operation()
            self.test_complex_query()
            self.test_error_handling()
            
            print("\n" + "="*80)
            print("🎉 All GraphQL tests completed!")
            print("="*80)
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")


def main():
    """Main function to run GraphQL tests"""
    print("GraphQL Testing for Explore Server")
    print("Make sure the server is running at http://localhost:8000")
    print("GraphQL endpoint: http://localhost:8000/graphql")
    print()
    
    tester = GraphQLTester()
    
    print("Choose test type:")
    print("1. User operations")
    print("2. Post operations")
    print("3. Server statistics")
    print("4. Complex query")
    print("5. Error handling")
    print("6. Comprehensive test (all)")
    
    choice = input("\nEnter choice (1-6) or press Enter for comprehensive test: ").strip()
    
    if choice == "1":
        tester.test_user_queries()
        tester.test_user_mutations()
    elif choice == "2":
        tester.test_post_operations()
    elif choice == "3":
        tester.test_server_stats()
    elif choice == "4":
        tester.test_complex_query()
    elif choice == "5":
        tester.test_error_handling()
    else:  # Default to comprehensive test
        tester.run_comprehensive_test()


if __name__ == "__main__":
    main()