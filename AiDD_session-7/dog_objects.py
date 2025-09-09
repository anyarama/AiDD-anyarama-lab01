class Dog: #Parent Class
    #CLASS VARIABLES
    kind = 'canine'         # class variable shared by all instances

    #ATTRIBUTES a.k.a. INSTANCE VARIABLES
    def __init__(self, name="", petShop_price=0.00): #(__init__ is a RESERVED method)
        if name == "": 
            print("I am sad. I don't have a name. :^(")
        self.name = name    # instance variable unique to each instance
        self.tricks = []    # instance variable unique to each instance
        self.price = petShop_price

    #METHOD #1 -- Create a method that allows a programer to easily add a trick
    def add_trick(self, trick):
        if trick not in self.tricks:
            self.tricks.append(trick)
        else:
            print("The dog already knows that trick")

    #METHOD #2 - Create a method that allows a programer to easily print the list
    def list_tricks(self):
        print(self.name + "'s tricks include")
        for trick in self.tricks:
            print(" > ", trick)

    #METHOD #3 (__str__ is a RESERVED method) -- Allows you to "print" this variable
    def __str__(self):
        return self.name + " is a good boy/girl!!!" + \
               " His/her price is " + str(self.price) + ".\n"

    #METHOD #4 - Create a METHOD that return the price but addes a $ in front of it.
    def format_price(self):
        return "$" + str(round(self.price,2))

    #METHOD #5 - Create a METHOD that return the price but addes a $ in front of it.
    def discountPrice(self):
        return round(self.price * .9,2)





########################################################
# Create a new subclass FAMILYPET
########################################################
class FamilyPet(Dog): #Child Class
  
    #Run the Dog parent CONSTRUCTOR
    #Notice that this subclass has an ADDITIONAL ATTRIBUTE (nickName)
    def __init__(self, name="", petShop_price=0.00, pNickName="Buddy"):
        Dog.__init__(self, name, petShop_price)
        self.nickName = pNickName #Add the extra or different variables


    #OVERRIDE the default print statement
    def __str__(self):
        return self.name + " is a good family pet!!!" + \
        " His/her price is " + str(self.price) + "." \
        " His/her nickname is " + self.nickName + ".\n"


########################################################
# Create a new subclass SHOWDOG
########################################################
class ShowDog(Dog): #Child Class
  
    #Run the Dog parent CONSTRUCTOR
    #Notice that this subclass has an ADDITIONAL ATTRIBUTE (ShowID)
    def __init__(self, name="", petShop_price=0.00, pShowID="9999"):
        Dog.__init__(self, name, petShop_price)
        self.ShowID = pShowID #Add the extra or different variables


    #OVERRIDE the default print statement
    def __str__(self):
        return self.name + " is a very good looking dog!!!"+ \
                " His/her price is " + str(self.price) + "." \
                " His/her ID is " + str(self.ShowID) + ".\n"


###############################################################
# UNIT TEST EXAMPLE for dog class
###############################################################
if __name__ == "__main__":
    # 1. Create a Dog
    my_dog = Dog(name="Rex", petShop_price=500.00)
    print()

    # 2. Does this dog have a name?
    print("The dog's name is", my_dog.name)
    print()
    
    # 3. Does this dog have a price?
    print("The dog's price is", my_dog.price)
    print()

    # 4. The dog should not know any tricks yet
    print("The number of trick's known by the dog is", len(my_dog.tricks))
    print()

    # 5. Add 1 trick to the dog
    #    Why not use my_dog.tricks.append("Sit")
    my_dog.add_trick("Sit")
    my_dog.add_trick("Shake Hands/Paws")

    # 6. The dog should know 2 trick
    my_dog.list_tricks()
    print()

    #7. Print the default __str__ for the dog
    print(my_dog)
    
    # 8. Print a formatted version of the price
    print(my_dog.format_price())
    print()

    # 9. Print the discounted price for the dog
    print(my_dog.discountPrice())
    print()

'''
#############################################################################
#  FULL UNIT TEST
#############################################################################

# Function to simulate assertion by printing success or failure
def check(condition, success_message, failure_message):
    if condition:
        print(success_message)
    else:
        print(f"Test failed: {failure_message}")

# Test the Dog, FamilyPet, and ShowDog classes
def test_dog_initialization():
    dog = Dog(name="Rex", petShop_price=500.00)
    check(dog.name == "Rex", "test_dog_initialization: Name check passed.", f"Expected 'Rex', but got {dog.name}")
    check(dog.price == 500.00, "test_dog_initialization: Price check passed.", f"Expected 500.00, but got {dog.price}")
    check(dog.tricks == [], "test_dog_initialization: Tricks list check passed.", f"Expected empty tricks list, but got {dog.tricks}")

def test_dog_str():
    dog = Dog(name="Rex", petShop_price=500.00)
    expected_str = "Rex is a good boy/girl!!! His/her price is 500.0.\n"
    check(str(dog) == expected_str, "test_dog_str passed.", f"Unexpected __str__ output: {str(dog)}")

def test_add_trick():
    dog = Dog(name="Rex")
    dog.add_trick("Sit")
    check("Sit" in dog.tricks, "test_add_trick: Add trick passed.", f"Expected 'Sit' in {dog.tricks}")
    dog.add_trick("Sit")  # Test if trick is added only once
    check(len(dog.tricks) == 1, "test_add_trick: Duplicate trick prevention passed.", f"Expected tricks length 1, but got {len(dog.tricks)}")

def test_format_price():
    dog = Dog(name="Rex", petShop_price=500.00)
    check(dog.format_price() == "$500.0", "test_format_price passed.", f"Expected '$500.0', but got {dog.format_price()}")

def test_discount_price():
    dog = Dog(name="Rex", petShop_price=500.00)
    check(dog.discountPrice() == 450.00, "test_discount_price passed.", f"Expected 450.00, but got {dog.discountPrice()}")

def test_family_pet_initialization():
    familypet = FamilyPet(name="Buddy", petShop_price=300.00, pNickName="Bud")
    check(familypet.name == "Buddy", "test_family_pet_initialization: Name check passed.", f"Expected 'Buddy', but got {familypet.name}")
    check(familypet.nickName == "Bud", "test_family_pet_initialization: Nickname check passed.", f"Expected 'Bud', but got {familypet.nickName}")
    expected_str = "Buddy is a good family pet!!! His/her price is 300.0. His/her nickname is Bud.\n"
    check(str(familypet) == expected_str, "test_family_pet_initialization: __str__ check passed.", f"Unexpected __str__ output: {str(familypet)}")

def test_show_dog_initialization():
    showdog = ShowDog(name="Champion", petShop_price=1000.00, pShowID="CH1234")
    check(showdog.name == "Champion", "test_show_dog_initialization: Name check passed.", f"Expected 'Champion', but got {showdog.name}")
    check(showdog.ShowID == "CH1234", "test_show_dog_initialization: ShowID check passed.", f"Expected 'CH1234', but got {showdog.ShowID}")
    expected_str = "Champion is a very good looking dog!!! His/her price is 1000.0. His/her ID is CH1234.\n"
    check(str(showdog) == expected_str, "test_show_dog_initialization: __str__ check passed.", f"Unexpected __str__ output: {str(showdog)}")

# Run the simplified tests without using assert
if __name__ == "__main__":
    test_dog_initialization()
    test_dog_str()
    test_add_trick()
    test_format_price()
    test_discount_price()
    test_family_pet_initialization()
    test_show_dog_initialization()
    print("All simplified tests completed.")

'''