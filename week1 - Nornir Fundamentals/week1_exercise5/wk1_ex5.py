from nornir import InitNornir

"""
5. Expand on your inventory files to include DNS servers.
Add a dns1 and a dns2 server to your defaults.yaml file (this should be under the "data" key).
These two DNS servers have IP addresses of 1.1.1.1 and 1.0.0.1, respectively.
Since these DNS servers are in your defaults.yaml file, you can think of them as the global DNS server that you would use unless you overwrite them at the host or group level.
Now for your first host in inventory (in hosts.yaml) add a more specific dns1 server under the "data" key.
This DNS server should have an IP address of 8.8.8.8.

Now expand on your custom task from exercise4 and print out the two DNS servers for each host object.
The first host object should have dns1=8.8.8.8 and dns2=1.0.0.1 (the first entry from hosts.yaml and the second entry from defaults.yaml).
The second host object should have dns1=1.1.1.1 and dns2=1.0.0.1 (where both entries are pulled from defaults.yaml).

"""

# Create norn object by initialising Nornir - automatically processess simpinventory files
norn = InitNornir()

# Define task in form of function - passing in task object
def a_task(task):
    # Get hostname from task object
    dev_name = task.host.hostname
    # Get DNS servers from defaults.yml data and hosts.yml data - we have to specify key as cisco3 overrides dns1 at host level
    dns_servers = [
        norn.inventory.hosts[str(task.host)]["dns1"],
        norn.inventory.hosts[str(task.host)]["dns2"],
    ]
    print(f"Hey {dev_name} your DNS servers are {dns_servers}")


# Use run method to execute task against hosts and pass in task
norn.run(task=a_task)
