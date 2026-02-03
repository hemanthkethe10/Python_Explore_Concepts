#!/usr/bin/env python3
"""
Rate Limit Testing Script
Test the rate limiting functionality of the Explore Server
"""

import requests
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class RateLimitTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_endpoint_rate_limit(self, endpoint, method="GET", data=None, expected_limit=10):
        """
        Test rate limiting for a specific endpoint
        
        Args:
            endpoint (str): API endpoint to test
            method (str): HTTP method
            data (dict): Request data for POST/PUT requests
            expected_limit (int): Expected rate limit per minute
        """
        print(f"\n{'='*60}")
        print(f"Testing Rate Limit: {method} {endpoint}")
        print(f"Expected Limit: {expected_limit} requests/minute")
        print(f"{'='*60}")
        
        url = f"{self.base_url}{endpoint}"
        successful_requests = 0
        rate_limited_requests = 0
        
        # Make requests rapidly to trigger rate limit
        for i in range(expected_limit + 5):  # Try 5 more than the limit
            try:
                if method.upper() == "GET":
                    response = self.session.get(url)
                elif method.upper() == "POST":
                    response = self.session.post(url, json=data or {})
                elif method.upper() == "PUT":
                    response = self.session.put(url, json=data or {})
                elif method.upper() == "DELETE":
                    response = self.session.delete(url)
                
                if response.status_code == 200 or response.status_code == 201:
                    successful_requests += 1
                    print(f"✓ Request {i+1}: Success (Status: {response.status_code})")
                elif response.status_code == 429:
                    rate_limited_requests += 1
                    print(f"✗ Request {i+1}: Rate Limited (Status: {response.status_code})")
                    retry_after = response.headers.get('Retry-After', 'Not specified')
                    print(f"  Retry-After: {retry_after}")
                else:
                    print(f"? Request {i+1}: Unexpected Status {response.status_code}")
                
                # Small delay to avoid overwhelming the server
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Request {i+1}: Error - {e}")
        
        print(f"\nResults:")
        print(f"  Successful requests: {successful_requests}")
        print(f"  Rate limited requests: {rate_limited_requests}")
        print(f"  Expected successful: ~{expected_limit}")
        
        return successful_requests, rate_limited_requests
    
    def test_concurrent_requests(self, endpoint, num_threads=5, requests_per_thread=3):
        """
        Test rate limiting with concurrent requests from multiple threads
        """
        print(f"\n{'='*60}")
        print(f"Testing Concurrent Rate Limiting: {endpoint}")
        print(f"Threads: {num_threads}, Requests per thread: {requests_per_thread}")
        print(f"{'='*60}")
        
        def make_requests(thread_id):
            results = []
            for i in range(requests_per_thread):
                try:
                    response = requests.get(f"{self.base_url}{endpoint}")
                    results.append({
                        'thread_id': thread_id,
                        'request_num': i + 1,
                        'status_code': response.status_code,
                        'timestamp': datetime.now().isoformat()
                    })
                    time.sleep(0.1)
                except Exception as e:
                    results.append({
                        'thread_id': thread_id,
                        'request_num': i + 1,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
            return results
        
        # Execute concurrent requests
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_requests, i) for i in range(num_threads)]
            all_results = []
            
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        # Analyze results
        successful = sum(1 for r in all_results if r.get('status_code') == 200)
        rate_limited = sum(1 for r in all_results if r.get('status_code') == 429)
        errors = sum(1 for r in all_results if 'error' in r)
        
        print(f"\nConcurrent Request Results:")
        print(f"  Total requests: {len(all_results)}")
        print(f"  Successful: {successful}")
        print(f"  Rate limited: {rate_limited}")
        print(f"  Errors: {errors}")
        
        return all_results
    
    def test_rate_limit_recovery(self, endpoint, wait_time=65):
        """
        Test that rate limits reset after the time window
        """
        print(f"\n{'='*60}")
        print(f"Testing Rate Limit Recovery: {endpoint}")
        print(f"Wait time: {wait_time} seconds")
        print(f"{'='*60}")
        
        # First, trigger rate limit
        print("Phase 1: Triggering rate limit...")
        for i in range(15):  # Should trigger rate limit
            response = self.session.get(f"{self.base_url}{endpoint}")
            if response.status_code == 429:
                print(f"✓ Rate limit triggered at request {i+1}")
                break
            time.sleep(0.1)
        
        # Wait for rate limit to reset
        print(f"\nPhase 2: Waiting {wait_time} seconds for rate limit reset...")
        time.sleep(wait_time)
        
        # Test if rate limit has reset
        print("Phase 3: Testing if rate limit has reset...")
        response = self.session.get(f"{self.base_url}{endpoint}")
        
        if response.status_code == 200:
            print("✓ Rate limit successfully reset - request succeeded")
            return True
        elif response.status_code == 429:
            print("✗ Rate limit still active - request failed")
            return False
        else:
            print(f"? Unexpected status code: {response.status_code}")
            return False
    
    def run_comprehensive_test(self):
        """
        Run a comprehensive test of all endpoints and their rate limits
        """
        print("🚀 Starting Comprehensive Rate Limit Testing")
        print("=" * 80)
        
        # Test different endpoints with their expected limits
        test_cases = [
            ("/", "GET", None, 10),
            ("/health", "GET", None, 30),
            ("/api/users", "GET", None, 20),
            ("/api/users", "POST", {"name": "Test User", "email": "test@example.com"}, 5),
            ("/api/stats", "GET", None, 15),
            ("/api/rate-limit-info", "GET", None, 60),
        ]
        
        results = {}
        
        for endpoint, method, data, expected_limit in test_cases:
            try:
                successful, rate_limited = self.test_endpoint_rate_limit(
                    endpoint, method, data, expected_limit
                )
                results[f"{method} {endpoint}"] = {
                    'successful': successful,
                    'rate_limited': rate_limited,
                    'expected_limit': expected_limit
                }
                
                # Wait a bit between tests to avoid cross-contamination
                time.sleep(2)
                
            except Exception as e:
                print(f"Error testing {method} {endpoint}: {e}")
                results[f"{method} {endpoint}"] = {'error': str(e)}
        
        # Test concurrent requests
        self.test_concurrent_requests("/", num_threads=3, requests_per_thread=4)
        
        # Summary
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print(f"{'='*80}")
        
        for endpoint, result in results.items():
            if 'error' in result:
                print(f"❌ {endpoint}: ERROR - {result['error']}")
            else:
                success_rate = (result['successful'] / result['expected_limit']) * 100
                print(f"✅ {endpoint}: {result['successful']}/{result['expected_limit']} "
                      f"successful ({success_rate:.1f}%), {result['rate_limited']} rate limited")


def main():
    """
    Main function to run rate limit tests
    """
    print("Rate Limit Testing for Explore Server")
    print("Make sure the server is running at http://localhost:8000")
    print()
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please start the server with: python main.py")
        return
    
    # Initialize tester
    tester = RateLimitTester()
    
    # Run tests
    print("\nChoose test type:")
    print("1. Quick test (single endpoint)")
    print("2. Comprehensive test (all endpoints)")
    print("3. Concurrent request test")
    print("4. Rate limit recovery test")
    
    choice = input("\nEnter choice (1-4) or press Enter for comprehensive test: ").strip()
    
    if choice == "1":
        endpoint = input("Enter endpoint to test (default: /): ").strip() or "/"
        tester.test_endpoint_rate_limit(endpoint)
    
    elif choice == "3":
        endpoint = input("Enter endpoint to test (default: /): ").strip() or "/"
        tester.test_concurrent_requests(endpoint)
    
    elif choice == "4":
        endpoint = input("Enter endpoint to test (default: /): ").strip() or "/"
        print("⚠️  This test will take about 65 seconds...")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            tester.test_rate_limit_recovery(endpoint)
    
    else:  # Default to comprehensive test
        tester.run_comprehensive_test()
    
    print("\n🎉 Testing completed!")


if __name__ == "__main__":
    main()