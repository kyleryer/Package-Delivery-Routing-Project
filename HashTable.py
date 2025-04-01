class HashTable:

    def __init__(self, size):
        self.size = size
        self.map = [None] * self.size
    
    # Inserts a package into hash table using package ID as key
    def Insert(self, package):
        key = int(package.id) - 1
        value = [package.id, package.address, package.city, package.state, package.zipcode, package.deadline, package.weight, 
                 package.notes, package.status, package.loaded, package.enRouteTime, package.deliveredTime, package.truck]

        self.map[key] = value

        return None
    
    # Looks up a package by ID and returns all package information
    def Get(self, key):
        if  key < 1 or key > self.size:
            return None
        
        if self.map[key - 1][0] == str(key):
            return self.map[key - 1]
        else:
            return None

    # Changes a package's loaded status to "Yes" if that package is loaded onto a truck and specifies which truck package is loaded on
    def Loaded(self, key, truck):
        package = self.map[key - 1]
        package[9] = "Yes"
        package[12] = truck

    # Checks to see if a package has been loaded onto a truck
    def IsLoaded(self, key):
        package = self.map[key - 1]
        if package[9] == "Yes":
            return True
        else:
            return False
    
    # Checks to see if all packages have been loaded onto trucks
    def AllLoaded(self):
        for package in self.map:
            if package[9] == "No":
                return False
        
        return True
    
    # Changes the delivery status of a package    
    def ChangeStatus(self, key, status):
        package = self.map[key - 1]
        package[8] = status

    # Records what time package is en route to its destination and changes its status to "En Route"
    def EnRoute(self, table, key, time):
        package = self.map[key - 1]
        package[10] = time
        table.ChangeStatus(key, "En Route")

    # Records what time package is delivered to its destination and changes its status to "Delivered"
    def Delivered(self, table, key, time):
        package = self.map[key - 1]
        package[11] = time
        table.ChangeStatus(key, f"Delivered at {time}")
     
    def Print(self):
        for item in self.map:
            if item is not None:
                print(item)