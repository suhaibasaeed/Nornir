"""
4c. Add a step to your custom task to render the ACL as an attribute of SRX2 host
Store the rendered value as an attribute of the "srx2" host
(in other words, store the ACL data in the Nornir host object).
Once again print the fully rendered ACL to standard out
(this time using the host object attribute where you stored the ACL data).
"""

from nornir_utils.plugins.tasks.data import load_yaml
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_jinja2.plugins.tasks import template_file

def j2_render(task):
    
    # Load data from yaml file and parse to get dict
    fw_rules = task.run(task=load_yaml, file="acl.yaml")
    fw_dict = fw_rules[0].result
    # Unpack into string and list of dictionaries - one for each rule
    fw_filter_name, fw_filter_entries = list(fw_dict.items())[0]
    
    # Use template_file task plugin and pass in template, path and vars
    result = task.run(
        task=template_file, template="fw_template.j2", path=".", filter_name=fw_filter_name,
        entries=fw_filter_entries)
    # Parse through MultiResult object then add to host object as attribute
    config = result[0].result
    task.host['fw_config'] = config

    print(task.host['fw_config'])

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir()
    # Execute custom task against srx2 only
    nr = nr.filter(name='srx2')
    results = nr.run(task=j2_render)