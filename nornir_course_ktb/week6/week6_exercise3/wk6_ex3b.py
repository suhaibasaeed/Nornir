"""
3b. Add a logger configuration into your Nornir script and send a few log messages at the "debug", "error", and "critical" levels.
Confirm your messages make it into your log file.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from getpass import getpass
from logging import getLogger

PASSWORD = getpass()

# Task which sends command to device
def send_cmd(task):

    result = task.run(task=netmiko_send_command, command_string='show version')

if __name__ == "__main__":

    # Get access to Nornirs python logger
    logger = getLogger("nornir")
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Loop through inventory and set password attr via getpass
    for hostname, host_object in nr.inventory.hosts.items():
        host_object.password = PASSWORD

    logger.debug("This is a debug message")
    logger.error("This is an error message")
    agg_result = nr.run(task=send_cmd)
    logger.critical("This is a critical message")
    print_result(agg_result)