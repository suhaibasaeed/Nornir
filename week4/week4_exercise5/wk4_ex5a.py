"""
5a. Write a script that captures the running configuration from "arista4" using the NAPALM "config" getter.
Print this configuration out to the screen.
"""

from rich import print
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# Initialise Nornir
nr = InitNornir('config.yaml')

# Filter on arista4
arista4 = nr.filter(name='arista4')

# Use config getter task-plugin to get configuration from devices in group
results = arista4.run(task=napalm_get, getters=['config'])
print_result(results)