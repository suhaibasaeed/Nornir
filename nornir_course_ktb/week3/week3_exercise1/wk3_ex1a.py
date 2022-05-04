"""
1a. Create a Python script that initializes a Nornir object.

Print out the "data" attribute of the "arista3" host. Call the "items()" method on host "arista3".

Notice that when calling the items() method that Nornir not only displays the "data" entries associated at the host-level,
 but also recurses the data for the groups (that the host belongs to).
"""

from nornir import InitNornir
from rich import print

# Initialise Nornir
nr = InitNornir()

# Print data atrribute of arista3
print(nr.inventory.hosts['arista3'].data)
# Print arista3 .items() which will show us data attribute by recursing through groups.yaml too
print(nr.inventory.hosts['arista3'].items())