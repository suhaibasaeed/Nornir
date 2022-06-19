"""
5a. Create a Nornir script that includes a custom task that executes "show clock" on the Cisco IOS, Arista EOS, and Cisco NX-OS devices.
This same custom task should execute "show system uptime" on the Juniper SRX. Use the "print_result" function to verify the output of this task is correct.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Task which sends command to device
def send_cmd(task):
    # Choose specific command based on group
    if str(task.host.groups[0]) == 'junos':
        cmd = 'show system uptime'
    else:
        cmd = 'show clock'
    
    result = task.run(task=netmiko_send_command, command_string=cmd)


if __name__ == "__main__":

    nr = InitNornir("config.yaml")
    results = nr.run(task=send_cmd)
    
    print_result(results)