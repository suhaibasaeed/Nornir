from nornir import InitNornir # Function used to initialise nornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result # Function used to print output

# Initialise nornir by creating object using InitNornir function and pass in the config file
nornir = InitNornir('config.yml')
# List of commands we want to send to the devices
config_lst = ["interface loopback100", "description configured using Nornir-Netmiko"]

# Call run method on object and tell it to use netmiko and pass in the list of commands above to send to devices
result = nornir.run(netmiko_send_config, config_commands=config_lst)

print_result(result)

