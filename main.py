# Student ID: 012026763

import csv
from HashTable import HashTable
from package import Package
from truck import Truck
from functions import NearestNeighborSort, GetHours, GetMinutes, GetAMPM
import UserInterface

# Number of packages to deliver
CONST_NUMBER_OF_PACKAGES = 40

# Max capacity of packages that can be carried on a truck
CONST_TRUCK_MAX_CAPACITY = 16

# Speed of trucks in MPH
CONST_TRUCK_SPEED = 18

# Start time for deliveries
CONST_START_TIME = "8:00 AM"

# Create hash table to store package data
PackageData = HashTable(CONST_NUMBER_OF_PACKAGES)

# Create adjacency matrix to store distance data
AdjacencyMatrix = []

# Read package data from csv file into hash table
with open('PackageData.csv', mode = 'r') as file:
    packageFile = csv.reader(file)
    for line in packageFile:
        package = Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8])
        PackageData.Insert(package)

# Read distance data from csv file into adjacency matrix
with open('AdjacencyList.csv', mode = 'r') as file:
    distanceFile = csv.reader(file)
    for line in distanceFile:
        lineList = list(line)
        AdjacencyMatrix.append(lineList)

# Create truck objects
Truck1 = Truck(CONST_TRUCK_MAX_CAPACITY, CONST_TRUCK_SPEED, 1)
Truck2 = Truck(CONST_TRUCK_MAX_CAPACITY, CONST_TRUCK_SPEED, 2)
Truck3 = Truck(CONST_TRUCK_MAX_CAPACITY, CONST_TRUCK_SPEED, 3)

# Load packages with prerequisites/special notes onto respective trucks
for i in range(1, CONST_NUMBER_OF_PACKAGES + 1, 1):
    currentPackage = PackageData.Get(i)
    if currentPackage[7] == "Delayed on flight---will not arrive to depot until 9:05 am":
        Truck3.Load(currentPackage[0])
        PackageData.Loaded(int(currentPackage[0]), 3)
    if currentPackage[7] == "Can only be on truck 2" or currentPackage[7] == "Wrong address listed":
        Truck2.Load(currentPackage[0])
        PackageData.Loaded(int(currentPackage[0]), 2)
    if currentPackage[0] == "13" or currentPackage[0] == "14" or currentPackage[0] == "15" or currentPackage[0] == "16" or currentPackage[0] == "19" or currentPackage[0] == "20":
        Truck1.Load(currentPackage[0])
        PackageData.Loaded(int(currentPackage[0]), 1)

# Load packages with deadlines onto trucks 1 and 3 if package is not already loaded onto another truck and truck is not at max capacity
for i in range(1, CONST_NUMBER_OF_PACKAGES + 1, 1):
    currentPackage = PackageData.Get(i)
    if currentPackage[5] != "EOD" and PackageData.IsLoaded(int(currentPackage[0])) == False:
        if len(Truck1.packagelist) < 16:
            Truck1.Load(currentPackage[0])
            PackageData.Loaded(int(currentPackage[0]), 1)
        elif len(Truck3.packagelist) < 16:
            Truck3.Load(currentPackage[0])
            PackageData.Loaded(int(currentPackage[0]), 3)

# Load unloaded packages that have matching addresses with loaded packages onto the same truck unless truck is already at max capacity
for i in range(1, CONST_NUMBER_OF_PACKAGES + 1, 1):
    currentPackage = PackageData.Get(i)   
    for package in Truck1.packagelist:
        loadedPackage = PackageData.Get(int(package))
        if PackageData.IsLoaded(int(currentPackage[0])) == False and currentPackage[1] == loadedPackage[1] and len(Truck1.packagelist) < 16:
            Truck1.Load(currentPackage[0])
            PackageData.Loaded(int(currentPackage[0]), 1)
            break
    for package in Truck3.packagelist:
        loadedPackage = PackageData.Get(int(package))
        if PackageData.IsLoaded(int(currentPackage[0])) == False and currentPackage[1] == loadedPackage[1] and len(Truck3.packagelist) < 16:
            Truck3.Load(currentPackage[0])
            PackageData.Loaded(int(currentPackage[0]), 3)
            break
    for package in Truck2.packagelist:
        loadedPackage = PackageData.Get(int(package))
        if PackageData.IsLoaded(int(currentPackage[0])) == False and currentPackage[1] == loadedPackage[1] and len(Truck2.packagelist) < 16:
            Truck2.Load(currentPackage[0])
            PackageData.Loaded(int(currentPackage[0]), 2)
            break    

# Search each truck's list, find package address closest to hub, and place this package at the beginning of the list
Truck1.ClosestToHub(AdjacencyMatrix)
Truck2.ClosestToHub(AdjacencyMatrix)
Truck3.ClosestToHub(AdjacencyMatrix)

# Sort each truck's list by distance using nearest neighbor algorithm 
NearestNeighborSort(Truck1.packagelist, AdjacencyMatrix)
NearestNeighborSort(Truck2.packagelist, AdjacencyMatrix)
NearestNeighborSort(Truck3.packagelist, AdjacencyMatrix)

# Load unloaded packages onto trucks via NearestNeighborLoad. Load trucks that are leaving earliest first. 
Truck1.NearestNeighborLoad(PackageData, AdjacencyMatrix)
Truck3.NearestNeighborLoad(PackageData, AdjacencyMatrix)
Truck2.NearestNeighborLoad(PackageData, AdjacencyMatrix)

# Send first truck out for delivery at start of day
Truck1.DeliverPackages(PackageData, AdjacencyMatrix, CONST_START_TIME)

# Send third truck out at 9:05 a.m. since since certain packages will not arrive until then
Truck3.DeliverPackages(PackageData, AdjacencyMatrix, "9:05 AM")

# Second truck has to wait until 10:20 AM for a package needing an address change 
# Send second truck at 10:20 AM if another truck has returned to the hub, or whenever another truck returns if later than 10:20 AM
Truck1Hours = GetHours(Truck1.endtime)
Truck1Minutes = GetMinutes(Truck1.endtime)
Truck1AMPM = GetAMPM(Truck1.endtime)

Truck3Hours = GetHours(Truck3.endtime)
Truck3Minutes = GetMinutes(Truck3.endtime)
Truck3AMPM = GetAMPM(Truck3.endtime)
if Truck1Hours < 10:
    Truck2.DeliverPackages(PackageData, AdjacencyMatrix, "10:20 AM")

elif Truck1Hours == 10:
    if Truck1Minutes <= 20:
        Truck2.DeliverPackages(PackageData, AdjacencyMatrix, "10:20 AM")

elif Truck3Hours < 10:
    Truck2.DeliverPackages(PackageData, AdjacencyMatrix, "10:20 AM")

elif Truck3Hours == 10:
    if Truck3Minutes <= 20:
        Truck2.DeliverPackages(PackageData, AdjacencyMatrix, "10:20 AM")

else:
    if Truck1AMPM == "AM" and Truck3AMPM == "PM":
        Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck1.endtime)
    elif Truck3AMPM == "AM" and Truck1AMPM == "PM":
        Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck3.endtime)
    elif Truck1AMPM == "AM" and Truck3AMPM == "AM":
        if Truck1Hours <= Truck3Hours:
            Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck1.endtime)
        else:
            Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck3.endtime)
    else:
        if Truck1Hours <= Truck3Hours:
            Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck1.endtime)
        else:
            Truck2.DeliverPackages(PackageData, AdjacencyMatrix, Truck3.endtime)

# Record total miles traveled by all trucks
totalMiles = Truck1.mileage + Truck2.mileage + Truck3.mileage

# Create list of trucks for user interface to use
TruckList = [Truck1, Truck2, Truck3]

# Print out successful delivery message and start up the user interface
print(f"Deliveries have been successfully completed! Total miles traveled for all trucks: {totalMiles}")
print()
UserInterface.StartUserInterface(PackageData, TruckList)