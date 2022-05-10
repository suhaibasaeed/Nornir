"""
3a. Create a script with a custom task that accepts a vlan_id and a vlan_name as arguments.
Utilize the "netmiko_send_config" task-plugin to send the VLAN configuration to the "eos" and "nxos" hosts.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

def vlan(task, vlan_id, vlan_name):

    # Config to send to the devices
    config = [f"vlan {vlan_id}", f"name {vlan_name}"]
    # Use send_config task plugin
    result = task.run(task=netmiko_send_config, config_commands=config)
    # Return Result object and actual result from device
    return Result(host=task.host, result=result)


if __name__ == "__main__":
    # Initalise nornir and filter on EOS and NXOS groups
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains='eos') | F(groups__contains='nxos'))

    # Run custom task passing in vlan name and id
    results = nr.run(task=vlan, vlan_id=10, vlan_name="SAS-TEST")

    print_result(results)

