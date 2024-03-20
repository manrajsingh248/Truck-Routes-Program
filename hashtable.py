class ChainingHashTable:
    # Constructor for the HashTable class
    def __init__(self, initial_capacity=40):
        # Initialize empty hash table with a initial capacity of 40
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        # Calculates index for the key
        index = hash(key) % len(self.table)
        # Obtains the list at the calculated index
        hash_list = self.table[index]
        # Updates the value if the key already exists
        for key_value in hash_list:
            if key_value[0] == key:
                key_value[1] = item
                return True
        # Adds new key-value pair if key does not exist
        key_value = [key, item]
        hash_list.append(key_value)
        return True

    def search(self, key):
        # Calculates index for the key
        index = hash(key) % len(self.table)
        # Obtains the list at the calculated index
        hash_list = self.table[index]
        # Searches for key and returns the value if the key is found
        for key_value in hash_list:
            if key_value[0] == key:
                return key_value[1]
            # Returns None if key not found
            return None

    def remove(self, key):
        # Calculates index for the key
        index = hash(key) % len(self.table)
        # Obtains the list at the calculated index
        hash_list = self.table[index]
        # Removes key-value pair if found
        for key_value in hash_list:
            if key_value[0] == key:
                hash_list.remove([key_value[0], key_value[1]])
