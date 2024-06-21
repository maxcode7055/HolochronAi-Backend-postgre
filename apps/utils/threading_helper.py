# global_variables.py

import threading

# Define global variables
BLACKLIST = set()
blacklist_lock = threading.Lock()

# Function to add an item to the blacklist
def add_to_blacklist(item):
    with blacklist_lock:
        BLACKLIST.add(item)

# Function to remove an item from the blacklist
def remove_from_blacklist(item):
    with blacklist_lock:
        BLACKLIST.remove(item)