from nornir import InitNornir

"""
2e. Create a Python script that uses InitNornir to create a Nornir object using the newly created hosts.yaml and groups.yaml files.
Using a for-loop loop over the Nornir hosts in inventory and print out the following attributes for each host:
 hostname, groups, platform, username, password, and port.
Do this directly from the Nornir host objects
(i.e. rely on Nornir's ability to search from the host object then to group object).
"""

# Create norn object by initialising Nornir - automatically processess simpinventory files
norn = InitNornir()
# Get hosts object
hosts = norn.inventory.hosts

# Loop through dictionary of hostobjects and get attributes
for i in hosts:
    print(hosts[i].hostname)
    print(hosts[i].groups)
    print(hosts[i].platform)
    print(hosts[i].username)
    print(hosts[i].password)
    print("-" * 10)
