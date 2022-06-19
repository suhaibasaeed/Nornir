"""
Create a Nornir script that uses the "netmiko_file_transfer" task-plugin to transfer a small text file to one of the NX-OS devices.
After the file has been transferred, then create a custom Nornir task that uses Netmiko to delete this file. This custom task should do the following:

* Directly establish a Netmiko connection to the NX-OS device using "get_connection" (technically, it will be reusing the connection that was created in the netmiko_file_transfer task).
* Use the command "del bootflash:/{filename}" where {filename} is the name of the file you earlier transferred to the NX-OS device.

The delete command will prompt you as follows:
    nxos1# del bootflash:/testx.txt
    Do you want to delete "/testx.txt" ? (yes/no/abort)   [y] y

You will need to use Netmiko's send_command_timing method to handle these prompts.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_file_transfer
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

def transfer_file(task):
    # Specify file to send to device 
    filename = "nxos_test2.txt"
    # PUT operation to send file to device
    result = task.run(netmiko_file_transfer,
                      source_file=filename,
                      dest_file=filename,
                      direction="put")

def delete_file(task):

    # Manually create Netmiko connection and pass in config object
    net_conn = task.host.get_connection("netmiko", task.nornir.config)
    # List of cmds to send to device
    cmd_list = ["del bootflash:/nxos_test2.txt", "\n"]
    output = ""

    # Loop through cmds in list and send to device directly via netmiko method
    for cmd in cmd_list:
        output += net_conn.send_command_timing(cmd, strip_prompt=False, strip_command=False)
    
    print("#" * 80)
    print(task.host.name)
    print(output)
    print("#" * 80)
    
if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))

    send_results = nr.run(name="SEND FILE TO DEVICE", task=transfer_file)
    print_result(send_results)

    delete_results = nr.run(name="DELETE FILE FROM DEVICE",task=delete_file)