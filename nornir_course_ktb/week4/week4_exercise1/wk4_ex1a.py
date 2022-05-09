"""
1a. Create a custom task that uses the 'netmiko_send_command' task-plugin to query all of the lab devices for their uptime.
This task will require that you execute different commands based on the platform (see the table below):
Platform                    Command
--------                    -----------
Cisco IOS/NX-OS             show version | inc uptime
Arista                      show version | inc Uptime
Juniper SRX                 show system uptime | match System

Print out the Nornir device name and the uptime string for each of the hosts.
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F
from nornir.core.task import Result


# Custom task which gets uptime of device
def device_uptime(task):
    
    # Dict which stores platform and commands - means we don't need if statement for each
    command = {"ios": "show version | inc uptime",
               "nxos": "show version | inc uptime",
               "eos": "show version | inc Uptime",
               "junos": "show system uptime | match System"
    }
    # Get group name and pass into dict get method which returns command
    cmd = command.get(task.host.groups[0].name)
    # Execure task serially against devices
    result = task.run(task=netmiko_send_command, command_string=cmd)
    
    # Print host and result - Parse through list like MultiResult object
    print(task.host.name)
    print(result[0])
    

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute custom task against hosts in inventory
    results = nr.run(task=device_uptime, name="Get device uptime")




