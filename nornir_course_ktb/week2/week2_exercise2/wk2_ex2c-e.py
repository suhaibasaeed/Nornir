"""
2c. Assign the results from "cisco3" to a new variable named "host_results".
Inspect this new MultiResult object: access the zeroith element from this MultiResult object.
Finally, determine if "host_results" is an iterable or not.

2d. Assign the zeroith element of the host_results object to a new variable named "task_result".
What type of object is task_result? Print out the 'host', 'name', 'result', and 'failed' attributes from task_result.
Which field actually contains the output from the network device?

2e. Looking back at exercises 2a - 2d: explain what Nornir result types are "my_results", "host_results", and "task_result"?
What purpose does each of those three data types serve (i.e. why do we have them)?
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

# 2c - Get only cisco3 info and inspect data MultiResult object
host_results = my_results['cisco3']
print(type(host_results))
print()

# 2d - Get first element in list i.e result of first task executed
task_result = host_results[0]

print(type(task_result))

# Print attributes of Result object
print(task_result.host)
print(task_result.name)
print(task_result.result)
print(task_result.failed)






