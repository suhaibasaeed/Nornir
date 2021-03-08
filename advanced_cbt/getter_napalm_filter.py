from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli
from nornir_utils.plugins.functions import print_result

# Initialise nornir by creating object using InitNornir function and pass in the config file
nornir = InitNornir('config.yml')
# Use filter to only run the commands on a single device - DEV02
r2 = nornir.filter(name="DEV02")

# Call run method on r2 object and tell it to use napalm and pass commands in
result = r2.run(napalm_cli, commands=['show version', 'show ip interface brief'])
print_result(result)





