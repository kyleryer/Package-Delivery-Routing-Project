# Sorts a list by nearest neighbor based on first item in list
def NearestNeighborSort(list, matrix): 
    for i in range(len(list) - 1):
        leastDistance = None
        packageLocation = int(list[i])

        for j in range(i + 1, len(list)):
            comparisonLocation = int(list[j])
            currentDistance = float(matrix[packageLocation][comparisonLocation])
            if leastDistance == None:
                leastDistance = currentDistance
                leastDistanceIndex = j
            else:
                if currentDistance < leastDistance:
                    leastDistance = currentDistance
                    leastDistanceIndex = j
        
        (list[i + 1], list[leastDistanceIndex]) = (list[leastDistanceIndex], list[i + 1])

# Finds unloaded package that is the nearest neighbor to chosen package 
def FindNearestNeighbor(id, table, matrix):
    nearestNeighbor = None
    closestDistance = None
    numberOfPackages = table.size

    for i in range(1, numberOfPackages, 1):
        currentPackage = table.Get(i)
        currentDistance = float(matrix[int(id)][int(currentPackage[0])])

        if table.IsLoaded(int(currentPackage[0])) == False and nearestNeighbor == None:
            closestDistance = currentDistance
            nearestNeighbor = currentPackage[0]
        else:
            if table.IsLoaded(int(currentPackage[0])) == False and currentDistance < closestDistance:
                closestDistance = currentDistance
                nearestNeighbor = currentPackage[0]
    
    return nearestNeighbor

# Get number of hours from a given time
def GetHours(time):
    hours = time.split(":")[0]

    return int(hours)

# Get number of minutes from a given time
def GetMinutes(time):
    minutes = time.split(":")[1]
    minutes = minutes.split()[0]

    return int(minutes)

# Get AM/PM from a given time
def GetAMPM(time):
    AMPM = time.split(":")[1]
    AMPM = AMPM.split()[1]

    return AMPM