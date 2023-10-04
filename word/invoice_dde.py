from typing import Iterable

import win32com.client


def speak_to_commence(agent_trigger, category, command):
    cmc = win32com.client.Dispatch("Commence.DB")
    conv = cmc.GetConversation("Commence", "GetData")
    dde = f"[FireTrigger({agent_trigger}, {category}, {command})]"
    conv.Execute(dde)


def speak_to_commence2():
    cmc = win32com.client.Dispatch("Commence.DB")
    conv = cmc.GetConversation("Commence", "ViewData")
    dde = f"ViewCategory(Customer)"
    conv.Execute(dde)
    dde2 = r"ViewFilter(1, F,,Name, Equal to, Test,)"
    conv.Execute(dde2)

    ...


def do_commence(table, name, fields: Iterable[str]):
    conv = get_conversation()
    conv = get_record(conv, table, name)
    data = get_data(conv, fields)
    return data


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

def get_connected_data(conv, connection, fields: Iterable[str]):
    ...






fields_to_get = [
    "Telephone",
]
# Usage
customer_data = do_commence(table="Customer", name="Test", fields=fields_to_get)
# speak_to_commence2()
...


def display_test_customer():
    speak_to_commence(agent_trigger='PYTHON_DDE', category='Customer', command='Test')


display_test_customer()
