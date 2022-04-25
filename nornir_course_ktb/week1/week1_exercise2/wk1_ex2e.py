from nornir import InitNornir

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
    print('-' * 10)