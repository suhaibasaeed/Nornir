"""
5c. Using NAPALM configure, read configurations from rendered_configs dir and deploy the configs to nxos hosts.
Use a NAPALM merge operation for this task.

Use the NAPALM "bgp_neighbors" getter to verify that your BGP peering session becomes established.
Note, you might need to add a time.sleep delay between the configuration step and the verification step
(in other words allow the BGP session sufficient time to reach the established state).
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_napalm.plugins.tasks import napalm_get
import pdbr
from time import sleep


def deploy_config(task, config):

    # Get correct file name from dir via name attr of host and what type of config
    name =  task.host.name
    filename = f"rendered_configs/{name}_{config}.txt"

    # Open and read file into cfg
    with open(filename, "r") as fr:
        cfg = fr.read()
    # Use napalm_configure to push config to device
    result = task.run(task=napalm_configure, configuration=cfg)
 
if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute custom task against nxos devices only
    nr = nr.filter(F(groups__contains='nxos'))
    # Deploy interface config to the devices
    deploy_intf = nr.run(task=deploy_config, config='interfaces')
    print_result(deploy_intf)
    # Deploy bgp config to the devices
    deploy_bgp = nr.run(task=deploy_config, config='bgp')
    print_result(deploy_bgp)

    # Sleep for 20s to allow BGP neighbourship to form
    sleep(20)
    # Use NAPALM getter to verify BGP configuration
    napalm_bgp = nr.run(task=napalm_get, getters=['bgp_neighbors'])
    print_result(napalm_bgp)

    if napalm_bgp['nxos2'][0].result['bgp_neighbors']['global']['peers']['172.20.22.1']['is_up'] == True:
        print('BGP neighbourship is successful')