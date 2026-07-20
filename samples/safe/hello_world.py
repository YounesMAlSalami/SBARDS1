#!/usr/bin/env python3
# Safe hello world script

def main():
    """Simple hello world function"""
    print("Hello, World!")
    print("This is a completely safe Python script")
    print("It contains no malicious code or suspicious patterns")
    
    # Print some information about Python
    import sys
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Calculate and print the first 10 Fibonacci numbers
    print("\nFirst 10 Fibonacci numbers:")
    a, b = 0, 1
    for i in range(10):
        print(a, end=" ")
        a, b = b, a + b
    print()

if __name__ == "__main__":
    main()
