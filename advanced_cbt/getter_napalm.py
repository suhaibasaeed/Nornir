from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli
from nornir_utils.plugins.functions import print_result

# Initialise nornir by creating object using InitNornir function and pass in the config file
nornir = InitNornir('config.yml')

# Call run method on object and tell it to use napalm and the interfaces getter
result = nornir.run(task=napalm_get, getters=["interfaces"])
print_result(result)