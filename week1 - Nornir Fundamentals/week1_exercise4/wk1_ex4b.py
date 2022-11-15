from nornir import InitNornir

"""
4a. Create a very simple custom task that prints a string for each host in inventory
(there should be two hosts in your inventory at this point).
You should use the .run() method to execute your custom task.

b. Adding to your custom task, print out the 'task.host.hostname' attribute (from inside the task).


"""

# Create norn object by initialising Nornir - automatically processess simpinventory files
norn = InitNornir()

# Define task in form of function - passing in task object
def a_task(task):
    dev_name = task.host.hostname
    print(f"Hey {dev_name}")

# Use run method to execute task against hosts and pass in task
norn.run(task=a_task)