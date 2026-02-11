"""Advanced mathematical operations"""


def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent"""
    return base ** exponent


def factorial(n: int) -> int:
    """Calculate factorial of n"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number"""
    if n < 0:
        raise ValueError("Fibonacci not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def printNameAndReturn(name: str):
    return f"Hello from Mathops Updated 11:::: {name}"
