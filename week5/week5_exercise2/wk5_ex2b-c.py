"""
2b. Create a script initialize Nornir and filter the inventory to just the eos" devices.
Next use the "napalm_get" task-plugin and use the "config" getter to retrieve the configuration
Execute the script--at this point the script should fail as the eAPI port is not port 22!

2c. Modify your "groups.yaml" file such that your script succeeds.
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.filter import F


if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute napalm_get config task against hosts in eos groups
    nr = nr.filter(F(groups__contains='eos'))
    results = nr.run(task=napalm_get, getters=["config"])
    print_result(results)