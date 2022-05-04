"""
6a. Using the config.yaml file from exercise 4, create a new Nornir object that filters to only the "nxos" devices.
Using the "napalm_get" task-plugin, retrieve the configuration from these devices. Print the results of this task.

6b. Filter the napalm "get" to capture only the running configuration. Print the results of the task.

6c. Modify the script to get the running configuration AND facts from the device. Once again, print the results.
"""

from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# Initialise Nornir
nr = InitNornir('config.yaml')

# 6a - Filter on devices in nxos group
nxos = nr.filter(F(groups__contains='nxos'))
print(nxos.inventory.hosts)

# Use config getter task-plugin to get configuration from devices in group
results = nxos.run(task=napalm_get, getters=['config'])
#print_result(results)

# 6b - Get running config only this time via config getter
b_results = nxos.run(task=napalm_get, getters=['config'], retrieve='running')
#rint_result(b_results)

# 6c - Get running config and facts from device by passing in options as dict this time
c_results = nxos.run(task=napalm_get, getters=['config', 'facts'], getters_options={'config': {'retrieve': 'running'}})
print_result(c_results)
