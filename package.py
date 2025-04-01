class Package:
    
    def __init__(self, id, address, city, state, zipcode, deadline, weight, notes, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.loaded = "No"
        self.enRouteTime = None
        self.deliveredTime = None
        self.truck = None