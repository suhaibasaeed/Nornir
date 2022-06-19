"""
4a. In a new script, create a Jinja2 representation of the ACL from the previous task;
this Jinja2 template should just be an embedded string in your script.
Using the same external YAML/JSON file for source data,
construct the ACL from the previous task, render it, and print this ACL out to standard output.
Your output should be identical to the output of exercise3.
"""

from re import template
from nornir_utils.plugins.tasks.data import load_yaml
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_jinja2.plugins.tasks import template_string

# j2 template in string format
TEMPLATE_STR =  """{% for i in entries %}
set firewall family inet filter {{ filter_name }} term {{ i.term_name }} from protocol {{ i.protocol }}
set firewall family inet filter {{ filter_name }} term {{ i.term_name }} from destination-port {{ i.destination_port }}
set firewall family inet filter {{ filter_name }} term {{ i.term_name }} from destination-address {{ i.destination_address }}
set firewall family inet filter {{ filter_name }} term {{ i.term_name }} then {{ i.state }}
{% endfor %}"""

def j2_render(task):
    
    # Load data from yaml file and parse to get dict
    fw_rules = task.run(task=load_yaml, file="acl.yaml")
    fw_dict = fw_rules[0].result
    # Unpack into string and list of dictionaries - one for each rule
    fw_filter_name, fw_filter_entries = list(fw_dict.items())[0]
    
    # Use template_string task plugin and pass in template and vars
    result = task.run(
        task=template_string, template=TEMPLATE_STR, filter_name=fw_filter_name,
        entries=fw_filter_entries)
    # Parse through MultiResult object
    print(result[0].result)

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir()
    # Execute custom task against srx2 only
    nr = nr.filter(name='srx2')
    results = nr.run(task=j2_render)