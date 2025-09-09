#IMPORT EACH CLASS
from dog_objects import Dog       #Parent Class
from dog_objects import FamilyPet #Child  Class
from dog_objects import ShowDog   #Child  Class

#Create three different dogs
#Create a "regular" dog (Parent Class)
d1 = Dog("Fido")
d1.price = 100.456
#Add a family pet OBJECT
d2 = FamilyPet("Spot",100,"Buddy")
#Add a ShowDog pet
d3 = ShowDog("Cliford",100,1234)


#Print their names
print("Dog1's name is", d1.name)
print("Family Pet's name is", d2.name)
print("Show dog's name is", d3.name)
print()

print("Family Pet's nickname is", d2.nickName)
print("ShowDog's ID is", d3.ShowID)
print()

#Print what is common about them
print("Dog1 is a", d1.kind)
print("Family Dog is a", d2.kind)
print("Show Dog is a", d3.kind)
print()

#Specify what kinds of tricks each pet knows.
print("Regular Dog's Tricks are ...")
d1.tricks.append("Sit")
d1.add_trick("Stay")
print()

print("Family Dog's Tricks are ...")
d2.add_trick("Roll-over")
d2.add_trick("Beg")
print()

#Option 1 for printing the list of dog tricks
print("Dog1's tricks include:",d1.tricks)
print("Dog2's tricks include:",d2.tricks)
print()

#Option 2 for printing the list of dog tricks
d1.list_tricks()
print()
d2.list_tricks()
print()

#Can we "print" this variable called d1?
#Can a "dog" class object be printed?
print(d1) #Only if we have a __str__ METHOD

#Can we add these dogs to a list?
allDogs = []
allDogs.append(d1)
allDogs.append(d2)
print()

#Print the dogs list
print("Printing  the dogs list does not look very good.")
print(allDogs)
print()

#Print the name of the first dog
print("The first dog in this list is ...", end="")
print(allDogs[0].name)
print()

#Print the tricks that first dog can do
print("The tricks that the first dog can do include...")
print(allDogs[0].tricks)
print()

#Print the tricks that first dog can do using the class method "list_tricks"
print(allDogs[0].list_tricks())
print()

#Print a FORMATTED
print("\nThe formatted price is ...")
print(d1.format_price())
print()

#Print the discount
print("The discounted price is...")
print(d1.discountPrice())
print()

#Print the objects...
print(d1)
print(d2)
print(d3)
