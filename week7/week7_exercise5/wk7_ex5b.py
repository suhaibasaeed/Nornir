"""
 5b. Modify your solution to write the checkpoint files out to the file system. The files should be written to:

backups/nxos1_checkpoint
backups/nxos2_checkpoint

Your script should automatically create the "backups" directory if it doesn't already exist.
"""

import pathlib
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from pathlib import Path
from nornir_utils.plugins.tasks.files import write_file

def get_checkpoint(task):

    # Manually create NAPALM connection
    napalm = task.host.get_connection("napalm", task.nornir.config)
    # Get checkpoint file and store in host object
    task.host["backup"] = napalm._get_checkpoint_file()

def write_checkpoint(task):
    
    filename = f"{task.host.name}_checkpoint"

    # Create backup directory
    pathlib.Path("backup").mkdir(exist_ok=True)
    # Write checkpoint from host obj to file
    task.run(task=write_file, filename=f"backup/{filename}", content=task.host["backup"])

if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")
    nr = nr.filter(F(groups__contains='nxos'))
    checkp_results = nr.run(task=get_checkpoint)
    write_results = nr.run(task=write_checkpoint)