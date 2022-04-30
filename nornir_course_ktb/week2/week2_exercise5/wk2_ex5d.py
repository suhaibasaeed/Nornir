"""
5d. Expand on exercise 5c except at the very end of your program, recover the failed host.
Print out the global failed hosts before and after you do this. At this point there should be no failed hosts.

"""

from nornir import InitNornir
from nornir.core.filter import F # Import F class which will be used for filtering inventory
from rich import print
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import os

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS group only
ios_filt = F(groups__contains="ios")
norn = norn.filter(ios_filt)

# Set password of cisco3 to an incorrect one so task will fail
norn.inventory.hosts["cisco3"].password = 'bogus'

# Call netmiko send command plugin on IOS hosts via run() method - cisco3 will fail
my_results = norn.run(task=netmiko_send_command, command_string="show ip interface brief")
print_result(my_results)

# Set cisco3's password to correct password again
norn.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]

print('RUN TASK ON FAILED HOST')
# Run the task again but only on the failed host cisco3 by reversing on_failed and on_good bools
scnd_task_results = norn.run(task=netmiko_send_command, command_string="show ip interface brief", on_failed=True, on_good=False)

print_result(scnd_task_results)

# Recover failed cisco3 host
print(f"Failed hosts: {norn.data.failed_hosts}")
norn.data.recover_host('cisco3')
print(f"Failed hosts: {norn.data.failed_hosts}")
