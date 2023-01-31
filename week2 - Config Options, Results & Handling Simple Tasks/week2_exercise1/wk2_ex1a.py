"""
1a. Create a simple 'hosts.yaml' file that contains a single entry for localhost.

Now create a Python script that uses InitNornir to initialize a Nornir object.
Using this Nornir object print out the number of workers currently configured.
This value should be 20 at this point.
"""

from nornir import InitNornir
from rich import print

# Create norn object by initialising Nornir - automatically processess simpinventory files
norn = InitNornir()

# Print no. of workers
no_of_workers = norn.runner.num_workers
print(f"The number of workers are: {no_of_workers}")
