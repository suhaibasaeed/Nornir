from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir.core.task import Result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file
import pdbr

def render_configs(task, template_name):
    
    # Use group name to set folder to get templates from
    template_path = f"{task.host.groups[0]}/"

    # Run template_task plugin passing vars from host and template from func arg
    result = task.run(task=template_file, template=template_name, path=template_path,
    **task.host)

    # Parse output of rendered config from MultiResult object
    rendered_config = result[0].result

    # Store the rendered config in the host object for acessing later
    task.host[f'{template_name.rstrip(".j2")}_config'] = rendered_config

    print(task.host.name)
    print(rendered_config)
    
def write_config(task, config):

    # Path of filename config will be written to
    filename = f"rendered_configs/{task.host.name}_{config}.txt"
    # What we're writing to the file - bgp/interfaces_config attribute from host object 
    content = task.host[f"{config}_config"]
    # Use write_file task plugin pass in content and filename
    task.run(task=write_file, content=content, filename=filename)



 
if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Execute custom task against nxos devices only
    nr = nr.filter(F(groups__contains='nxos'))
    print(nr.inventory.hosts)
    # Render BGP config
    bgp_results = nr.run(task=render_configs, template_name='bgp.j2')
    # Render interfaces config
    int_results = nr.run(task=render_configs, template_name='interfaces.j2')

    # Write BGP config to file
    bgp_config = nr.run(task=write_config, config='bgp')
    # Write intf config to file
    int_config = nr.run(task=write_config, config='interfaces')
    #pdbr.set_trace()