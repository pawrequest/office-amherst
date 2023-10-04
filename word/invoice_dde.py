from dataclasses import dataclass
from typing import Iterable

import win32com.client


def fire_commence_agent(agent_trigger, category, command):
    conv = get_conversation()
    conv.Execute(f"[FireTrigger({agent_trigger}, {category}, {command})]")


@dataclass
class Connection:
    name: str
    table: str
    fields: Iterable[str]


def do_commence(table, name, fields: Iterable[str], connections: Iterable[Connection] = None):
    results = {}
    conv = get_conversation()
    conv = get_record(conv, table, name)
    results['data'] = get_data(conv, fields)
    if connections:
        results['connected_data'] = {}
        for connection in connections:
            connected_data = get_connected_data(conv, connection)
            results['connected_data'][connection.name] = connected_data
        ...
    return results


def get_connected_data(conv, connection: Connection):
    connected_name = conv.Request(f"[ViewConnectedItem(1, {connection.name}, {connection.table}, 1)]")
    connected_conv = get_record(conv, connection.table, connected_name)
    connected_data = get_data(connected_conv, connection.fields)
    return connected_data


def get_conversation():
    cmc = win32com.client.Dispatch("Commence.DB")
    conv = cmc.GetConversation("Commence", "GetData")
    return conv


def get_record(conv, table, name):
    conv.Request(f"[ViewCategory({table})]")
    conv.Request(f"[ViewFilter(1, F,,Name, Equal to, \"{name}\",)]")
    item_count = conv.Request("[ViewItemCount]")
    if int(item_count) != 1:
        raise ValueError(f"{item_count} entries found")
    return conv


def get_data(conv, fields: Iterable[str]):
    return {field: conv.Request(f"[ViewField(1, {field})]") for field in fields}



def test_do_cmc():
    fields_to_get_hire = ["Name"]
    fields_to_get_cust = [
        "Telephone",
    ]
    hires_to = Connection(name="Has Hired", table='Hire', fields=fields_to_get_hire)
    customer_data = do_commence(table="Customer", name="Test", fields=fields_to_get_cust, connections=[hires_to])
    ...

test_do_cmc()


def display_test_customer_agent():
    fire_commence_agent(agent_trigger='PYTHON_DDE', category='Customer', command='Test')


