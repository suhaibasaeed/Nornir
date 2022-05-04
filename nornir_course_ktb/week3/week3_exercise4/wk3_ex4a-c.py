"""
4a. Create a "config.yaml" file that uses hosts, groups and defaults inventory files in ~/nornir_inventory directory.

Create a Python script that creates a new Nornir object from inventory using the above config.yaml file.

4b. From your Nornir object in exercise4a, add a filter and select only the "eos" group.
Using the "netmiko_send_command" task-plugin, execute "show interface status" command against this "eos" group.
Ensure that you receive structured data back from Netmiko.

4c. From the results in exercise4b, process the interface table for all of the devices and create a single final dictionary.
The primary dictionary keys of this final dictionary should be the switch names.
The switch name keys should point to an inner dictionary.
The inner dictionary should have the interface names as keys and point to another internal dictionary.
This last internal dictionary should have keys of "status" and "vlan".
"""

from nornir import InitNornir
from rich import print
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Initialise Nornir
nr = InitNornir('config.yaml')

# 4b - Filter on EOS devices
arista = nr.filter(F(groups__contains='eos'))
# Send show int status command to device and return structured data
results = arista.run(task=netmiko_send_command, command_string='show interface status', use_textfsm=True)
#print_result(results)

# 4c - Loop through results and create new dict
final_dict, dev_dict = {}, {}
# Loop through host and Multiresult object
for host, v in results.items():
    # Parse to get to get actual result which is list of dicts
    device_result = v[0].result
    # Loop through list of dicts - one for each port
    for i in device_result:
        # Get info we need from dict
        port = i['port']
        status = i['status']
        vlan = i['vlan']
        # Add keys to inner dict which will have another dict inside it with port info
        dev_dict.update({port: {'status': status, 'vlan': vlan} })
    # Add keys to outer dict which will be hostname as key then inner dict and value. This has ports + info inside
    final_dict.update({host: dev_dict})
        
print(final_dict)



