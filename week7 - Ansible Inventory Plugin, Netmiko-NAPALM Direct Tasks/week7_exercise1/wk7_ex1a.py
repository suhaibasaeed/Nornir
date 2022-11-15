"""
1a. Create a Nornir script that uses this Ansible-style inventory.
In this script, print the username, password, port, and platform for one of the NX-OS hosts.
Note, the port will be "None" because it has not been set at the host or group inventory level.
Lastly, use the "get_connection_parameters" method to obtain and print the NAPALM port number (to ensure that it is 8443).
"""

from nornir import InitNornir

if __name__ == "__main__":
    # Initialise Nornir and filter to NXOS1 host only
    nr = InitNornir("config.yaml")
    nr = nr.filter(name="nxos1")

    # Print info
    print(nr.inventory.hosts["nxos1"].username)
    print(nr.inventory.hosts["nxos1"].password)
    print(nr.inventory.hosts["nxos1"].port)
    print(nr.inventory.hosts["nxos1"].platform)

    # Obtain and print NAPALM port no via get_connection_parameters method
    napalm_params = nr.inventory.hosts["nxos1"].get_connection_parameters("napalm")
    print(napalm_params.port)

