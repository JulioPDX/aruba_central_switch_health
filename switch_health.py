#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from pycentral.base import ArubaCentralBase

# Creating dependencies for API calls, from Aruba team docs

central_info = {
    "base_url": "aruba_api_url",
    "token": {
        "access_token": "some_token"
    }
}

central = ArubaCentralBase(central_info=central_info, 
ssl_verify=True)

# Setting parameters for specific call
apiPath = "/platform/device_inventory/v1/devices"
apiMethod = "GET"
apiParams = {
    "limit": 30,
    "offset": 0,
    "sku_type": "MAS"
}

# Creating empty list, we will add to this list in a sec
switches = []

# Actual API call here
device_resp = central.command(apiMethod=apiMethod, apiPath=apiPath,
apiParams=apiParams)

# Appending to list we mentioned earlier
for device in device_resp['msg']['devices']:
    switches.append(device['serial'])

# Creating table, thanks to https://calmcode.io/rich/tables.html
device_table = Table(title="Aruba Switch Health")
device_table.add_column("Switch Type", justify="center", style="orange3")
device_table.add_column("Status", justify="center")
device_table.add_column("Model", justify="center", style="dodger_blue2")

# For loop for each switch in serials list
for serial in switches:
    apiPath = f"/monitoring/v1/switches/{serial}"
    apiMethod = "GET"
    apiParams = {
        "serial": f"{serial}"
    }
    # Saving each device response to device_resp variable
    # If statements are just checking a key and then adding rows to table
    device_resp = central.command(apiMethod=apiMethod, apiPath=apiPath,
    apiParams=apiParams)
    if 'status' in device_resp['msg'].keys():
        if device_resp['msg']['status'] != 'Up':
            device_table.add_row(
                f"{device_resp['msg']['switch_type']}", 
                f":thumbs_down: [red]{device_resp['msg']['status']}[/] :thumbs_down:", 
                f"{device_resp['msg']['model']}", style='green')
        elif device_resp['msg']['status'] == 'Up':
            device_table.add_row(
                device_resp['msg']['switch_type'], 
                device_resp['msg']['status'], 
                device_resp['msg']['model'], style='green')

console = Console()
console.print(device_table)