"""
6d. Finally, modify the code to capture all configurations (continue to use the "getters_options"), and the facts.
For each device, parse the data and indicate whether the startup and running configs match.
Print out this information along with some of the basic device information.
Your output should be similar to the following:

{'nxos1': {'model': 'Nexus9000 9000v Chassis',
           'start_running_match': True,
           'uptime': 7172937,
           'vendor': 'Cisco'},
 'nxos2': {'model': 'Nexus9000 9000v Chassis',
           'start_running_match': True,
           'uptime': 7172474,
           'vendor': 'Cisco'}}

Startup and running config contain timestamps--remove those timestamps before comparing the configurations!
"""

from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
import pdbr

final_dict, inner_dict = {}, {}
start_running_match = False

# Initialise Nornir
nr = InitNornir('config.yaml')

# Filter on devices in nxos group
nxos = nr.filter(F(groups__contains='nxos'))
print(nxos.inventory.hosts)

# Get running config and facts from device by passing in options as dict this time
results = nxos.run(task=napalm_get, getters=['config', 'facts'], getters_options={'config': {'retrieve': 'all' }})
#print_result(results)

for host, v in results.items():
    # Parse to get to get actual result which is list of dict like object
    device_result = v[0].result
    # Get startup/running config turn to a list and remove timestamp/! which will make comparison fail
    start_config = device_result['config']['startup'].split('\n')[1:]
    # Turn list back into a string
    start_config = '\n'.join(start_config)
    run_config = device_result['config']['running'].split('\n')[1:]
    run_config = '\n'.join(run_config)
    
    # If start and running config are the same set bool to True - used in final dict
    if start_config == run_config:
        start_running_match = True
    else:
        start_running_match = False

    # Extract info we need from facts dict
    model = device_result['facts']['model']
    uptime = device_result['facts']['uptime']
    vendor = device_result['facts']['vendor']
    
    inner_dict.update({'model': model, 'start_running_match': start_running_match, 'uptime': uptime, 'vendor': vendor})

    final_dict.update({host: inner_dict})

print(final_dict)
    

