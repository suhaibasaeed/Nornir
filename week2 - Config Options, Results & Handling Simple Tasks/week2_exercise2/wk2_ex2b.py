"""
2b. Create a Python script that uses netmiko_send_command to execute "show run | inc hostname" on all the "ios" devices in your inventory
(once again use the filter that you created in exercise 2a). Assign the result of this task to a variable named "my_results".

Print the "type" of the my_results object. Additionally, inspect the my_results object using its "keys()", "items()" and "values" methods.
"""

from nornir import InitNornir
from nornir.core.filter import F # Import F class which will be used for filtering inventory
from rich import print
from nornir_netmiko import netmiko_send_command

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS group only
ios_filt = F(groups__contains="ios")
norn = norn.filter(ios_filt)

# Call netmiko send command plugin on IOS hosts via run() method
my_results = norn.run(task=netmiko_send_command, command_string="show run | inc hostname")

# Print type of return data structure
print(type(my_results))
print()

# Inspect returned object
print(my_results.keys())
print(my_results.values())

for k, v in my_results.items():
    print('*' * 30)
    print(k)
    print(v[0].result)
    print('*' * 30)





