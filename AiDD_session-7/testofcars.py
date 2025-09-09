from cars import *

# Set a couple of variables to be used below
distance = 2.0
gallons = 2

#Create an empty list of cars
mycars = []

# INSTANTIATE the OBJECT while you are appending it to the mycars Python List
print("Create several cars and add them to a list")
print("==========================================")
mycars.append(Car("Toyota"))
mycars.append(PassCar("VW"))
mycars.append(LuxCar("Audi"))
print("--------------------------------------------")
print("Done creating cars and adding them to a list")
print("--------------------------------------------")
print()

#Change the first car to point to the third car
# This effective "deletes" the first car and now you have the same
# car in the list twice.  Both 0 and 2 point to the same INSTANCE
mycars[0] = mycars[2]

#Call the drive method for each car
mycars[0].drive(distance*2)
mycars[1].drive(distance*2)
mycars[2].drive(distance)

#Refuel the cars
mycars[0].refuel(gallons)
mycars[1].refuel(gallons)
mycars[2].refuel(gallons)

# Did refueling the first car also refuel the thrid car?