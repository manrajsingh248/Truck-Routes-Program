import csv
import datetime
import Package
import hashtable
import Truck
import requests
from dotenv import load_dotenv
import os
load_dotenv()


# Function to load package data from the CSV file into a hash table
def load_package_data(package_file, hashtab):
    # Open csv file and read its contents
    with open(package_file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)  # Skips header row
        # Loop through each row in the csv file
        for row in csv_reader:
            # Extract package data from the row
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            # Create a new package with the extracted data
            package = Package.Package(id, address, city, state, zipcode, deadline, weight)
            # Insert the package into the hash table
            hashtab.insert(id, package)


# Function to load distance data from the csv file
def load_distance_data(distance_file):
    # Initialize empty list to store distance data
    distance_data = []
    # Open csv file and read its contents
    with open(distance_file) as csvfile:
        count = 0
        csv_reader = csv.reader(csvfile, delimiter=",")
        # Loop through each row in the csv file
        for row in csv_reader:
            # Append each row to the distance_data list
            distance_data.append(row)
    # Return the populated distance_data list
    return distance_data


# Function to load address data from the csv file
def loaadddress_data(address_file):
    # Initialize empty list to store address data
    address_data_list = []
    # Open csv file and read its contents
    with open(address_file, 'r') as file:
        # csv reader to parse the file
        reader = csv.reader(file)
        # Loop through each row in the csv file
        for row in reader:
            # Append each address to the address_data_list list
            address_data_list.append(row[2])
    # Return the populated address_data_list list
    return address_data_list


# Function to calculate distance between 2 addresses using address_data_list and distance_data
def distance_between(address1, address2, address_data_list, distance_data):
    # Initialize distance as 0.0
    distance = 0.0
    # Find index of two addresses in address_data_list
    add1 = address_data_list.index(address1)
    add2 = address_data_list.index(address2)
    # Check if distance exists, if not, use reverse distance to find distance
    # between the two addresses
    if distance_data[add1][add2] == "":
        distance = distance_data[add2][add1]
    else:
        distance = distance_data[add1][add2]
    # Return the calculated distance
    return distance


# Function to find the minimum distance
# Compares each calculated distance to the current minimum distance, updating
# min_distance, nearest_address, nextid, whenever the smalled distance is found
def min_distance_from(from_address, Truck_packages, address_data_list, distance_data):
    # Variable set to infinity to ensure any real distance will be found initially
    min_distance = float('inf')
    # Initialize variables to None and 0, to store the nearest address and next id
    nearest_address = None
    nextid = 0
    for package_id in Truck_packages:
        # Iterates over each package ID in Truck_packages and finds min_distance
        # by using distance_between, comparing the distance from the starting address
        # (from_address) and package address of each package to the current min_distance
        pkg = hashtab.search(package_id)
        package_address = pkg.address
        distance = float(distance_between(from_address, package_address, address_data_list, distance_data))
        # Updates minimum distance, nearest package, and next id if a closer package is found
        if distance < min_distance:
            min_distance = distance
            nearest_address = package_address
            nextid = pkg.id
    # Return nearest address, next id and minimum distance
    return nearest_address, nextid, min_distance


# Function to deliver all packages in each Truck
def delivery_packages(Truck):
    # Initialize miles and the Truck's starting location
    miles = 0
    current_location = '4001 South 700 East'
    # For each package list in each of the 3 Trucks, the loop goes through each package the Truck needs to deliver,
    # calculates the distance to nearest address, updates Truck distance and delivery time, and marks Truck status as delivered.
    # Process repeats until all Truck packages have been delivered.
    while len(Truck.packages) > 0:
        nearest_address, nextid, min_distance = min_distance_from(current_location, Truck.packages, address_data_list, distance_data)
        # Updates Truck's total miles and current time based on delivery
        Truck.miles += min_distance
        # Calculates delivery time in seconds. Speed is a default 18 miles per hour.
        delivery_time = min_distance / 18 * 60 * 60
        # Converts delivery time to object using datetime.timedelta
        dts = datetime.timedelta(seconds=delivery_time)
        # Update Truck's current time by adding the delivery time
        Truck.current_time += dts
        # Get next package to be delivered and update its status and delivery time
        pkg = hashtab.search(nextid)
        pkg.status = 'Delivered'
        pkg.delivery_time = Truck.current_time
        # Remove the delivered package from the Truck and update the current location
        Truck.packages.remove(nextid)
        current_location = nearest_address


# MAIN--------------------------------------------------------------------------------------------------------------------------------------
# file paths for the csv files
package_file = 'packages.csv'
distance_file = 'distances.csv'
address_file = 'addresses.csv'

# Load address data, package data from csv files
address_data_list = loaadddress_data(address_file)
distance_data = load_distance_data(distance_file)

# Initialize a new hash table for storing package information,
# Load package data into the hash table and distance data into a list
hashtab = hashtable.ChainingHashTable()
load_package_data(package_file, hashtab)

# Manually loading sets of packages with package IDs onto each Truck
Truck1packages = {1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40}
Truck2packages = {3, 6, 7, 17, 18, 25, 26, 27, 28, 32, 36, 38}
Truck3packages = {2, 4, 5, 8, 9, 10, 11, 12, 21, 22, 23, 24, 33, 35, 39}

# Loop that searches and assigns each package to Truck 1, 2, or 3
for i in Truck1packages:
    package = hashtab.search(i)
    package.truck = "1"
for i in Truck2packages:
    package = hashtab.search(i)
    package.truck = "2"
for i in Truck3packages:
    package = hashtab.search(i)
    package.truck = "3"

# Setting start time for Truck 1
start_time = '8:00:00'
# Split start time into hours, minutes, seconds
h, m, s = start_time.split(':')
# Convert start time into datetime.timedelta object
time_obj1 = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

# Initializing Truck 1 and starting delivery
Truck1 = Truck.Truck(1, time_obj1, Truck1packages, hashtab)
delivery_packages(Truck1)

# Setting start time for Truck 2
start_time = '9:06:00'
# Split start time into hours, minutes, seconds
h, m, s = start_time.split(':')
time_obj2 = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

# Initializing Truck 2 and starting delivery
Truck2 = Truck.Truck(2, time_obj2, Truck2packages, hashtab)
delivery_packages(Truck2)

# Setting start time for Truck 3
start_time = '10:30:00'
# Split start time into hours, minutes, seconds
h, m, s = start_time.split(':')
# Convert start time into datetime.timedelta object
time_obj3 = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

# Initializing Truck 3 and starting delivery
Truck3 = Truck.Truck(3, time_obj3, Truck3packages, hashtab)
delivery_packages(Truck3)

# Wrong address listed for package 9, Truck Routing System updates correct address at 10:20 am
start_time = '10:20:00'
# Split start time into hours, minutes, seconds
h, m, s = start_time.split(':')
# Convert start time into datetime.timedelta object
time_obj_pkg9 = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))


# USER INTERFACE----------------------------------------------------------------------------------------------------------------------------
# Displays menu options for the Truck Routing System
print("Welcome to the Truck Routing System")
print("1, Print All Package Status")
print("2, Get Status of Any Given Package with Time")
print("3, Get Status of All Packages with Time")
print("4, Total Mileage Traveled by All Trucks")
print("5, Get Today's Weather and Forecast for Tomorrow")
print("6, Exit the Program")


# Takes user input for selecting an option
option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")
exit = True

# Loop that will continue until user chooses to exit
while exit:
    if option == "1":
        # Option 1: Print status of all packages
        # Searches for each package in the hash table by ID
        for i in range(len(hashtab.table)):
            package = hashtab.search(i + 1)
            if package:
                print(
                    f"Package #{i + 1}: Status: {package.status} at {package.delivery_time}, Address: {package.address}, {package.city}, "
                    f"{package.state}, {package.zipcode}, Deadline: {package.deadline}, Weight: {package.weight}, on Truck {package.truck}")
        # Re-displaying menu and take user input again for selecting an option
        print("\n\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")

    elif option == "2":
        # Option 2: Get status of a specific package at a given time
        input_package = int(input("Enter a valid package ID# (1-40): "))
        input_time = input("Enter a time in (HH:MM:SS): ")
        # Split input time into hours, minutes, seconds
        h, m, s = input_time.split(':')
        # Convert the split time into datetime.timedelta object for comparison
        user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        # Searches for each package in the hash table by ID
        for i in range(len(hashtab.table)):
            package = hashtab.search(i + 1)
            # Wrong address listed for package 9, Truck Routing System updates correct address at 10:20 am
            if package.id == 9 and user_time < time_obj_pkg9:
                package.address = "300 State St"
                package.zipcode = "84103"
            if package.id == input_package:
                if 0 >= input_package or input_package >= 41:
                    print("Invalid package ID#. Please try again.")
                else:
                    # compares user time and package's delivery time,
                    # displays status based on specified time
                    if user_time >= package.delivery_time:
                        print(f"Package {i + 1} Status at {input_time}: Delivered at {package.delivery_time}, Address: {package.address},"
                              f" {package.city}, {package.state}, {package.zipcode}, Deadline: {package.deadline}, Weight: "
                              f"{package.weight}, on Truck {package.truck}")
                    elif user_time < package.delivery_time and user_time < package.time_left_hub:
                        print(f"Package {i + 1} Status at {input_time}: At Hub, Address:"
                              f" {package.address}, {package.city}, {package.state}, {package.zipcode}, Deadline: {package.deadline},"
                              f" Weight: {package.weight}, on Truck {package.truck}")
                    else:
                        print(f"Package {i + 1} Status at {input_time}: En Route, Address:"
                              f" {package.address}, {package.city}, {package.state}, {package.zipcode}, Deadline: {package.deadline}, "
                              f"Weight: {package.weight}, on Truck {package.truck}")

        # Re-displaying menu and take user input again for selecting an option
        print("\n\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")

    elif option == "3":
        # Option 3: Get status of all packages at a given time
        input_time = input("Enter a time in (HH:MM:SS): ")
        # Split input time into hours, minutes, seconds
        h, m, s = input_time.split(':')
        # Convert the split time into datetime.timedelta object for comparison
        user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        # Searches for each package in the hash table by ID
        for i in range(len(hashtab.table)):
            package = hashtab.search(i + 1)
            # Wrong address listed for package 9, Truck Routing System updates correct address at 10:20 am
            if package.id == 9 and user_time < time_obj_pkg9:
                package.address = "300 State St"
                package.zipcode = "84103"
            if package:
                # Compares user time and package's delivery time,
                # displays status based on specified time
                if user_time >= package.delivery_time:
                    print(f"Package {i + 1} Status at {input_time}: Delivered at {package.delivery_time}, Address: {package.address}, "
                          f"{package.city}, {package.state}, {package.zipcode}, Deadline: {package.deadline}, Weight: {package.weight}, on "
                          f"Truck {package.truck}")
                elif user_time < package.delivery_time and user_time < package.time_left_hub:
                    print(
                        f"Package {i + 1} Status at {input_time}: At Hub, Address:"
                        f" {package.address}, {package.city}, {package.state}, {package.zipcode}, Deadline: {package.deadline}, Weight: "
                        f"{package.weight}, on Truck {package.truck}")
                else:
                    print(
                        f"Package {i + 1} Status at {input_time}: En Route, Address: {package.address}, {package.city}, {package.state},"
                        f" {package.zipcode},  Deadline: {package.deadline}, Weight: {package.weight}, on Truck {package.truck}")
            else:
                print("Invalid package ID#. Please try again.")
        # Re-displaying menu and take user input again for selecting an option
        print("\n\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")

    elif option == "4":
        # Option 4: Mileage for each Truck and total mileage traveled by all Trucks
        # Calculates total time each Truck was en route
        Truck1_time = Truck1.current_time - time_obj1
        Truck2_time = Truck2.current_time - time_obj2
        Truck3_time = Truck3.current_time - time_obj3
        # Calculate total miles traveled by all Trucks
        total_miles = Truck1.miles + Truck2.miles + Truck3.miles
        print(f"\nTotal Mileage for all 3 Trucks: {total_miles} miles")
        print(f"\nTruck 1 Mileage: {Truck1.miles} miles")
        print(f"Truck 1 Total Time Taken: {Truck1_time}")
        print(f"\nTruck 2 Mileage : {Truck2.miles} miles")
        print(f"Truck 2 Total Time Taken: {Truck2_time}")
        print(f"\nTruck 3 Mileage: {round(Truck3.miles, 1)} miles")
        print(f"Truck 3 Total Time Taken: {Truck3_time}")

        # Re-displaying menu and take user input again for selecting an option
        print("\n\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")

    elif option == "5":
        # Option 5: Gets Weather Data

        # Base URLs and API Key for Weather and list of cities in the route
        BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather?"
        BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast?"
        API_KEY = os.getenv("API_KEY")
        CITIES = ["Salt Lake City, UT, US", "West Valley City, UT, US", "Holladay, UT, US", "Murray, UT, US", "Millcreek, UT, US"]

        # Function converts temp from kelvin to celsius and fahrenheit
        def kelvin_to_celsius_fahrenheit(kelvin):
            celsius = kelvin - 273.15
            fahrenheit = celsius * (9 / 5) + 32
            return celsius, fahrenheit

        # Function displays current weather for city in cities list
        def get_current_weather(city):
            url = BASE_URL_CURRENT + "appid=" + API_KEY + "&q=" + city.replace(" ", "%20")
            response = requests.get(url).json()
            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            description = response['weather'][0]['description']
            print(f"Current Weather in {city}: {temp_fahrenheit:.2f}°F, {description}")


        # Function displays today's hourly forecast weather for city in cities list
        def get_tdhourly_weather(city):
            url = BASE_URL_FORECAST + "appid=" + API_KEY + "&q=" + city.replace(" ", "%20")
            response = requests.get(url).json()
            today = datetime.date.today()
            print(f"\nToday's hourly forecast:")
            for item in response['list']:
                forecast_time = datetime.datetime.fromtimestamp(item['dt'])
                if forecast_time.date() == today:
                    temp_kelvin = item['main']['temp']
                    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
                    description = item['weather'][0]['description']
                    print(f"At {forecast_time.strftime('%H:%M')}: {temp_fahrenheit:.2f}°F, {description}")

        # Function displays tomorrow's hourly forecast for city in cities list
        def get_tmrw_weather(city):
            url = BASE_URL_FORECAST + "appid=" + API_KEY + "&q=" + city.replace(" ", "%20")
            response = requests.get(url).json()
            tmrw = datetime.date.today() + datetime.timedelta(days=1)
            print(f"\nTomorrow's hourly forecast: ")
            for item in response['list']:
                forecast_time = datetime.datetime.fromtimestamp(item['dt'])
                if forecast_time.date() == tmrw:
                    temp_kelvin = item['main']['temp']
                    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
                    description = item['weather'][0]['description']
                    print(f"At {forecast_time.strftime('%H:%M')}: {temp_fahrenheit:.2f}°F, {description}")

        # Loops through cities to print current and tomorrow's weather
        for city in CITIES:
            print("------")
            get_current_weather(city)
            get_tdhourly_weather(city)
            get_tmrw_weather(city)

            print("------")

        # Re-displaying menu and take user input again for selecting an option
        print("\n\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")

    elif option == "6":
        # Option 6: Exits Program
        print('Exiting Program...')
        exit = False  # Sets exit to False and will exit the loop

    else:
        # If user does not choose a valid option 1-6
        print("\nInvalid option, please try again")
        # Re-displaying menu and take user input again for selecting an option
        print("\n1, Print All Package Status")
        print("2, Get Status of Any Given Package with Time")
        print("3, Get Status of All Packages with Time")
        print("4, Total Mileage Traveled by All Trucks")
        print("5, Get Today's Weather and Forecast for Tomorrow")
        print("6, Exit the Program")
        option = input("\nChoose An Option: 1, 2, 3, 4, 5, 6: ")
