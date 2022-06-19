"""
3a. Using an F-filter, create a Nornir object that is the hosts belonging to the role "AGG".
    Print the hosts that are contained in this new Nornir object.

3b. Using an F-filter, create a Nornir object of devices that are members of either the "sea" or (union) the "sfo" group.
    Print the hosts that are contained in this new Nornir object.

3c. Using an F-filter, create a Nornir object that contains devices that belong to:
    the "WAN" role and (intersection) have a WIFI password of "racecar".
Note, for a nested dictionary key inside data, you can use the following pattern:
F(site_details__wifi_password__contains="whatever")

Where the corresponding section of inventory is:
data:
  site_details:
    wifi_password: whatever

3d. Modify the filter from exerice3c such that you retrieve the devices:
    that do NOT have a wifi password of "racecar".

"""

from nornir import InitNornir
from rich import print
from nornir.core.filter import F

# Initialise Nornir
nr = InitNornir()


# 3a - filter on role AGG devices using F object
agg = nr.filter(F(role='AGG'))
print(agg.inventory.hosts)

# 3b - Filter on union of devices in sea or sfo grop
sea_sfo = nr.filter(F(groups__contains='sea') | F(groups__contains='sfo'))
print(sea_sfo.inventory.hosts)

# 3c - Filter on WAN role and racecar wifi_password in data
wan_role = nr.filter(F(role='WAN'))
# Filter on site_details dict and wifi_password key
wifi = wan_role.filter(F(site_details__wifi_password__contains="racecar"))
print(wifi.inventory.hosts)

# 3d - Filter on devices which don't have racecar wifi_password
not_wifi = wan_role.filter(~F(site_details__wifi_password__contains="racecar"))
print(not_wifi.inventory.hosts)
