
import sys
import random

def miller_rabin_test(n, k=5):  # Number of iterations
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as d * 2^r + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    def is_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(r):
            if pow(a, 2**i * d, n) == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if is_composite(a):
            return False

    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python M00AIE000.py <number>")
        return

    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    if miller_rabin_test(number):
        print(1)
    else:
        print(0)

if __name__ == "main":
    main()
