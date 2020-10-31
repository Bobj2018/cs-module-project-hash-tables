from numpy import *

class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = max(capacity, MIN_CAPACITY)
        self.storage = [None] * self.capacity
        self.load = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.load / len(self.storage)


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        """

        hash_index = 14695981039346656037
        FNV_prime = 1099511628211

        hash_bytes = key.encode()

        for byte in hash_bytes:
            hash_index = (hash_index * FNV_prime) ^ byte

        return hash_index


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        """
        hash_index = 5381
        hash_bytes = key.encode()

        for byte in hash_bytes:
            hash_index = ((hash_index << 5) + hash_index) + byte

        return hash_index


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.
        """
        index = self.hash_index(key)

        if self.storage[index] is not None:
            current_node = self.storage[index]

            while current_node is not None:
                if current_node.key == key:
                    current_node.value = value
                    return
                elif current_node.next is None:
                    current_node.next = HashTableEntry(key, value)
                    self.load += 1
                current_node = current_node.next
        else:
            self.storage[index] = HashTableEntry(key, value)
            self.load += 1





    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

        index = self.hash_index(key)

        if self.storage[index] is not None:
            if self.storage[index].key == key:
                self.storage[index] = self.storage[index].next
                return

            prev_node = self.storage[index]
            cur_node = self.storage[index].next

            while cur_node is not None:
                if cur_node.key == key:
                    prev_node.next = cur_node.next
                    return
                else:
                    prev_node = cur_node
                    cur_node = cur_node.next

        else:
            print("Warning: Key not found!")

        pass


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)

        if self.storage[index] is not None:

            current_node = self.storage[index]

            while current_node is not None:
                if current_node.key == key:
                    return current_node.value
                elif current_node.next is None:
                    return None
                current_node = current_node.next
        else:
            return None



    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        old_storage = list(set(self.storage))

        self.capacity = max(new_capacity, MIN_CAPACITY)
        self.storage = [None] * self.capacity
        self.load = 0

        for item in old_storage:
            self.put(item.key, item.value)
            if item.next is not None:
                curr_node = item.next
                while curr_node is not None:
                    self.put(curr_node.key, curr_node.value)
                    curr_node = curr_node.next



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
