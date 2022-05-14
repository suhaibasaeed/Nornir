"""
1c. Write a custom task that uses the netmiko_send_config task-plugin to configure the SNMP chassis ID for all of the Cisco IOS and Arista EOS devices.
For the IOS devices use the "snmp_id" value in hosts.yaml.
For the EOS devices, configure the chassis ID to be the "snmp_id" attribute plus the name of the device (Nornir inventory name).
The EOS devices should be pulling the base snmp_id attribute from groups.yaml.

The syntax for the Cisco IOS devices is as follows:

   snmp-server chassis-id YOURSTRING

And for the Arista EOS devices:

   snmp chassis-id YOURSTRING-name
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config
from nornir.core.filter import F
from nornir.core.task import Result


def configure_snmp(task):
    # Create dict for platforms/commands - means we don't need if statement for each
    # Pull in snmp_id from data in hosts/groups.yaml
    command = {"ios": f"snmp-server chassis-id {task.host['snmp_id']} ",
            "eos": f"snmp chassis-id {task.host['snmp_id']}-{task.host.name}",
    }
    # Get group name and pass into dict get method which returns full command from data
    cmd = command.get(task.host.groups[0].name)
    # Send config to arista and IOS devices
    result = task.run(task=netmiko_send_config, config_commands=cmd)


if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute custom task against hosts in ios/eos groups
    nr = nr.filter(F(groups__contains='ios') | F(groups__contains='eos'))
    results = nr.run(task=configure_snmp)

    print_result(results)