"""
Examples of Counter and LRU Cache with Python dictionaries.

1. collections.Counter - Count occurrences of elements
2. @lru_cache - Cache function results (memoization)
"""

from collections import Counter
from functools import lru_cache
import time


# ============================================================================
# 1. collections.Counter - Counting Dictionary Elements
# ============================================================================

def counter_examples():
    """Examples of using Counter for dictionary-like operations."""
    
    print("=" * 60)
    print("1. collections.Counter Examples")
    print("=" * 60)
    
    # Example 1: Count characters in a string
    text = "hello world"
    char_count = Counter(text)
    print(f"\n📝 Count characters in '{text}':")
    print(f"   {dict(char_count)}")
    print(f"   Most common: {char_count.most_common(3)}")
    
    # Example 2: Count items in a list
    items = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    item_count = Counter(items)
    print(f"\n🍎 Count items in list: {items}")
    print(f"   {dict(item_count)}")
    print(f"   Apple count: {item_count['apple']}")
    print(f"   Total items: {sum(item_count.values())}")
    
    # Example 3: Count from a dictionary
    word_freq = {'hello': 3, 'world': 2, 'python': 5}
    counter_from_dict = Counter(word_freq)
    print(f"\n📚 Counter from dict: {word_freq}")
    print(f"   {dict(counter_from_dict)}")
    
    # Example 4: Counter operations (add, subtract, update)
    counter1 = Counter({'a': 3, 'b': 2, 'c': 1})
    counter2 = Counter({'a': 1, 'b': 3, 'd': 2})
    
    print(f"\n➕ Counter operations:")
    print(f"   Counter1: {dict(counter1)}")
    print(f"   Counter2: {dict(counter2)}")
    print(f"   Addition: {dict(counter1 + counter2)}")
    print(f"   Subtraction: {dict(counter1 - counter2)}")
    print(f"   Intersection (min): {dict(counter1 & counter2)}")
    print(f"   Union (max): {dict(counter1 | counter2)}")
    
    # Example 5: Count dictionary values
    data = {
        'user1': 'active',
        'user2': 'inactive',
        'user3': 'active',
        'user4': 'active',
        'user5': 'inactive'
    }
    status_count = Counter(data.values())
    print(f"\n👥 Count status values:")
    print(f"   Data: {data}")
    print(f"   Status counts: {dict(status_count)}")
    
    # Example 6: Count nested dictionary values
    nested_data = {
        'group1': {'status': 'active', 'type': 'premium'},
        'group2': {'status': 'active', 'type': 'basic'},
        'group3': {'status': 'inactive', 'type': 'premium'},
        'group4': {'status': 'active', 'type': 'premium'}
    }
    status_counter = Counter(item['status'] for item in nested_data.values())
    type_counter = Counter(item['type'] for item in nested_data.values())
    print(f"\n📊 Count nested dict values:")
    print(f"   Status: {dict(status_counter)}")
    print(f"   Type: {dict(type_counter)}")


# ============================================================================
# 2. @lru_cache - Caching Dictionary Operations
# ============================================================================

# Example 1: Cache expensive dictionary lookups
@lru_cache(maxsize=128)
def expensive_dict_lookup(key: str) -> dict:
    """
    Simulate expensive dictionary lookup with caching.
    
    This function would normally query a database or API,
    but with @lru_cache, results are cached.
    """
    # Simulate slow operation
    time.sleep(0.1)
    return {
        'id': key,
        'name': f'User_{key}',
        'data': f'Some expensive data for {key}'
    }


# Example 2: Cache dictionary transformations
@lru_cache(maxsize=256)
def transform_dict(data_tuple: tuple) -> dict:
    """
    Transform dictionary with caching.
    
    Note: @lru_cache requires hashable arguments,
    so we pass dict items as a tuple.
    """
    # Convert tuple back to dict
    data = dict(data_tuple)
    # Simulate expensive transformation
    time.sleep(0.05)
    return {
        k.upper(): v * 2 if isinstance(v, (int, float)) else v
        for k, v in data.items()
    }


# Example 3: Cache dictionary key generation
@lru_cache(maxsize=64)
def generate_dict_key(prefix: str, suffix: str) -> str:
    """Generate dictionary key with caching."""
    # Simulate expensive key generation
    time.sleep(0.02)
    return f"{prefix}_{suffix}_{hash(prefix + suffix)}"


# Example 4: Cache dictionary validation
@lru_cache(maxsize=512)
def validate_dict_structure(data_tuple: tuple) -> bool:
    """Validate dictionary structure with caching."""
    data = dict(data_tuple)
    required_keys = {'name', 'email', 'age'}
    return required_keys.issubset(data.keys())


def lru_cache_examples():
    """Examples of using @lru_cache with dictionaries."""
    
    print("\n" + "=" * 60)
    print("2. @lru_cache Examples")
    print("=" * 60)
    
    # Example 1: Expensive dictionary lookup
    print("\n🔍 Expensive dictionary lookup (first call is slow, cached calls are fast):")
    
    start = time.time()
    result1 = expensive_dict_lookup("user123")
    time1 = time.time() - start
    print(f"   First call: {time1:.4f}s - {result1}")
    
    start = time.time()
    result2 = expensive_dict_lookup("user123")  # Cached!
    time2 = time.time() - start
    print(f"   Cached call: {time2:.4f}s - {result2}")
    print(f"   Speedup: {time1/time2:.1f}x faster!")
    
    # Example 2: Dictionary transformation caching
    print("\n🔄 Dictionary transformation caching:")
    test_dict = {'a': 1, 'b': 2, 'c': 3}
    dict_tuple = tuple(test_dict.items())
    
    start = time.time()
    transformed1 = transform_dict(dict_tuple)
    time1 = time.time() - start
    print(f"   First transform: {time1:.4f}s - {transformed1}")
    
    start = time.time()
    transformed2 = transform_dict(dict_tuple)  # Cached!
    time2 = time.time() - start
    print(f"   Cached transform: {time2:.4f}s - {transformed2}")
    
    # Example 3: Dictionary key generation
    print("\n🔑 Dictionary key generation caching:")
    keys = []
    for i in range(5):
        key = generate_dict_key("prefix", f"suffix{i}")
        keys.append(key)
    
    print(f"   Generated keys: {keys}")
    print(f"   Cache info: {generate_dict_key.cache_info()}")
    
    # Example 4: Dictionary validation caching
    print("\n✅ Dictionary validation caching:")
    test_data1 = {'name': 'John', 'email': 'john@example.com', 'age': 30}
    test_data2 = {'name': 'Jane', 'email': 'jane@example.com', 'age': 25}
    
    tuple1 = tuple(test_data1.items())
    tuple2 = tuple(test_data2.items())
    
    result1 = validate_dict_structure(tuple1)
    result2 = validate_dict_structure(tuple2)
    result1_cached = validate_dict_structure(tuple1)  # Cached!
    
    print(f"   Data1 valid: {result1}")
    print(f"   Data2 valid: {result2}")
    print(f"   Data1 cached: {result1_cached}")
    print(f"   Cache info: {validate_dict_structure.cache_info()}")


# ============================================================================
# 3. Combined Example: Counter + LRU Cache
# ============================================================================

@lru_cache(maxsize=100)
def count_dict_values_cached(data_tuple: tuple) -> dict:
    """
    Count dictionary values with caching.
    
    This combines Counter with caching for frequently accessed data.
    """
    data = dict(data_tuple)
    counter = Counter(data.values())
    return dict(counter)


def combined_example():
    """Example combining Counter and LRU cache."""
    
    print("\n" + "=" * 60)
    print("3. Combined: Counter + @lru_cache")
    print("=" * 60)
    
    # Simulate frequently accessed dictionary
    user_statuses = {
        f'user{i}': 'active' if i % 2 == 0 else 'inactive'
        for i in range(10)
    }
    
    print(f"\n📊 User statuses: {user_statuses}")
    
    # First call (computes)
    start = time.time()
    counts1 = count_dict_values_cached(tuple(user_statuses.items()))
    time1 = time.time() - start
    
    # Second call (cached)
    start = time.time()
    counts2 = count_dict_values_cached(tuple(user_statuses.items()))
    time2 = time.time() - start
    
    print(f"   Status counts: {counts1}")
    print(f"   First call: {time1:.6f}s")
    print(f"   Cached call: {time2:.6f}s")
    print(f"   Cache info: {count_dict_values_cached.cache_info()}")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    counter_examples()
    lru_cache_examples()
    combined_example()
    
    print("\n" + "=" * 60)
    print("✅ All examples complete!")
    print("=" * 60)

