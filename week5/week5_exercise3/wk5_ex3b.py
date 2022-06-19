"""
3b. Filter the Nornir inventory to just the srx2 device.
Write a custom task to generate the firewall rules for each entry in the YAML/JSON file. Print the generated rules to your standard output. Your output should look as follows:

set firewall family inet filter my_acl term rule1 from protocol tcp
set firewall family inet filter my_acl term rule1 from destination-port 22
set firewall family inet filter my_acl term rule1 from destination-address 1.2.3.4/32
set firewall family inet filter my_acl term rule1 then accept
set firewall family inet filter my_acl term rule2 from protocol tcp
set firewall family inet filter my_acl term rule2 from destination-port 443
set firewall family inet filter my_acl term rule2 from destination-address 1.2.3.4/32
set firewall family inet filter my_acl term rule2 then accept
set firewall family inet filter my_acl term rule3 from protocol tcp
set firewall family inet filter my_acl term rule3 from destination-port 443
set firewall family inet filter my_acl term rule3 from destination-address 1.2.3.4/32
set firewall family inet filter my_acl term rule3 then discard

You do not need to push these configuration changes out to the SRX.
"""

from nornir_utils.plugins.tasks.data import load_yaml
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir.core.task import Result

def generate_fw_rules(task):
    # Load data from yaml file and parse to get dict
    fw_rules = task.run(task=load_yaml, file="acl.yaml")
    fw_dict = fw_rules[0].result
    # Unpack into string and list of dictionaries - one for each rule
    fw_filter_name, fw_filter_entries = list(fw_dict.items())[0]

    for i in fw_filter_entries:
        
        print(f"set firewall family inet filter {fw_filter_name} term {i['term_name']} from protocol {i['protocol']}")
        print(f"set firewall family inet filter {fw_filter_name} term {i['term_name']} from destination-port {i['destination_port']}")
        print(f"set firewall family inet filter {fw_filter_name} term {i['term_name']} from destination-address {i['destination_address']}")
        print(f"set firewall family inet filter {fw_filter_name} term {i['term_name']} then {i['state']}")
    
    

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir()
    # Execute custom task against srx2 only
    nr = nr.filter(name='srx2')
    results = nr.run(task=generate_fw_rules)