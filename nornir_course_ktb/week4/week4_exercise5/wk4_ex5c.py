"""
5c. Create a new program that combines both exercise5a and exercise5b.
First, retrieve the current running configuration from Arista4, then configure the loopback interface.
Finally, use "napalm_configure" and configuration replace operation to restore the previously captured running configuration.
The net effect of this last step should be to remove the loopback configuration (i.e. to restore the running configuration to its original state).
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure
from nornir_utils.plugins.functions import print_result

arista4_loopback = """interface loopback124
  description Hello from SAS"""

if __name__ == "__main__":
   
   # Initialise Nornir
   nr = InitNornir('config.yaml')
   # Filter on arista4
   arista4 = nr.filter(name='arista4')

   # Use getter to retreive running config from device
   result = arista4.run(task=napalm_get, getters=["config"], retrieve="running")
   # Parse through objects to get what we want
   arista4_running = result['arista4'].result['config']['running']
   
   # Configure loopback so our captured config is different to new running config
   result = arista4.run(task=napalm_configure, configuration=arista4_loopback)

   # Now do replace operation by setting bool to True - This will override current config with one we got via getter
   result = arista4.run(task=napalm_configure, configuration=arista4_running, replace=True)

   print_result(result)