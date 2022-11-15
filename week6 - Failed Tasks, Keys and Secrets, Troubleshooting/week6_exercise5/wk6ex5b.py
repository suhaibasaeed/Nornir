"""
5c. Repeat exercise 5b except store the "recover" password in an ansible-vault YAML file.
Decrypt this file dynamically and assign the recover password using this vaulted password.
See the Ansible Vault decryption code that is included near the top of this lesson.

You can create a YAML file with the proper password and encrypt it using Ansible Vault: "ansible-vault encrypt MY_FILE".
"""

from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirSubTaskError
from netmiko.ssh_exception import NetmikoAuthenticationException
import os
import random

BAD_PASSWORD = "dDFDFGRFGS" 

import yaml
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader
from nornir import InitNornir
from nornir.plugins.tasks import networking

def decrypt_vault(
    filename, vault_password=None, vault_password_file=None, vault_prompt=False
):
    """
    filename: name of your encrypted file that needs decrypted.
    vault_password: key that will decrypt the vault.
    vault_password_file: file containing key that will decrypt the vault.
    vault_prompt: Force vault to prompt for a password if everything else fails.
    """

    loader = DataLoader()
    if vault_password:
        vault_secret = [([], VaultSecret(vault_password.encode()))]
    elif vault_password_file:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[vault_password_file]
        )   
    else:
        vault_secret = CLI.setup_vault_secrets(
            loader=loader, vault_ids=[], auto_prompt=vault_prompt
        )   

    vault = VaultLib(vault_secret)

    with open(filename) as f:
        unencrypted_yaml = vault.decrypt(f.read())
        unencrypted_yaml = yaml.safe_load(unencrypted_yaml)
        return unencrypted_yaml


# Task which sends command to device
def send_cmd(task):
    # Choose specific command based on group
    if str(task.host.groups[0]) == 'junos':
        cmd = 'show system uptime'
    else:
        cmd = 'show clock'
    
    try:

        result = task.run(task=netmiko_send_command, command_string=cmd)
    # If the password is wrong
    except (NornirSubTaskError, NetmikoAuthenticationException):
        print(f"{task.host.name} has incorrect password")
        # Remove failed SSH attempt from results so we get 2nd attempt result
        task.results.pop()
        # Set correct password from ansible vault file
        task.host.password = decrypt_vault(vault_password="Pa55word")
        # Re-run task
        result = task.run(task=netmiko_send_command, command_string=cmd)
        
        



if __name__ == "__main__":

    nr = InitNornir("config.yaml")
    # Loop through inventory and randomly give hosts wrong password
    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = BAD_PASSWORD
    
    results = nr.run(task=send_cmd)
    
    print_result(results)