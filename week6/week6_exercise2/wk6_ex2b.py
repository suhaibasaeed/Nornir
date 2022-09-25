"""
2b. In Nornir inventory, comment out or otherwise remove the "data > loopbacks" section for "nxos2".
Re-execute your Nornir script--at this point, there should be a failure (i.e. certain Jinja2 variables are not known).

Modify your custom task such that the exception returned from Jinja2 "template_file" call is gracefully handled in the subtask 
(using NornirSubTaskError).
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirSubTaskError


# Custom task which renders template for nxos interfaces
def render_loopintf(task):
    
    try:
      # Run template_task plugin passing vars from host and template
      result = task.run(task=template_file, template='nxos_interfaces.j2', path='.',
      **task.host)
    # Catch exception from jinja2 rendering
    except NornirSubTaskError:
      print('Templating error occurred')
    
if __name__ == "__main__":

    # Initialise Nornir and filter on NXOS devices only
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    
    agg_result = nr.run(task=render_loopintf)
    
    print_result(agg_result)
