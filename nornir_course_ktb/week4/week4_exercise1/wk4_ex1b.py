"""
1b. Process the returned uptime string and convert it over to uptime seconds.
If the uptime is less than 1 day, then print out a notice that the device recently rebooted.

Note, you can skip the uptime string conversion for the Juniper device.
Just have it return a value of 90 seconds for the "uptime seconds"
(in other words, artificially pretend that the Juniper device just rebooted).
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F
from nornir.core.task import Result
from parse import parse_uptime # Function from KTB
from re import search


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
    
    # Use re to match on only actual uptime and remove everything else
    uptime = search(r'\s\d+.*', result[0].result) # Result attribute

    # Pass uptime into function to get uptime in seconds - index 0 as we're returned list
    uptime_sec = parse_uptime(uptime[0])
    # If device is SRX2 just manually set uptime in seconds
    if task.host.name == "srx2":
        uptime_sec = 90
    # If uptime is under a day
    if uptime_sec < 86400:
        print(f"{task.host.name} rebooted within the last day")
    else:
        print(f"{task.host.name} has been up for longer than a day")
    

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute custom task against hosts in inventory
    results = nr.run(task=device_uptime, name="Get device uptime")





