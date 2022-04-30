"""
5b. Expanding on exercise 5a, set the 'cisco3' password attribute to an invalid value. The code to do this would be similar to the following:
nr.inventory.hosts["cisco3"].password = 'bogus'

Re-run your Nornir task and print out the "failed_hosts" using both the results object (results.failed_hosts) and the Nornir object (nr.data.failed_hosts)

"""

from nornir import InitNornir
from nornir.core.filter import F # Import F class which will be used for filtering inventory
from rich import print
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS group only
ios_filt = F(groups__contains="ios")
norn = norn.filter(ios_filt)

# Set password of cisco3 to an incorrect one so task will fail
norn.inventory.hosts["cisco3"].password = 'bogus'

# Call netmiko send command plugin on IOS hosts via run() method
my_results = norn.run(task=netmiko_send_command, command_string="show ip interface brief")

# Print out the hosts which the tasks have failed on
print("Failed hosts")
print(norn.data.failed_hosts)
print(my_results.failed_hosts)
