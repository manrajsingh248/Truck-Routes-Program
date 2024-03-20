class Truck(object):
    # Constructor for the Truck class
    def __init__(self, truck_id, current_time, packages=None, hashtab=None, location="4001 South 700 East"):
        self.truck_id = truck_id  # Truck ID
        self.packages = packages  # Set of packages
        self.current_time = current_time  # Time of completion of packages delivered for the truck
        self.time_left = current_time  # Departure time of thr truck
        self.location = location  # Starting location of the truck
        self.miles = 0  # Total distance traveled by the truck
        self.capacity = 16  # Capacity for Truck

        # Assigns the time the truck left the hub for each package on this truck
        for single_package_id in packages:
            package_hash = hashtab.search(single_package_id)
            package_hash.time_left_hub = self.time_left

    # String representation of the Truck object
    def __str__(self):
        return (f"Truck {self.truck_id} - \nPackages: {self.packages} \nTotal Distance: {self.miles} miles, Departure Time: "
                f"{self.time_left} "f"Delivery Complete at: {self.current_time}, \nStarting Location: {self.location}, Truck Capacity: "
                f"{self.capacity} Packages")