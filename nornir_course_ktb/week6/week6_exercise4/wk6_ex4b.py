"""
4b. Expand on exercise4a to create a per-device session log for the two NX-OS devices (use the Nornir device "name" as part of the session_log file name).
Set the session_log name dynamically in a custom task.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from getpass import getpass
import os

# Task which sends command to device
def send_cmd(task):

    # Use host to dyanmically chose session log file name
    filename = f"{task.host}-output.txt"
    
    # Get group object
    group_obj = task.host.groups[0]
    # Set group objects extras key to write to unique log for each device
    group_obj.connection_options["netmiko"].extras["session_log"] = filename
    
    result = task.run(task=netmiko_send_command, command_string='show ip int br')

if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    # Loop through inventory and set password attr via env var
    for hostname, host_object in nr.inventory.hosts.items():
        host_object.password = os.environ.get("NORNIR_PASSWORD")
    
    agg_result = nr.run(task=send_cmd)

    
    
