"""
5a. Create a Nornir script that uses the netmiko_send_command task-plugin to execute "show ip int brief" on each of the devices in the "ios" group.
Use the inventory filtering pattern that we used in earlier exercises.
Print the output from this task using the print_results function.
"""

from nornir import InitNornir
from nornir.core.filter import (
    F,
)  # Import F class which will be used for filtering inventory
from rich import print
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS group only
ios_filt = F(groups__contains="ios")
norn = norn.filter(ios_filt)

# Call netmiko send command plugin on IOS hosts via run() method
my_results = norn.run(
    task=netmiko_send_command, command_string="show ip interface brief"
)

print_result(my_results)
