Modify your Nornir "groups.yaml" file such that the NX-OS hosts will use SSH for NAPALM tasks instead of the NX-API.

Create a Nornir script with a custom task for "nxos1". This custom task should do the following:
Directly establish a NAPALM connection to nxos1 using nxos_ssh.
Prints this NAPALM connection object to standard output.
Retrieves an object for the underlying driver that NAPALM uses (this is accessed at napalm_conn.device). In this case, that underlying driver will be an SSH connection using Netmiko.
Prints the underlying driver object to standard output (i.e. the Netmiko connection object).
Print the output of the find_prompt() method on this underling Netmiko connection object.

The above will demonstrate how to get at the underlying connection that NAPALM uses (this could be PyEZ, eAPI, Netmiko, et cetera). In this case, the underlying connection object is a Netmiko connection object.

