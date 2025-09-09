"""grocery.py

Defines the Grocery class as a subclass of Store, demonstrating inheritance, method overriding,
and the use of super() to call parent class methods.
"""
# Import all classes located in the store2.py file
from store2 import *


# Create a CHILD CLASS called Grocery. Use the orginal Store CLASS as the PARENT CLASS
class Grocery (Store):
    """A subclass of Store representing a grocery store with a specific location."""

    # Create the CONSTRUCTOR
    def __init__(self, name, sales, locval):
        # Let's NOT re-write the code from the parent code
        #self.name       = aname
        #self.totalsales = asales
        #self._numempl    = 0
        #self._managementTeam = []
        # Instead let's call "super().__init__(name, sales)
        super().__init__(name, sales)
        # Then let's add 1 new variables called "location"
        self.location = locval

    #Write Property Decorators for the new variable
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, locval):
        self._location = "Grocery location is " + locval

    #Let's OVERWRITE the old increaseSales() function
    # Keep in mind this ONLY applies to Grovery objects and NOT Store objects
    # Whatever they type increase it by 10% first
    def increaseSales(self, saleval):
        self._totalsales = self._totalsales + 1.10 * saleval

    #Let's OVERWRITE the old __str__() function
    # Keep in mind this ONLY applies to Grovery objects and NOT Store objects
    def __str__(self):
        return super().__str__() + "\n" + self.location