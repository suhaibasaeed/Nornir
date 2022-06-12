"""
3a. Configure logging level specified in config.yaml to DEBUG; also change the logging output file name in config.yaml.
Create a Nornir script that executes a netmiko_send_command operation.

Watch the log file as the script executes (tail -f filename).

For this exercise and exercise 3b, set the credentials for the Nornir devices using getpass()
(instead of using a password embedded in inventory).
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from getpass import getpass

PASSWORD = getpass()

# Task which sends command to device
def send_cmd(task):

    result = task.run(task=netmiko_send_command, command_string='show version')

if __name__ == "__main__":

    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Loop through inventory and set password attr via getpass
    for hostname, host_object in nr.inventory.hosts.items():
        host_object.password = PASSWORD

    agg_result = nr.run(task=send_cmd)
    print_result(agg_result)