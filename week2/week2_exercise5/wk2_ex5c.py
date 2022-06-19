"""
5c. Expand upon the Python program in exercise5b, this time add an additional task that runs *only* on the failed hosts.

In other words, the sequence of actions should be:

i. Filter your hosts to only be the "ios" hosts.

ii. Set the "password" for "cisco3" to be an invalid password.

iii. Execute "show ip int brief" on all of the "ios" hosts ("cisco3" will fail due to the invalid password).

iv. Set the "cisco3" password back to its correct value using os.environ["NORNIR_PASSWORD"] (this environment variable will be set in the lab environment).

v. Execute "show ip int brief" again, but this time execute the task only on the "failed_hosts" (i.e. cisco3).
This will require that you set the "on_good" and "on_failed" arguments that are used in the Nornir .run() method.

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
