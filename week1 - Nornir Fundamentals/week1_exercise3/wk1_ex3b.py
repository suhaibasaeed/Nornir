from nornir import InitNornir

"""
b. Re-execute your exercise2e Python script against this new inventory.
In other words, verify that your Python for-loop on the Nornir Host Objects properly searches from host, to group, to defaults
 and prints out the attributes specified in exercise 2e.

3
"""

# Create norn object by initialising Nornir - automatically processess simpinventory files
norn = InitNornir()
# Get hosts object
hosts = norn.inventory.hosts

# Loop through dictionary of hostobjects and get attributes -
for i in hosts:
    print(hosts[i].hostname)
    print(hosts[i].groups)
    print(hosts[i].platform)
    print(hosts[i].username)
    print(hosts[i].password)
    print("-" * 10)
