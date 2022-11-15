"""
5a. Create a custom task that retrieves a "checkpoint" from both of the NX-OS devices.
This custom task should create a direct NAPALM connection and should call the NAPALM _get_checkpoint_file() method.

Store the checkpoint in a host variable named "backup".

The script should print the checkpoint output to standard output using "print_result".
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

def get_checkpoint(task):

    # Manually create NAPALM connection
    napalm = task.host.get_connection("napalm", task.nornir.config)
    # Get checkpoint file and store in host object
    task.host["backup"] = napalm._get_checkpoint_file()

    return task.host["backup"]
    

if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    results = nr.run(task=get_checkpoint)

    print_result(results)