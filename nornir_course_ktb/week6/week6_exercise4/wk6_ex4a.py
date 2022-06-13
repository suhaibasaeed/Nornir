"""
4a. Setup the Cisco NX-OS devices to use a Netmiko session log. Use a single session log defined in groups.yaml for both NX-OS devices.
Set runner plugin to "serial" so that threading doesn't cause issues with the session_log.

Create a Nornir script that uses the "netmiko_send_command" task-plugin and executes on only these two NX-OS devices.
Monitor the output of the session log file and see what is occurring in the Netmiko session.
For this exercise & ex 4b, set the password using an environment variable (instead of using a password embedded in inventory).
Once again, you can use "tail -f filename" to tail the session_log file to see what is happening real-time.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from getpass import getpass
import os

# Task which sends command to device
def send_cmd(task):

    result = task.run(task=netmiko_send_command, command_string='show ip int br')

if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    # Loop through inventory and set password attr via env var
    for hostname, host_object in nr.inventory.hosts.items():
        host_object.password = os.environ.get("NORNIR_PASSWORD")
    
    agg_result = nr.run(task=send_cmd)

    
    
