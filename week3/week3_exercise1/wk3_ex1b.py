"""
1b. In the "sea" group in groups.yaml, add a "timezone" key and set the value to "PST".
Print out the timezone for each of the hosts in the inventory.

Without setting any data fields on the "arista3" host, modify the inventory files such that the timezone attribute for "arista3" is set to "PST".
"""

from nornir import InitNornir
from rich import print

# Initialise Nornir
nr = InitNornir()

# Loop through arista hosts and print out timezone key from each - comes from groups
for i in nr.inventory.hosts.keys():
    print(f" Host {i} has Timezone {nr.inventory.hosts[i]['timezone']}" )