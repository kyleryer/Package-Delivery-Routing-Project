from functions import GetHours, GetMinutes, GetAMPM

# Checks the status of a package at a given time based on when it was on en route and delivered
def CheckStatus(userTime, enRouteTime, deliveryTime):
    status = None

    userHours = GetHours(userTime) % 12
    userMinutes = GetMinutes(userTime)
    userAMPM = GetAMPM(userTime)

    enRouteHours = GetHours(enRouteTime) % 12
    enRouteMinutes = GetMinutes(enRouteTime)
    enRouteAMPM = GetAMPM(enRouteTime)

    deliveredHours = GetHours(deliveryTime) % 12
    deliveredMinutes = GetMinutes(deliveryTime)
    deliveredAMPM = GetAMPM(deliveryTime)  

    if userAMPM == "AM" and enRouteAMPM == "PM":
        status = "At The Hub"

    elif userAMPM == "AM" and enRouteAMPM == "AM":
        if userHours < enRouteHours:
            status = "At The Hub"

        elif userHours == enRouteHours:
            if userMinutes < enRouteMinutes:
                status = "At The Hub"
            
            else:
                status = "En Route"
        
        else:
            if deliveredAMPM == "PM":
                status = "En Route"
            
            else:
                if userHours < deliveredHours:
                    status = "En Route"
                
                elif userHours == deliveredHours:
                    if userMinutes < deliveredMinutes:
                        status = "En Route"
                    
                    else:
                        status = f"Delivered at {deliveryTime}"
                
                else:
                    status = f"Delivered at {deliveryTime}"
    
    elif userAMPM == "PM" and enRouteAMPM == "PM":
        if userHours < enRouteHours:
            status = "At The Hub"

        elif userHours == enRouteHours:
            if userMinutes < enRouteMinutes:
                status = "At The Hub"
            
            else:
                status = "En Route"
        
        else:
            if userHours < deliveredHours:
                status = "En Route"
                
            elif userHours == deliveredHours:
                if userMinutes < deliveredMinutes:
                       status = "En Route"
                    
                else:
                    status = f"Delivered at {deliveryTime}"
                
            else:
                status = f"Delivered at {deliveryTime}"
    
    else:
        if deliveredAMPM == "AM":
            status = f"Delivered at {deliveryTime}"
            
        else:
            if userHours < deliveredHours:
                status = "En Route"
                
            elif userHours == deliveredHours:
                if userMinutes < deliveredMinutes:
                    status = "En Route"
                    
                else:
                    status = f"Delivered at {deliveryTime}"
                
            else:
                status = f"Delivered at {deliveryTime}"
    
    return status

# Returns the delivery status and package information for a single package at a requested time
def SinglePackage(table, id, time):
    package = table.Get(int(id))

    if package == None:
        print("Package ID not found. Please try again with a different ID.")
        print()
    
    elif package[0] == "9":
        status = CheckStatus(time, package[10], package[11])

        if status == "At The Hub":

            data = []

            data.append(f"ID: {package[0]}")
            data.append(f"Address: 300 State St Salt Lake City, UT 84103")
            data.append(f"Weight: {package[6]} kg")
            data.append(f"Deadline: {package[5]}")
            data.append(f"Delivery Status: {status}")

            print(data)
        
        else:
            data = []

            data.append(f"ID: {package[0]}")
            data.append(f"Address: {package[1]} {package[2]}, {package[3]} {package[4]}")
            data.append(f"Weight: {package[6]} kg")
            data.append(f"Deadline: {package[5]}")

            if status == "En Route":
                data.append(f"Delivery Status: {status}")
                data.append(f"Loaded on Truck {package[12]}")
            else:
                data.append(f"Delivery Status: {status}")
                data.append(f"Delivered by Truck {package[12]}")

            print(data)

    else:
        status = CheckStatus(time, package[10], package[11])

        data = []

        data.append(f"ID: {package[0]}")
        data.append(f"Address: {package[1]} {package[2]}, {package[3]} {package[4]}")
        data.append(f"Weight: {package[6]} kg")
        data.append(f"Deadline: {package[5]}")

        if status == "At The Hub":
            data.append(f"Delivery Status: {status}")
        elif status == "En Route":
            data.append(f"Delivery Status: {status}")
            data.append(f"Loaded on Truck {package[12]}")
        else:
            data.append(f"Delivery Status: {status}")
            data.append(f"Delivered by Truck {package[12]}")

        print(data)
    
    print()
    print("Returning to user interface...")
    print()
    

# Returns the delivery status and package information for all packages at a requested time
def AllPackages(table, userInput):
    for i in range(1, table.size + 1, 1):
        currentPackage = table.Get(i)

        status = CheckStatus(userInput, currentPackage[10], currentPackage[11])

        if currentPackage[0] == "9" and status == "At The Hub":
            
            data = []

            data.append(f"ID: {currentPackage[0]}")
            data.append(f"Address: 300 State St Salt Lake City, UT 84103")
            data.append(f"Weight: {currentPackage[6]} kg")
            data.append(F"Deadline: {currentPackage[5]}")

            data.append(f"Delivery Status: {status}")

            print(data)

        else:
            data = []

            data.append(f"ID: {currentPackage[0]}")
            data.append(f"Address: {currentPackage[1]} {currentPackage[2]}, {currentPackage[3]} {currentPackage[4]}")
            data.append(f"Weight: {currentPackage[6]} kg")
            data.append(f"Deadline: {currentPackage[5]}")

            if status == "At The Hub":      
                data.append(f"Delivery Status: {status}")
            elif status == "En Route":
                data.append(f"Delivery Status: {status}")
                data.append(f"Loaded on Truck {currentPackage[12]}")
            else:
                data.append(f"Delivery Status: {status}")
                data.append(f"Delivered by Truck {currentPackage[12]}")

            print(data)
    
    print()
    print("Returning to user interface...")
    print()

# Displays the user interface
def StartUserInterface(table, list):
    print("Welcome to the user interface!")
    print()
    print("Please select an option:")
    print()
    print("   Press 1 and then enter to look up delivery status of any or all packages at a given time")
    print("   Press 2 and then enter to view total mileage traveled by any or all trucks")
    print("   Press 0 and then enter to exit program")
    print()
    userInput = input()

    while userInput != "0" and userInput != "1" and userInput != "2":
        print("Invalid input. Please press 1, 2, or 0 followed by enter based on the options provided.")
        userInput = input()

    if userInput == "0":
        return
    
    if userInput == "1":
        userInput = input("Type in the package ID you would like to view the delivery status of, or type \"All\" to view delivery status of all packages: ")
        print()

        if userInput == "All":
            userInput = input("Type in your desired time using the format \"XX:XX AM\": ")
            print()

            AllPackages(table, userInput)
            StartUserInterface(table, list)
        
        else:
            if userInput.isdigit() == False:
                print("Invalid ID. Please try again using only numerical values.")
                print()
                StartUserInterface(table, list)
            
            else:
                userInput2 = input("Type in your desired time using the format \"X:XX AM\" or \"XX:XX AM\": ")
                print()

                SinglePackage(table, userInput, userInput2)
                StartUserInterface(table, list)
    
    if userInput == "2":
        size = len(list)
        userInput = input(f"Type in the truck's number (1-{size}) you would like to view the mileage of, or type \"All\" to view mileage for all trucks: ")
        print()

        if userInput == "All":
            totalMileage = 0

            for truck in list:
                totalMileage += truck.mileage
            
            print(f"Total mileage for all trucks: {totalMileage}")
            print()
            StartUserInterface(table, list)
            
        else:
            if userInput.isdigit() == False:
                print(f"Invalid input. Please try again using only numbers (1-{size}) or \"All\".")
                print()
                StartUserInterface(table, list)

            else:
                if int(userInput) < 1 or int(userInput) > size:
                    print(f"Invalid input. Please try again using only numbers (1-{size}) or \"All\".")
                    print()
                    StartUserInterface(table, list)

                else:
                    currentTruck = list[int(userInput) - 1]
                    print(f"Truck {int(userInput)}'s mileage: {currentTruck.mileage}")
                    print()
                    StartUserInterface(table, list)