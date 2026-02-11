"""Example usage of the MathOps SDK"""

from mathops import add, subtract, multiply, divide
from mathops import power, factorial, fibonacci


def main():
    print("=== Basic Operations ===")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"20 / 4 = {divide(20, 4)}")
    
    print("\n=== Advanced Operations ===")
    print(f"2^10 = {power(2, 10)}")
    print(f"5! = {factorial(5)}")
    print(f"Fibonacci(10) = {fibonacci(10)}")
    
    print("\n=== Fibonacci Sequence (first 10) ===")
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")


if __name__ == "__main__":
    main()
