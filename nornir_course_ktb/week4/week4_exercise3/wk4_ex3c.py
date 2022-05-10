"""
3c. Modify your custom task to return a Nornir Result object. Set the value of changed, failed, and result.
These values should correspond to what happened in the custom task.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_send_config, netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

# Subtask
def vlan_check_configure(task, vlan_id, vlan_name):

    # Set default is False as it should only be true if command executed
    changed = False
    # Check to see if vlan already exists by issuing show vlan
    vlan_output = task.run(task=netmiko_send_command, command_string="show vlan")
    
    # Configure VLAN if it's not already in the results
    if vlan_name not in vlan_output[0].result:
        # Config to send to the devices
        config = [f"vlan {vlan_id}", f"name {vlan_name}"]
        # Use send_config task plugin
        result = task.run(task=netmiko_send_config, config_commands=config)
        # If above line succesful then a change actually happened so change bool
        changed = True
    # No change needed as VLAN already there
    else:
        result = "No change necessary"
        
    # Return Result object and actual result from device as well as changed/failed bools
    return Result(host=task.host, result=result, changed=changed, failed=False)


if __name__ == "__main__":
    # Initalise nornir and filter on EOS and NXOS groups
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains='eos') | F(groups__contains='nxos'))

    # Run custom task passing in vlan name and id
    results = nr.run(task=vlan_check_configure, vlan_id=12, vlan_name="SAS-TEST03")

    print_result(results)

