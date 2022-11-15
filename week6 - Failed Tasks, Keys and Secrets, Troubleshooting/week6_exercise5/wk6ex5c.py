"""
5b. Expand on exercise5a, except randomly change the password on some of your devices in inventory 
(this is prior to executing the custom task that connects to those devices). This can be accomplished using the "random.choice" function as follows:

for host, data in nr.inventory.hosts.items():
    if random.choice([True, False]):
       data.password = BAD_PASSWORD

This will of course cause the "send_command" task to fail due to authentication issues.

Now, catch the NornirSubTaskError exception (if the sub task exception is "NetMikoAuthenticationException") and then set the host password back to "88newclass".
After this is done, re-execute the Netmiko "send_command" task (all of this code should be inside of your custom task).

Re-run your script, the end result of this should be that the appropriate data is gathered from all devices in the inventory.
The devices that failed authentication the first time should have been corrected and executed correctly on the second attempt.

Note, you will probably want to execute the following (inside your NornirSubTaskError exception handler to remove the failed connection attempt):

    task.results.pop()

This will make your print_results output much cleaner (i.e. it will remove the failed SSH attempt from the print_results output).
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirSubTaskError
from netmiko.ssh_exception import NetmikoAuthenticationException
import os
import random

BAD_PASSWORD = "dDFDFGRFGS" 

# Task which sends command to device
def send_cmd(task):
    # Choose specific command based on group
    if str(task.host.groups[0]) == 'junos':
        cmd = 'show system uptime'
    else:
        cmd = 'show clock'
    
    try:

        result = task.run(task=netmiko_send_command, command_string=cmd)
    # If the password is wrong
    except (NornirSubTaskError, NetmikoAuthenticationException):
        print(f"{task.host.name} has incorrect password")
        # Remove failed SSH attempt from results so we get 2nd attempt result
        task.results.pop()
        # Set correct password from env vars
        task.host.password = os.environ.get("NORNIR_PASSWORD")
        # Re-run task
        result = task.run(task=netmiko_send_command, command_string=cmd)
        
        



if __name__ == "__main__":

    nr = InitNornir("config.yaml")
    # Loop through inventory and randomly give hosts wrong password
    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = BAD_PASSWORD
    
    results = nr.run(task=send_cmd)
    
    print_result(results)