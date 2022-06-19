"""
1b. Write a simple task to run the "ntp_servers" getter against the NX-OS devices
(this will confirm NAPALM and NX-API is working properly).
Use the "print_result" function to print out your results.
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

if __name__ == "__main__":
    
    # Initialise Nornir
    nr = InitNornir("config.yaml")
    # Run NTP NAPALM getter against devices and print results
    results = nr.run(name="GET NTP SERVERS", task=napalm_get, getters=["ntp_servers"])

    print_result(results)

