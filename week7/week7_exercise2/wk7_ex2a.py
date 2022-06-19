"""
2a. Copy the `ansible-hosts` file from your user directory.
This Ansible inventory file contains all of the hosts for the course's lab environment; however, it is *not* setup for Nornir.
In other words, the "connection_options" are not configured.

Write a transform function (or loop over the Nornir Host objects)
that converts this Ansible inventory such that this inventory could be used with a Netmiko task. This task will require several steps:

Setting the Nornir host "password" to the value of "ansible_ssh_pass" (which is set in the "all" group in the ansible-hosts inventory).
Setting the "platform" value for the Netmiko connection_options
Set the "extras > global_delay_factor" for the Arista devices to a value of 2

Run a simple Netmiko send command task that validates that the transform_function and the inventory are working properly.
Use the "show version" command as this will succeed on all of the platforms. You should exclude "localhost" from the set of hosts for this task.
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F

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



if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Loop through inventory and add attributes
    for host in nr.inventory.hosts.values():
        transform_ansible(host)

    
    # Exclude localhost device and send show version to the devices
    nr = nr.filter(~F(groups__contains='local'))
    results = nr.run(name="SHOW VERSION", task=netmiko_send_command, command_string="show version")
    print_result(results)