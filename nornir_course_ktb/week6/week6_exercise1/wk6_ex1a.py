"""
1a. Create a Nornir script that will send an invalid command to the Junos "srx2" device
(for example, "show ip interface" does not work on Junos).

Netmiko will not attempt to interpret the output of this invalid command.

Use the "print_result" function to ensure that the task succeeded and to inspect the output received back from the device.
Note, the "syntax error" message is from the Junos SRX and is not a Python exception.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result


# Task which sends incorrect command to device
def invalid_cmd(task):

    result = task.run(task=netmiko_send_command, command_string='show ip interface')

if __name__ == "__main__":

    # Initialise Nornir and filter on SRX2 device only
    nr = InitNornir("config.yaml")
    nr = nr.filter(name='srx2')
    
    agg_result = nr.run(task=invalid_cmd)
    print_result(agg_result)

