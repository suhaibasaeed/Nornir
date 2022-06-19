"""
4a. Write a script with a custom task that uses "napalm_configure" to deploy the same VLAN configuration as exercise 3.
"""
from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from nornir.core.filter import F

def nap_vlan(task, vlan_id, vlan_name):

    # config to send to the devices
    cfg = f"""vlan {vlan_id}
      name {vlan_name}"""
    
    # use napalm_configure task plugin to actually configure devices
    result = task.run(task=napalm_configure, configuration=cfg)
    

if __name__ == "__main__":
    # Initalise nornir and filter on EOS and NXOS groups
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains='eos') | F(groups__contains='nxos'))

    # Run custom task passing in vlan name and id
    results = nr.run(task=nap_vlan, vlan_id=16, vlan_name="SAS-TEST06")

    print_result(results)