"""
Filter your inventory to select ONLY devices that belong to the "ios" group.

Add the following to your script after initializing your Nornir object (this will filter to select only the "ios" group):
from nornir.core.filter import F
filt = F(groups__contains="ios")
nr = nr.filter(filt)

Print out your inventory hosts after you accomplish your filtering:
print(nr.inventory.hosts)
"""

from nornir import InitNornir
from nornir.core.filter import (
    F,
)  # Import F class which will be used for filtering inventory
from rich import print

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS group only
ios_filt = F(groups__contains="ios")
norn = norn.filter(ios_filt)

# Print inventory
print(norn.inventory.hosts)
