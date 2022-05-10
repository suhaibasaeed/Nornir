"""
2b. Repeat exercise2a except now create a custom task that performs both a file transfer and a verify operation.
The custom_task should execute the "netmiko_file_transfer" task-plugin (as before) and should also execute the following command
(using the "netmiko_send_command" task-plugin):
more flash:/arista_test.txt
Your program should print the contents of the remote file to the screen.
"""

from nornir import InitNornir
from nornir_netmiko import netmiko_file_transfer, netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

def file_trans_verify(task):

    # Get platform name and file name from inventory - used for file path
    platform = task.host.platform
    file_name = task.host.groups[0].data['file_name']
    source_file = f"{platform}/{file_name}"

    # Transfer the file to the device and overwrite if it already exists
    results = task.run(
        netmiko_file_transfer,
        source_file=source_file,
        dest_file=file_name,
        direction='put',
        overwrite_file=True)
    
    # Check if correct file and contents is on device by doing more command on file
    check_result = task.run(netmiko_send_command, command_string='more flash:/arista_test.txt')

    # Return Result object
    return Result(host=task.host, result=check_result)

if __name__ == "__main__":

    nr = InitNornir()
    # Filter on the EOS group
    eos = nr.filter(F(groups__contains="eos"))
    
    results = eos.run(task=file_trans_verify)
    print_result(results)