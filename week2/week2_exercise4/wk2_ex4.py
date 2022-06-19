"""
4. Using a NAPALM getter instead of Netmiko, capture the ARP table output from all of the EOS and IOS devices.
The NAPALM "arp_table" getter will return a list of dictionaries.
In this list of dictionaries each inner-dictionary will correspond to one entry in the ARP table.

Post-process the data retrieved from this NAPALM getter and print out the "host" name (for example, "cisco3", "cisco4") 
and the NAPALM inner dictionary corresponding to the MAC address of the default gateway. For both exercise3 and exercise4, you can just hard-code the gateway value into your code.
In other words, you do not need to dynamically determine the default gateway.
"""

from nornir import InitNornir
from nornir.core.filter import F # Import F class which will be used for filtering inventory
from rich import print
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

DEFAULT_GATEWAY = '10.220.88.1'

# Create norn object by initialising Nornir - Pass in config file
norn = InitNornir("config.yaml")

# Filter on inventory to select IOS and EOS group
ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
norn = norn.filter(ios_filt | eos_filt)

# Call NAPALM get plugin on IOS/EOS hosts via run() method
my_results = norn.run(task=napalm_get, getters=["arp_table"])

# Loop through results and parse default gateway ARP entry
for host, result in my_results.items():
    # Loop through arp entries by parsing to get arp_table dict from result attribute
    for entry in result[0].result['arp_table']:
        # Look for default gateway IP 
        if entry['ip'] == DEFAULT_GATEWAY:
            print(f"Host: {host}, Gateway: {entry}")