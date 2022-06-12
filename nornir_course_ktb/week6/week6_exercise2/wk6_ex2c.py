"""
2c. [Optional] - Further modify your custom task such that the multi_result execution reports "failed" as False.
In other words, exercise 2b gracefully caught the exception in the subtask,
but Nornir multi_result will still report the multi_result as failed:

ipdb> multi_result = agg_result["nxos2"]
ipdb> multi_result.failed
True
ipdb> multi_result[0].failed
False
ipdb> multi_result[1].failed
True

Nornir performs an "any" operation on the multi_result to determine "failed" so if any of the subtasks failed,
then the overall multi_result will still be reported as "failed".
So even though we gracefully caught the exception,
the exception/failure of the template rendering still happened and is still reflected in the multi_result:

ipdb> multi_result[1].exception                                                                                                                    
UndefinedError("'loopbacks' is undefined",)
ipdb> multi_result[1].failed                                                                                                                       
True
The above is from the Jinja2 templating task in the multi_result.

But you can remove "results" from inside the subtask using.

    except NornirSubTaskError:
        task.results.pop()

And then you can return your own custom Result object.       

        msg = "Encountered Jinja2 error"
        return Result(
            changed=False,
            diff=None,
            result=msg,
            host=task.host,
            failed=False,
            exception=None,
        ) 
The end result should be that back in your "main" program that there is "no failure".
In other words, this is potentially showing you how you could hide failures that you don't care about.

ipdb> p agg_result["nxos2"]                                                                                                                        
MultiResult: [Result: "render_configurations"]
ipdb> p agg_result["nxos2"].failed                                                                                                                 
False
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result


# Custom task which renders template for nxos interfaces
def render_loopintf(task):
    
    try:
      # Run template_task plugin passing vars from host and template
      result = task.run(task=template_file, template='nxos_interfaces.j2', path='.',
      **task.host)
    # Catch exception from jinja2 rendering
    except NornirSubTaskError:
      print('Subtask error')
      # Remove results from task object
      task.results.pop()
      # Return our own custom Results object
      msg = "Encountered Jinja2 error"
      return Result(
          changed=False,
          diff=None,
          result=msg,
          host=task.host,
          failed=False,
          exception=None,
      ) 
    
if __name__ == "__main__":

    # Initialise Nornir and filter on NXOS devices only
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    
    agg_result = nr.run(task=render_loopintf)
    
    print_result(agg_result)
