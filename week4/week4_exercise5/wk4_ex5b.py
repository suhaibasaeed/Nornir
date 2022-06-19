"""
5b. Use napalm_configure to add a new loopback interface to the "arista4" device.
Your configuration should be similar to the following:
interface Loopback123
   description Hello
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_napalm.plugins.tasks import napalm_configure

arista4_loopback = """interface loopback123
  description Hello"""


if __name__ == "__main__":
   
   # Initialise Nornir
   nr = InitNornir('config.yaml')
   # Filter on arista4
   arista4 = nr.filter(name='arista4')

   # Send loopback confing to arista4 device via napalm_configure task plugin
   result = arista4.run(task=napalm_configure, configuration=arista4_loopback)

   print_result(result)