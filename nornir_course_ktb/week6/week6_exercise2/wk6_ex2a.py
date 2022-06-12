"""
2a. Create a Jinja2 template that generates loopback interfaces for NX-OS devices.

This template should use a data structure defined in inventory similar to the following:

    data:
      loopbacks:
        - id: 123
          description: ntp source
          ip: 1.2.3.1
          mask: 255.255.255.255
Note, the value "loopbacks" is a list that contains an inner dictionary (with fields of "id", "description", "ip", "mask").

Copy the default hosts.yaml file to current dir and add "loopbacks" key inside data for each of the NX-OS hosts

In your Nornir script, filter your inventory to just the "nxos" hosts.
Create a custom task that uses the inventory data and the Jinja2 template to render the configuration.
Use the print_result function to ensure that your template renders correctly for each NX-OS device.
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

# Custom task which renders template for nxos interfaces
def render_loopintf(task):
    
    # Run template_task plugin passing vars from host and template
    result = task.run(task=template_file, template='nxos_interfaces.j2', path='.',
    **task.host)
    

if __name__ == "__main__":

    # Initialise Nornir and filter on NXOS devices only
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    
    agg_result = nr.run(task=render_loopintf)
    
    print_result(agg_result)
