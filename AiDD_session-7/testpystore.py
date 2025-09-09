"""testpystore.py

Test script for demonstrating the Store and Grocery classes.
Shows object creation, property usage, and basic OOP concepts in action.
"""
#  Import every class from the store.py file and the grocery.py file
from store2 import *
from grocery import *

print("\nWelcome to the Store Application")
print("=" * 50, "\n")

while True:
    try:
        # When prompted try entering "Around the World in 60 Days"
        storeName = input("Enter a store name: ")
        # When prompted try entering a negative number
        totalSales = int(input("Please enter the total sales: "))
        s1 = Store(storeName, totalSales)
        break
    except Exception as error:
        print(error)

# Move the triple quotes down as you move through the demonstration

print("==============================================================")
print("Showing Print Statements for the new Store Object")
print("==============================================================\n")
# Print s1's __str__ output
print("Printing the 'datatype' (technically the CLASS) of s1")
print(type(s1))
print("Note: s1 is a Store object")
print() #Print an empty line to make the output look better

# Now print the name and sales amount directly
print("Printing the name and sales amount directly")
print(s1._name)
print(s1._totalsales)
print("Note: The name is printed in the original format")
print() #Print an empty line to make the output look better

# Now print the name and sales amount using the property
print("Now print the name and sales amount using the property")
print(s1.name)
print(s1.totalsales)
print("Note: The name is printed in UPPERCASE format")
print() #Print an empty line to make the output look better
'''

print("==============================================================")
print("Print statement for Grocery Store 'gs'")
print("==============================================================\n")
# Create a Grocery Store
gs = Grocery("A", 200, "btown")
print() #Print an empty line to make the output look better
print("The location of gs is ...\n", gs.location)
print("Since we automatically added 'Grocery location is' should we add")
print("it again when we print the location? Probably not!\n")
print() #Print an empty line to make the output look better

# Notice the difference between s1 and gs
print("Printing gs. What is the difference between s1 and gs?")
print(gs)
print("Note: When we print a Grocery object it adds the location")
print() #Print an empty line to make the output look better

# Add 500 to the total sales (reminder.. it will be increase by an addition 10% of this value)
print("The orginal sales amount of gs is", gs.totalsales)
gs.increaseSales(500)
print("Printing gs after increasing sales by 500")
print(gs)
print() #Print an empty line to make the output look better

#Change s1 to be gs (s1 is now an alias for gs)
print("Changing s1 to be equal to gs. What does that do?")
s1 = gs
print("Answer: s1 is now an ALIAS for gs. They are the SAME object")
print() #Print an empty line to make the output look better

print("Re-printing the 'datatype' of s1...")
print(type(s1))
print("Answer: s1 is now a Grocery object")
print() #Print an empty line to make the output look better

print("Adding s1 and gs to a list called mylist")
mylist = [s1, gs]
print() #Print an empty line to make the output look better

print("==============================================================")
print("Demonstrating the idea of Polymorphism")
print("==============================================================\n")
print(" Looping through the list of s1 and gs")
print(" --------------------------------------")

#First Add a new Store to the list
s3 = Store("Third Store", 5000)
mylist.append(s3)

# Now loop through the list and print the type and sales amount
# They are not all the same type of object
# The code below demonstrates POLYMORPHISM
count = 1
for item in mylist:
    print(count,"This item is has a type of ", type(item))
    # Print the sales value. It is the same for both Store and Grocery
    print("Sales value of " + item.name + " is", item.totalsales)
    # If the item is a Grocery object print the location
    # We have to check the type first otherwise we will get an error 
    #  where we try to print the location of a Store object.
    #  Store does not have a location variable
    if (type(item) == Grocery):
        print("I am a grocery: " + item.location)
    count += 1
    print()

'''