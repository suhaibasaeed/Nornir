"""
2b. Expanding on exercise 2a, update the transform function (or host-object loop equivalent) such that the connection options also support NAPALM tasks.

This will require:
Setting the "platform" value for the NAPALM connection_options
Update the NX-OS port value to 8443

Create a Nornir script that uses this new transform_function.
In your Nornir script, filter your inventory down to only the "nxos" group.
Execute a NAPALM "get_facts" against the two NX-OS devices and confirm that the NAPALM task is working properly.
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get

platform = {"cisco": "cisco_ios",
            "nxos": "cisco_nxos",
            "juniper": "juniper_junos",
            "arista": "arista_eos",
            }

# Transform function convert ansible inventory to work with Nornir Netmiko
def transform_ansible(host):
    # Set host's password attr
    host.password = host["ansible_ssh_pass"]
    # Set platform key in connection_options Netmiko section
    netmiko_params = host.get_connection_parameters("netmiko")
    netmiko_params.platform = platform.get(str(host.groups[0]))
    # Set global_delay_factor on EOS devices
    if str(host.groups[0]) == "arista":
        netmiko_params.extras["global_delay_factor"] = 2
    
    # Update connection_options attr for host obj
    host.connection_options["netmiko"] = netmiko_params

    # NAPALM section - Set platform plus port only for NXOS
    #import pdbr; pdbr.set_trace()
    napalm_params = host.get_connection_parameters("napalm")
    napalm_params.platform = platform.get(str(host.groups[0])).split("_")[1]
    
    if host.groups[0].name == "nxos":
        napalm_params.port = 8443
    
    # Update connection_options attr for host obj
    host.connection_options["napalm"] = napalm_params



if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    
    # Loop through inventory and add attributes
    for host in nr.inventory.hosts.values():
        transform_ansible(host)

    # Get facts via NAPALM
    results = nr.run(name="GET FACTS", task=napalm_get, getters=["get_facts"])
    print_result(results)