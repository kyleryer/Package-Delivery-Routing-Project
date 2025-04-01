from functions import FindNearestNeighbor, GetHours, GetMinutes, GetAMPM 

class Truck:
    
    def __init__(self, capacity, speed, number):
        self.packagelist = []
        self.mileage = 0
        self.capacity = capacity
        self.speed = speed
        self.number = number
        self.starttime = None
        self.endtime = None

    # Loads a package onto the truck
    def Load(self, id):
        if len(self.packagelist) < self.capacity:
            self.packagelist.append(id)
        else:
            return "Max capacity reached"
        
    # Finds package in package list that is closest to the hub location and places package at the front of the list
    def ClosestToHub(self, matrix):
        closestPackage = None
        closestPackageIndex = None
        closestDistance = None

        for index, package in enumerate(self.packagelist):
            distanceToHub = float(matrix[0][int(package)])
            if closestDistance is None:
                closestDistance = distanceToHub
                closestPackage = package
                closestPackageIndex = index
            else:
                if distanceToHub < closestDistance:
                    closestDistance = distanceToHub
                    closestPackage = package
                    closestPackageIndex = index

        tmp = self.packagelist[0]
        self.packagelist[0] = closestPackage
        self.packagelist[closestPackageIndex] = tmp

    # Load unloaded packages that are closest distance away from last package in package list until max capacity
    def NearestNeighborLoad(self, table, matrix):  
        while len(self.packagelist) < self.capacity and table.AllLoaded() == False:
            length = len(self.packagelist)
            currentPackage = self.packagelist[length - 1]

            nearestNeighbor = FindNearestNeighbor(currentPackage, table, matrix)

            self.Load(nearestNeighbor)
            table.Loaded(int(nearestNeighbor), self.number)
        
    # Initiates package delivery of all packages loaded onto truck delivering each package in order
    def DeliverPackages(self, table, matrix, startTime):
        totalMilesTraveled = 0.0

        runningHours = GetHours(startTime)
        runningMinutes = GetMinutes(startTime)
        AMPM = GetAMPM(startTime)

        self.starttime = startTime

        for i in range(len(self.packagelist)):
            table.EnRoute(table, int(self.packagelist[i]), startTime)
            deliveryTime = None

            if self.packagelist[i] == self.packagelist[0]:
                milesTraveled = float(matrix[0][int(self.packagelist[i])])
                totalMilesTraveled += milesTraveled

                timeInMinutes = (milesTraveled / self.speed) * 60

                hours = timeInMinutes // 60
                minutes = timeInMinutes % 60
                runningHours += hours
                runningMinutes += minutes

                if runningHours >= 12: 
                    if runningHours == 12:
                        if AMPM == "AM":
                            AMPM = "PM"
                        else:
                            AMPM = "AM"
                    runningHours = runningHours % 12
                
                if runningMinutes > 60:
                    runningMinutes = runningMinutes % 60
                    runningHours += 1
                
                if len(str(int(runningMinutes))) == 1:
                    deliveryTime = f"{int(runningHours)}:0{int(runningMinutes)} {AMPM}"
                else:
                    deliveryTime = f"{int(runningHours)}:{int(runningMinutes)} {AMPM}"
                
                table.Delivered(table, int(self.packagelist[i]), deliveryTime)

            else:
                milesTraveled = float(matrix[int(self.packagelist[i - 1])][int(self.packagelist[i])])
                totalMilesTraveled += milesTraveled

                timeInMinutes = (milesTraveled / self.speed) * 60

                hours = timeInMinutes // 60
                minutes = timeInMinutes % 60
                runningHours += hours
                runningMinutes += minutes

                if runningMinutes > 59:
                    runningMinutes = runningMinutes % 60
                    runningHours += 1

                if runningHours >= 12: 
                    runningHours = runningHours % 12
                    
                    if AMPM == "AM":
                        AMPM = "PM"
                    
                    if runningHours == 0:
                        runningHours = 12
                                   
                if len(str(int(runningMinutes))) == 1:
                    deliveryTime = f"{int(runningHours)}:0{int(runningMinutes)} {AMPM}"
                else:
                    deliveryTime = f"{int(runningHours)}:{int(runningMinutes)} {AMPM}"
                
                table.Delivered(table, int(self.packagelist[i]), deliveryTime)
        
        milesBackToHub = float(matrix[int(self.packagelist[len(self.packagelist) - 1])][0])
        totalMilesTraveled += milesBackToHub

        self.mileage = totalMilesTraveled
        
        backToHubTime = (milesBackToHub / self.speed) * 60
        backToHubHours = backToHubTime // 60
        backToHubMinutes = backToHubTime % 60

        runningHours += backToHubHours
        runningMinutes += backToHubMinutes

        if runningMinutes > 59:
            runningMinutes = runningMinutes % 60
            runningHours += 1
        
        if runningHours >= 12: 
            runningHours = runningHours % 12
            
            if AMPM == "AM":
                AMPM = "PM"

            if runningHours == 0:
                runningHours = 12              
        
        if len(str(int(runningMinutes))) == 1:
            self.endtime = f"{int(runningHours)}:0{int(runningMinutes)} {AMPM}"
        else:
            self.endtime = f"{int(runningHours)}:{int(runningMinutes)} {AMPM}"
 
    # Prints package list
    def Print(self):

        print(self.packagelist)