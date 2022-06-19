"""
1b. Modify your custom task to raise a ValueError exception if "syntax error" is detected in the Netmiko send_command output.
This exception raising should be inside the custom task.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result


# Task which sends incorrect command to device
def invalid_cmd(task):
    
    result = task.run(task=netmiko_send_command, command_string='show ip interface')
    
    if 'syntax error' in result[0].result:
        raise ValueError("Command syntax incorrect - Please fix and re-try")


if __name__ == "__main__":

    # Initialise Nornir and filter on SRX2 device only
    nr = InitNornir("config.yaml")
    nr = nr.filter(name='srx2')
    
    agg_result = nr.run(task=invalid_cmd)
    print_result(agg_result)

