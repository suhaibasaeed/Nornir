"""
2c. Create a Nornir script that copies "arista_test.txt" from each of the remote Arista devices (secure copy, "get" operation)
It should then save the file as "eos/{device_name}-saved.txt" where {device_name} is the Nornir device name.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_file_transfer, netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

def file_copy(task):
    
    # Get platform name and source/dest filenames - used for file path
    platform = task.host.platform
    source_file = "arista_test.txt" # Filename on network device
    dest_file = f"{platform}/{task.host}"
    
    # Transfer the file
    results = task.run(
        netmiko_file_transfer,
        source_file=source_file,
        dest_file=dest_file,
        direction="get", # GET operation now and not PUT
    )

    print(task.host)
    # If file already present it's not transferred
    if results[0].changed is False:
        print("File not transferred: correct local file already exists")
    # If file not present and thus downloaded from the network device
    else:
        print("File downloaded")
    # If results attribute is not empty
    if results[0].result is True:
        print("Retrieved file exists and is correct")
    print("-" * 40)


if __name__ == "__main__":

    nr = InitNornir()
    # Filter on the EOS group
    eos = nr.filter(F(groups__contains="eos"))
    
    results = eos.run(task=file_copy)