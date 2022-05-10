"""
2a. Create a new directory named "eos". In this "eos" directory create a file named "arista_test.txt".
In this "arista_test.txt" file add some unique content that you will be able to identify.
This unique content will let verify that your particular file was transferred to the remote device.

Next, copy the hosts.yaml, groups.yaml, and defaults.yaml files from ~/nornir_inventory to your current directory.
Modify the groups.yaml file and add the following to the "eos" group:
  data:
    file_name: arista_test.txt

Now, using the "netmiko_file_transfer" task-plugin,
secure copy your arista_test.txt file to all of the Arista switches in the lab environment.

Please use the "platform" attribute from inventory to specify the directory name.
Additionally, please use the "file_name" variable from inventory.
In other words, construct "eos/arista_test.txt" entirely from inventory information.

Note, you will want to pass the following argument into the "netmiko_file_transfer" task-plugin:
    overwrite_file=True,

This will allow the "netmiko_file_transfer" task-plugin to overwrite the file if it already exists.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_file_transfer
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

nr = InitNornir()
# Filter on the EOS group
eos = nr.filter(F(groups__contains="eos"))

# Get platform name and file name from inventory - used for file path
platform = eos.inventory.groups['eos'].platform
file_name = eos.inventory.groups['eos'].data['file_name']
source_file = f"{platform}/{file_name}"

# Transfer the file to the device and overwrite if it already exists
results = eos.run(
    netmiko_file_transfer,
    source_file=source_file,
    dest_file=file_name,
    direction='put',
    overwrite_file=True)

print_result(results)