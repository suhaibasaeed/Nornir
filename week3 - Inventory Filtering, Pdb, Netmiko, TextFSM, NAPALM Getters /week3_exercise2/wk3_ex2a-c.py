"""
2a. Using the inventory files from the previous exercise, create a Nornir object that is filtered to only "arista1".
Use the .filter() method to accomplish this. Print the hosts that are contained in this new Nornir object.

2b. Using the filter method, create a Nornir object that is filtered to all devices using the role "WAN".
Print the hosts that are contained in this new Nornir object.
Further filter on this newly created Nornir object to capture only hosts using port 22.
Once again, print the hosts in this new Nornir object.

2c. Using an F-filter, create a new Nornir object that contains all the hosts that belong to the "sfo" group.
Print the hosts that are contained in this new Nornir object.

"""

from nornir import InitNornir
from rich import print
from nornir.core.filter import F

# Initialise Nornir
nr = InitNornir()


# 2a - create arista3 object by filtering on the arista3 host only and print
arista3 = nr.filter(name='arista3')
print(arista3.inventory.hosts)

# 2b - create object by filtering on WAN role then further filter on port 22
arista_wan = nr.filter(role='WAN')
print(arista_wan.inventory.hosts)

arista_wan_22 = arista_wan.filter(port=22)
print(arista_wan_22.inventory.hosts)

# 2c - Filter on sfo group using F object
sfo = nr.filter(F(groups__contains='sfo'))
print(sfo.inventory.hosts)