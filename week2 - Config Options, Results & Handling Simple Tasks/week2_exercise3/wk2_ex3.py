"""
3. Using the Nornir filter pattern shown below and the 'netmiko_send_command' task-plugin capture the output of 'show ip arp' from all of the Cisco-IOS and Arista-EOS devices.

NOTE: We will cover filtering inventory later in the course, but for now, add the following to your script after initializing your Nornir object.
This will filter the Nornir hosts to be only the IOS and EOS devices:
ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

Process the "show ip arp" results such that only the default gateway is retained from the ARP table.
Note, please accomplish this exercise by handling the AggregatedResult and MultiResult in your Python program instead of using a router CLI command 
(i.e. do not do "show ip arp | include gateway"). In other words, the purpose of this exercise is for you to gain familiarity with handling Nornir result objects.

For both exercise3 and exercise4, you can just hard-code the gateway value into your code. In other words, you do not need to dynamically determine the default gateway.

Print output similar to the following to standard output 
(the "Host" should be the Nornir host that you retrieved the ARP data from; the "Gateway" should be the "show ip arp" gateway entry from that Host).
Note, the IP address of the default gateway and its corresponding MAC address might be different in your lab environment.

Host: cisco3, Gateway: Internet 10.220.88.1 8 0062.ec29.70fe ARPA GigabitEthernet0/0/0
Host: cisco4, Gateway: Internet 10.220.88.1 8 0062.ec29.70fe ARPA GigabitEthernet0/0/0
Host: arista1, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
Host: arista2, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
Host: arista3, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
Host: arista4, Gateway: 10.220.88.1 N/A 0062.ec29.70fe Vlan1, Ethernet1
"""

from nornir import InitNornir
from nornir.core.filter import (
    F,
)  # Import F class which will be used for filtering inventory
from rich import print
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

DEFAULT_GATEWAY = "10.220.88.1"

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS and EOS group
ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
norn = norn.filter(ios_filt | eos_filt)

# Call netmiko send command plugin on IOS hosts via run() method
my_results = norn.run(task=netmiko_send_command, command_string="show ip arp")

# Loop through results and parse default gateway ARP entry
for host, result in my_results.items():
    # Loop and get Result object's result attribute and turn it into list - one element per ARP entry
    for entry in result[0].result.split("\n"):
        # Find ARP entry with default gateways IP
        if DEFAULT_GATEWAY in entry:
            print(f"Host: {host}, Gateway: {entry}")
