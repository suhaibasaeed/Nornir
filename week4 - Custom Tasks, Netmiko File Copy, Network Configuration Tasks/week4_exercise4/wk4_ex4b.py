"""
4b. Modify your custom task to add a keyword argument for the "dry_run" setting.
Set this argument to False by default.

In the main part of your program call this custom task and test both dry_run=True and dry_run=False.
Note, for napalm_configure and dry_run=True, NAPALM will not actually make any configuration 
--instead NAPALM and Nornir will report whether any changes would have been made.
"""
from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from nornir.core.filter import F

# Custom task - set dry_run to False by default
def nap_vlan(task, vlan_id, vlan_name, dry_run=False):

    # config to send to the devices
    cfg = f"""vlan {vlan_id}
      name {vlan_name}"""
    
    # use napalm_configure task plugin to actually configure devices
    result = task.run(task=napalm_configure, configuration=cfg, dry_run=dry_run)
    

if __name__ == "__main__":
    # Initalise nornir and filter on EOS and NXOS groups
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains='eos') | F(groups__contains='nxos'))

    # Run custom task passing in vlan name and id
    results = nr.run(task=nap_vlan, vlan_id=16, vlan_name="SAS-TEST07")

    print_result(results)