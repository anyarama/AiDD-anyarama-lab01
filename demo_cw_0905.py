####################################################################
# Iteration #1: Creating the simplest Dog class
####################################################################
'''
print("\nIteration 1\n===============")

# Define a Dog class with two attributes: name and price
class Dog:
    def __init__(self, name = "", petShop_price = 0.00):
        # self is a reference to *this* specific dog object
        self.name = name
        self.price = petShop_price
    
    def __str__(self):
        return f"Dog(name='{self.name}', price={self.price})"
    

# Create two dogs using the constructor
dog1 = Dog()                  # default values: name="", price=0.00
dog2 = Dog("Rex", 100)        # custom values: name="Rex", price=100

# Printing a dog object directly without __str__ looks confusing (memory address)
print("Printing Dog 2:", dog2.__str__())

# Accessing attributes directly
print("Dog 1's name is", dog1.name)
print("Dog 2's name is", dog2.name)

# Explain why print(dog2) shows something like <__main__.Dog object at ...>. 
# Students need to understand that Python doesn’t know how to display 
# objects yet.
'''
####################################################################
#Iteration #2 - Add a list of tricks
####################################################################
print("\nIteration 2\n===============")
class Dog:
    def __init__(self, name = "", petShop_price=0.00):
        self.name = name
        self.price = petShop_price
    
    def __str__(self):
        return f"Dog(name='{self.name}', price={self.price})"
#NEW NEW NEW
        self.tricks = [] 
#NEW NEW NEW

dog1 = Dog()
dog2 = Dog("Rex", 100)

# Try to print the first dog
print("Printing Dog 2:", dog2)

# Try to print the first dog's name variable
#print("Dog 1's name is", dog1.name)

# Try to print the first dog's name variable
#print("Dog 2's name is", dog2.name)
'''
#NEW NEW NEW
dog2.tricks.append("Sit")
dog2.tricks.append("Sit")     # duplicates allowed here
dog2.tricks.append("Beg")
print("Dog 2's tricks are ...", dog2.tricks)
print()
#NEW NEW NEW

# Highlight that lists allow duplicates — do we 
# really want the dog to “know Sit” twice?

####################################################################
#Iteration #3: IMPROVE ON ADDING TRICKS
####################################################################
print("\nIteration 3\n===============")
class Dog:
    def __init__(self, name = "", petShop_price=0.00):
        self.name = name
        self.price = petShop_price
        self.tricks = [] 
    
    #NEW NEW NEW
    def add_trick(self, trick):
        if trick not in self.tricks:
            self.tricks.append(trick)
        else:
            print("The dog already knows that trick")
    #NEW NEW NEW

dog1 = Dog()
dog2 = Dog("Rex", 100)

# Try to print the first dog
#print("Printing Dog 2:", dog2)

# Try to print the first dog's name variable
#print("Dog 1's name is", dog1.name)

# Try to print the first dog's name variable
#print("Dog 2's name is", dog2.name)

#NEW NEW NEW
dog2.add_trick("Sit")       # added
dog2.add_trick("Sit")       # rejected (duplicate)
dog2.add_trick("Beg")       # added
print("Dog 2's tricks are ...", dog2.tricks)
print()
#NEW NEW NEW

# NOTE: This is a good time to emphasize encapsulation — 
#       by creating add_trick(), we protect the internal 
#       state (data) of the object.

####################################################################
#Iteration #4: IMPROVE ON PRINTING DOG
####################################################################
print("\nIteration 4\n===============")
class Dog:
    def __init__(self, name = "", petShop_price=0.00):
        self.name = name
        self.price = petShop_price
        self.tricks = [] 
    
    def add_trick(self, trick):
        if trick not in self.tricks:
            self.tricks.append(trick)
        else:
            print("The dog already knows that trick")
    
    #NEW NEW NEW
    #METHOD #3 (__str__ is a RESERVED method) -- Allows you to "print" this variable
    def __str__(self):
        return self.name + " is a good boy/girl!!!" + \
               " His/her price is " + str(self.price) + ".\n"
    #NEW NEW NEW
        
dog1 = Dog()
dog2 = Dog("Rex", 100)

# Try to print the first dog
print("Printing Dog 2:", dog2)

# Try to print the first dog's name variable
#print("Dog 1's name is", dog1.name)

# Try to print the first dog's name variable
#print("Dog 2's name is", dog2.name)

#dog2.add_trick("Sit")
#dog2.add_trick("Sit")
#dog2.add_trick("Beg")
#print("Dog 2's tricks are ...", dog2.tricks)
#print()

# Explain that __str__ is a special method 
# (a dunder method, double underscore) that makes objects 
# more readable. Show how this improves debugging and usability.
# WE CAN NOW PRINT A DOG!  (kind of)

# We can now have a list of dog objects instead of a list
# of Dictionaries. 
dogs = [
    Dog("Rex", 100),
    Dog("Buddy", 200),
    Dog("Luna", 150)
]
for d in dogs:
    print(d)

'''