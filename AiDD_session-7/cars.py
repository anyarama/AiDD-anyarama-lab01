# ================================================================
# Create PARENT CLASS
# ================================================================
class Car:

    def __init__(self, somename):
        self.name = somename
        print("I am a car named " + self.name)
        print() # Add a blank line for separation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, somename):
        self._name = somename

    def refuel(self, l):
        print("Give "+ self.name+" "+ str(l)+" gallons of regular gas\n")

    def drive(self, d):
	    print("You drove " + self.name + " "+ str(d) + " miles\n")

# ================================================================
# Create first CHILD CLASS
# ================================================================
class PassCar (Car):

    def __init__(self, somename):
        super().__init__(somename)
        # In addition to the parent printing the name let's reprint it
        self.pname = "Passenger Car named " + somename
        print("I am a " + self.pname)
        print() # Add a blank line for separation

    def drive(self, i):
        print("Drive " + self.name + " " + str(i) + " miles")
        print() # Add a blank line for separation

# ================================================================
#Create second CHILD CLASS
# ================================================================
class LuxCar(Car):

    def __init__(self, somename):
        super().__init__(somename)

    def refuel (self, d):
        print("Give "+ self.name+" "+str(d)+" gallons of premium!")
        print() # Add a blank line for separation
