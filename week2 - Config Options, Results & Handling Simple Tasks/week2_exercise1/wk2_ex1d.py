"""
1d. Finally, modify the python script to set the number of workers to 15 using inline Python. Your inline Python should be similar to the following:
nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})
Re-run the script and confirm the number of workers is now 15.

From the above exercises, you should observe that the configuration order of preference was: inline python > config.yaml file > environment variable.

"""

from nornir import InitNornir
from rich import print

# Create norn object by initialising Nornir - config via inline python
norn = InitNornir(runner={"plugin": "threaded", "options": {"num_workers": 15}})

# Print no. of workers
no_of_workers = norn.runner.num_workers
print(f"The number of workers are: {no_of_workers}")
