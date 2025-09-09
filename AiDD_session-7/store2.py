"""store2.py

Defines the Store class to demonstrate basic object-oriented programming concepts in Python,
including class variables, instance variables, property decorators, and encapsulation.
"""
# Step 1. Use the class word to create a class. Call this one "Store"
class Store:
    """A class representing a generic store with sales and employee management."""

    #Step 2: Decide if you need CLASS VARIABLES
    # Every OBJECT created from this CLASS shares one copy of this variable
    # If you change the value, it will change for all instances of this CLASS
    parentCompany = "Target"

    #Step 3.  Create a CONSTRUCTOR. ALWAYS called __init__
    # The CONSTRUCTOR is a FUNCTION (a.k.a METHOD) used to initialize the Object (i.e. set intial values)
    # The first parameter is ALWAYS the reserved word "self"
    def __init__( self,     aname, asales):
        # Using _ before the name of the variable tells programmers that they should
        # NOT directly access this variable
        #Step 4. Decide if you need INSTANCE VARIABLES
        
        #Let's look at two ways to set the name
        # Option 1: Directly set the variable (no validation)
        #self._name       = aname
        #Options 2: Use the property setter (with validation)
        self.name       = aname

        self._totalsales = asales
        self._numempl    = 0
        self._managementTeam = []


    #################################################
    #Step 4. SETTER AND GETTER PRESENT DAY PYTHON!!!
    #################################################
    # Property Decorators
    

    # Property for getting the store's name
    @property
    def name(self):
        return self._name.upper()

    # Setter for the store's name with validation
    @name.setter
    def name(self, aname):
        if len(aname) > 15:
            # Note: This will raise an exception if the name is too long!
            # There needs to be a try/except block when setting the name 
            # in the main program. Go check testpystore.py!
            raise Exception("Name cannot exceed 15 characters. Please try again.")
        self._name = aname

    # Property for getting the total sales
    @property
    def totalsales(self):
        return self._totalsales

    # Setter for total sales with validation
    @totalsales.setter
    def totalsales(self, asales):
        if asales < 0:
            raise Exception("Sales cannot be a negative number. Please try a different number.")
        self._totalsales = asales

    # Property for getting the number of employees
    @property
    def numempl(self):
        return self._numempl

    # Setter for the number of employees
    @numempl.setter
    def numempl(self, numberOfEmployees):
        self._numempl = numberOfEmployees


    ##########################################
    # OTHER METHODS TO HELP US WITH THE CLASS
    ##########################################
    # Method to reset total sales to zero
    def resetSales(self):
        self._totalsales = 0

    # Method to increase the value of sales
    def increaseSales(self, saleval):
        self._totalsales = self._totalsales + saleval

    # Method to increase total sales by a given value
    def increaseSales(self, saleval):
        self._totalsales = self._totalsales + saleval

    # Method to replace all managers with a new list
    def setManagers(self, lstOfManagers):
        self._managementTeam = lstOfManagers

    # Method to add/insert a manager to the management team
    def addManager(self, managerName):
        self._managementTeam.append(managerName)

    # Method to display all managers in the management team
    def displayManagers(self):
        for manager in self._managementTeam:
            print(manager)


    # Method to get the list of managers
    def getManagers(self):
        return self._managementTeam

    #There are seveal "special" method like __init__
    # One of those special functions is called __str__
    # __str__ is called when you want to "print" a Store object
    # Generally you should return a nicely formatted string

    # Special method to return a nicely formatted string for the Store object
    def __str__(self):
        return f'Store name: {self._name} \nCurrent Sales: {self._totalsales}'

