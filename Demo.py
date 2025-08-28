# This function below will determine if a number is prime
# I am going to have comments for each line of code
def is_prime(n):
    # Check if the number is less than or equal to 1
    if n <= 1:
        return False
    # Check for factors from 2 to the square root of n
    for i in range(2, int(n**0.5) + 1):
        # If n is divisible by i, it's not prime
        if n % i == 0:
            return False
    # If no factors were found, it's prime
    return True

# This code will test the above function
print(is_prime(11))  # Expected output: True
print(is_prime(4))   # Expected output: False

# 