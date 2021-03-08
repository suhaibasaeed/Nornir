from nornir import InitNornir # Function used to initialise nornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result # Function used to print output
# Initiliase nornir by creating object using InitNornir function and pass in the config file
nornir = InitNornir('config.yml')
# Call run method on object and tell it to use netmiko and specify the command we want to send
result = nornir.run(netmiko_send_command, command_string="show ip int br")
# Use function to print output
print_result(result)

