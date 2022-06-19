"""
3. Create a Nornir script that contains a custom task.
This custom task should directly create a Netmiko connection and retrieve the router/switch prompt for each device in inventory (use Netmiko's find_prompt method).
For the Cisco IOS devices use SSH keys for authentication.

For SSH keys, you should have the following files available in the lab environment:
-rw-------  1 user group 3243 Sep 19 09:27 student_key
-rw-r--r--  1 user group  739 Sep 19 09:27 student_key.pub

These files are located in the "~/.ssh/" directory (in other words, your home directory, then .ssh--note, the leading period).

You will need to use a username of "student1" with this SSH key.

"""

from nornir import InitNornir

def direct_netmiko(task):
    # Manually create Netmiko connection if not already there - pass in nornir config obj
    net_conn = task.host.get_connection("netmiko", task.nornir.config)

    # Invoke find prompt Netmiko method against object to print prompt
    print("-" * 80)
    print(net_conn.find_prompt())
    print("-" * 80)


if __name__ == "__main__":
    
    # Initialise Nornir and filter on NXOS group
    nr = InitNornir("config.yaml")

    results = nr.run(task=direct_netmiko)