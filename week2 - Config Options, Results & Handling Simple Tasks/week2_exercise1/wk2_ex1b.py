"""
1b. Create a Nornir config.yaml file that sets the number of workers to 5
Modify the Python script from exercise 1a to load this config.yaml file.
Print out and verify the new number of workers.

1c. Use:

export NORNIR_RUNNER_OPTIONS='{"num_workers": 100}'
in the bash shell to modify the number of workers using an environment variable.
Keep your Python script exactly the same as exercise1a
(in other words, you should NOT have any 'runner' section in your config.yaml).
Re-run your script to validate the environment variable setting is now being used.
"""

from nornir import InitNornir
from rich import print

# Create norn object by initialising Nornir - pass in config file
norn = InitNornir("config.yaml")

# Print no. of workers
no_of_workers = norn.runner.num_workers
print(f"The number of workers are: {no_of_workers}")
