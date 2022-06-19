"""

2b. Using the filter method, create a Nornir object that is filtered to all devices using the role "WAN".
Print the hosts that are contained in this new Nornir object.
Further filter on this newly created Nornir object to capture only hosts using port 22.
Once again, print the hosts in this new Nornir object.

2c. Using an F-filter, create a new Nornir object that contains all the hosts that belong to the "sfo" group.
Print the hosts that are contained in this new Nornir object.

"""

from nornir import InitNornir
from rich import print

# Initialise Nornir
nr = InitNornir()


# Create arista3 object by filtering on the arista3 host only and print
arista3 = nr.filter(name='arista3')
print(arista3.inventory.hosts)

# 
arista_wan = nr.filter