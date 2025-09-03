from typing import Union, List
#Problem 1
# Palindrome Checker
# The goal of the program below is to determine if a five-digit number is a palindrome. The number is defined
# as n: int. The output should be a boolean value indicating whether n is a palindrome. The output should return either True/ False.
# the program should prompt the user to ask the input five digit number and the program should throw an error if the input is not a five-digit number.


def is_palindrome(n: int) -> bool:
    # Convert the number to a string
    num_str = str(n)
    # Check if the string is equal to its reverse
    return num_str == num_str[::-1]

# Main program
try:
    user_input = int(input("Enter a five-digit number: "))
    if 10000 <= user_input <= 99999:
        print(is_palindrome(user_input))
    else:
        raise ValueError("Input is not a five-digit number.")
except ValueError as e:
    print("Error:", e)



# The updated program now will take both string and numbers and check for palindromes.
# The updated program will now return both reversed string and boolean value indicating whether it is a palindrome.

def is_palindrome(n: Union[int, str]) -> bool:
    # Convert the input to a string
    num_str = str(n)
    # Check if the string is equal to its reverse
    return num_str == num_str[::-1]

# below program is the input/output logic for the updated program.
# The updated program will now handle both string and integer inputs.
# The program now will not check for five-digit numbers specifically.
try:
    user_input = input("Enter a string or a number: ")
    reversed_input = str(user_input)[::-1]
    if user_input.isdigit():
        user_input = int(user_input)
    palindrome_result = is_palindrome(user_input)
    print(f"Reversed: {reversed_input}")
    print(f"Is palindrome: {palindrome_result}")
except ValueError as e:
    print("Error:", e)


# Problem 2 - Diamond Star Pattern (using fixed-width font for alignment)
# Method 1. Using brute force
# The pseudocode below is a brute force method for printing a diamond star pattern where I will not be using any functions or iterations.
# the pseudocode below is just the first half of the pattern.
print("     *")
print("    * *")
print("   * * *")
print("  * * * *")
print(" * * * * *")
# the pseudocode below is the second half of the pattern.
print(" * * * * *")
print("  * * * *")
print("   * * *")
print("    * *")
print("     *")

# Method 2. Using nested loops.
# The updated program below will print the same complete diamond star pattern with nested loops
# Problem 2 - Diamond Star Pattern using nested loops (no string multiplication)

rows = 5

# Top half of diamond
for i in range(1, rows + 1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()

# Bottom half of diamond
for i in range(rows-1, 0, -1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()


# Method 3. Using string multiplication
# The updated program below will print the same diamond star pattern using string multiplication technique that looks like this: (" " * n + "* " * k).

rows = 5

# Top half of diamond
for i in range(1, rows + 1):
    print(" " * (rows - i) + "* " * i)

# Bottom half of diamond
for i in range(rows-1, 0, -1):
    print(" " * (rows - i) + "* " * i)


# The updated generalised program below will print the same diamond star pattern for any odd number 'n' that was given as an input from the user.
# The program should not take the input if it is not an odd number.

# Generalised Diamond Star Pattern for any odd number 'n'

n = int(input("Enter an odd number: "))
if n % 2 == 1 and n > 0:
    for i in range(1,n+1):
        print(" " * (n - i) + "* " * i)
    for i in range(n-1,0,-1):
        print(" " * (n - i) + "* " * i)

else:
    print("Input is not an odd number.")


# Problem 3 - Salary Doubling
# The goal of the program is to calculate the daily earning starting at 1 penny and doubling it every day.
# The program contains the function daily_salary(days: int)-> List[int] that takes the number of days as input and returns a list of daily earnings for each day.
# The program should prompt the user to ask the number of days and the program should throw an error if the input is not a positive integer.


def daily_salary(days: int) -> List[int]:
    salaries = []
    dollar = 1
    for _ in range(days):
        salaries.append(dollar)
        dollar *= 2
    return salaries

try:
    num_days = int(input("Enter the number of days: "))
    if num_days > 0:
        earnings = daily_salary(num_days)
        print("Daily earnings in dollars:", earnings)
    else:
        raise ValueError("Input is not a positive integer.")
except ValueError as e:
    print("Error:", e)

# Can I use bit shifting (<<) to double salary values instead of multiplication?
# AI output: Yes, you can use bit shifting (<<) to double salary values instead of multiplication. 
# In Python, dollar << 1 is equivalent to dollar * 2. Both methods will work for doubling integer values.
# Updated code
def daily_salary(days: int) -> List[int]:
    salaries = []
    dollar = 1
    for _ in range(days):
        salaries.append(dollar)
        dollar = dollar << 1
    return salaries

try:
    num_days = int(input("Enter the number of days: "))
    if num_days > 0:
        earnings = daily_salary(num_days)
        print("Daily earnings in dollars:", earnings)
    else:
        raise ValueError("Input is not a positive integer.")
except ValueError as e:
    print("Error:", e)


'''
For problem 1: Palindrome Checker

The goal of the program below is to determine if a five-digit number is a palindrome. The number is defined
as n: int. The output should be a boolean value indicating whether n is a palindrome. The output should return either True/ False.
the program should prompt the user to ask the input five digit number and the program should throw an error if the input is not a five-digit number.
 The copilot suggested the function is_palindrome(n: int) -> bool: that I have used. No changes done. I have accepted the suggestion.
 I have implemeted the I/O logic by myself adjusting to the function the copilot have given:

 try:
    user_input = int(input("Enter a five-digit number: "))
    if 10000 <= user_input <= 99999:
        print(is_palindrome(user_input))
    else:
        raise ValueError("Input is not a five-digit number.")
except ValueError as e:
    print("Error:", e)

For the second part of the program. I wanted the function to take both int and str data type. The prompt I have given now is:
"The updated program now will take both string and numbers and check for palindromes.
The updated program will now return both reversed string and boolean value indicating whether it is a palindrome.
The updated program will now handle both string and integer inputs.
The program now will not check for five-digit numbers specifically."

Copilot initially gave me this function:

def is_palindrome(n: int | str) -> bool:
    num_str = str(n)
    return num_str == num_str[::-1]

but this program is throwing an error when I input a value. Because this type: int|str is only supported in Python 3.10 and above. 
Then the copilot has suggested me a fix, to use Union from the typing module for compatibility:

from typing import Union

def is_palindrome(n: Union[int, str]) -> bool:
    num_str = str(n)
    return num_str == num_str[::-1]

    
For problem 2: Diamond star pattern
I have written the brute force pseudo code myself. 

For method 2: Using nested loops, the prompt I have given is:
The updated program below will print the same complete diamond star pattern with nested loops
Problem 2 - Diamond Star Pattern using nested loops (no string multiplication)

The program , copilot given me is this
rows = 5

# Top half of diamond
for i in range(1, rows + 1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()

# Bottom half of diamond
for i in range(rows, 0, -1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()

But the problem with the program is when i run it, the center part of the program have two lines of equal astrisk pattern:
    * 
   * * 
  * * * 
 * * * * 
* * * * * --->1
* * * * * ---> 2
 * * * * 
  * * * 
   * * 
    * 

I have edited the latter part of the program to add -1 to the program.
'for i in range(rows-1, 0, -1)'. The updated program is:

rows = 5

# Top half of diamond
for i in range(1, rows + 1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()

# Bottom half of diamond
for i in range(rows-1, 0, -1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print stars with spaces
    for j in range(i):
        print("* ", end="")
    print()
One thing I noticed was that the copilot kept giving out same logic for bottom part of the pattern.
'for i in range(n,0,-1):'
So I had to keep editing to add -1 in the range.

For Method 3. Using string multiplication
The prompt I have given is:
"The updated program below will print the same diamond star pattern using string multiplication technique that looks like this: (" " * n + "* " * k)."
I have accepted what copilot has given me by making a small change of adding -1 in the range for the bottom half of the diamond.

I have written the generalised program myself where the user can input any odd number and the program will generate a diamond pattern based on that number.

n = int(input("Enter an odd number: "))
if n % 2 == 1 and n > 0:
    for i in range(1,n+1):
        print(" " * (n - i) + "* " * i)
    for i in range(n-1,0,-1):
        print(" " * (n - i) + "* " * i)

else:
    print("Input is not an odd number.")



For Problem 3 - Salary Doubling
the prompt I have given is:
"The goal of the program is to calculate the daily earning starting at 1 penny and doubling it every day.
The program contains the function daily_salary(days: int)-> List[int] that takes the number of days as input and returns a list of daily earnings for each day.
The program should prompt the user to ask the number of days and the program should throw an error if the input is not a positive integer."
The function that copilot given me is:

def daily_salary(days: int) -> List[int]:
    salaries = []
    dollar = 1
    for _ in range(days):
        salaries.append(dollar)
        dollar *= 2
    return salaries


I then asked copilot if I can use bit shifting:

AI Prompt: Can I use bit shifting (<<) to double salary values instead of multiplication?

copilot output: Yes, you can use bit shifting (<<) to double salary values instead of multiplication. 
In Python, dollar << 1 is equivalent to dollar * 2. Both methods will work for doubling integer values.
Copilot has advised to replace "dollar *= 2" with "dollar = dollar << 1"

I have later toyed with copilot and asked couple of questions:

AI Prompt 1: Does this program work efficiently and quickly when the number of days is large? Like 30?

AI Response:
"Yes, the program is efficient and can handle large numbers of days, such as 30, without any performance issues.
The use of bit shifting (<<) for doubling the dollar value is a fast operation, and the overall time complexity is O(n),
where n is the number of days. This means the program will run in a reasonable time even for larger inputs."

AI Prompt 2: would you suggest an alternate data type for larger numbers?

AI Response:
"For larger numbers, especially when dealing with very high values, you might consider using Python's built-in `decimal.Decimal` type from the `decimal` module.
This type provides arbitrary precision and can handle very large numbers more accurately than floating-point representations."




'''