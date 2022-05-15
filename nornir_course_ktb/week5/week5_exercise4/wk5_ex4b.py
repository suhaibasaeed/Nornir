"""
4b. Create an "acl.j2" file that is the Jinja2 representation of the ACL from the previous task.
Recreate your script from exercise4a except use the external Jinja2 file for the template.
Your output should once again be the fully generated ACL.
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
    # Parse through MultiResult object and print output
    print(result[0].result)

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir()
    # Execute custom task against srx2 only
    nr = nr.filter(name='srx2')
    results = nr.run(task=j2_render)