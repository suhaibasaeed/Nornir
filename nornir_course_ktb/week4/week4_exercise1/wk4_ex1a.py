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