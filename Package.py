class Package:
    # Constructor for the Package class
    def __init__(self, id, address, city, state, zipcode, deadline, weight, truck=None, status='At Hub', delivery_time=None):
        self.id = id  # Package id
        self.address = address  # Delivery address
        self.city = city  # City for delivery address
        self.state = state  # State for delivery address
        self.zipcode = zipcode  # Zip for delivery address
        self.deadline = deadline  # Delivery deadline for package
        self.truck = truck  # The truck carrying the package, None if not yet assigned
        self.status = status  # Current status of the package, (default is 'At Hub')
        self.delivery_time = delivery_time  # Time of delivery, None if not yet delivered
        self.time_left_hub = None  # Time when package leaves the hub, initially None
        self.weight = weight  # Weight of package

        # String representation of the Package object
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state, self.zipcode, self.deadline,
                                                           self.weight, self.truck, self.status, self.delivery_time)