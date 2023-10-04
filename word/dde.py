from dataclasses import dataclass
from typing import Iterable

import win32com.client

INVOICE_FIELDS_HIRE = [
    "Delivery Contact",
    "Delivery Name",
    "Delivery Address",
    "Delivery Postcode",
    "Number UHF",
    "Booked Date",

]
INVOICE_FIELDS_CUST = [
    "Contact Name",
    "Name",
    "Address",
    "Postcode",
]

INVOICE_FIELDS_SALE = [
    "Invoice Address",
]


def fire_commence_agent(agent_trigger, category, command):
    conv = get_conversation()
    conv.Execute(f"[FireTrigger({agent_trigger}, {category}, {command})]")


@dataclass
class Connection:
    name: str
    table: str
    fields: Iterable[str]


def commence_data(table, name, fields: Iterable[str], connections: Iterable[Connection] = None):
    results = {}
    conv = get_conversation()
    conv = get_record(conv, table, name)
    results[table] = get_data(conv, fields)
    if not connections:
        return results
    for connection in connections:
        connected_data = get_all_connected(conv, table, name, connection)
        results[connection.table] = connected_data
    return results


def get_sale_data_inv(sale_name):
    sales_to = Connection(name="To", table='Customer', fields=INVOICE_FIELDS_CUST)
    return commence_data(table="Sale", name=sale_name, fields=INVOICE_FIELDS_SALE, connections=[sales_to])


def get_hire_data_inv(hire_name):
    hires_to = Connection(name="To", table='Customer', fields=INVOICE_FIELDS_HIRE)
    return commence_data(table="Hire", name=hire_name, fields=INVOICE_FIELDS_HIRE, connections=[hires_to])


def get_connected_data_limited(conv, connection: Connection, limit=1):
    connected_name = conv.Request(f"[ViewConnectedItem(1, {connection.name}, {connection.table}, {limit},)]")
    connected_conv = get_record(conv, connection.table, connected_name)
    connected_data = get_data(connected_conv, connection.fields)
    return connected_data


def get_all_connected(conv, from_table, from_item, connection:Connection):
    connected_names = conv.Request(f"[GetConnectedItemNames({from_table}, {from_item}, {connection.name}, {connection.table}, ;)]")
    cons = connected_names.split(';')
    results = {}
    for c_name in cons:
        connected_conv = get_record(conv, connection.table, c_name)
        connected_data = get_data(connected_conv, connection.fields)
        # results.append(connected_data)
        results[c_name] = connected_data
    return results

def get_customer_sales(conv, customer_name):
    return get_all_connected(conv, 'Customer', customer_name, Connection(name='Involves', table='Sale', fields=INVOICE_FIELDS_SALE))


def get_conversation():
    cmc = win32com.client.Dispatch("Commence.DB")
    conv = cmc.GetConversation("Commence", "GetData")
    return conv


def get_record(conv, table, name):
    conv.Request(f"[ViewCategory({table})]")
    conv.Request(f"[ViewFilter(1, F,,Name, Equal to, {name},)]")
    item_count = conv.Request("[ViewItemCount]")
    if int(item_count) != 1:
        raise ValueError(f"{item_count} entries found")
    return conv


def get_data(conv, fields: Iterable[str]):
    return {field: conv.Request(f"[ViewField(1, {field})]") for field in fields}


def do_cmc():
    hires_to = Connection(name="Has Hired", table='Hire', fields=INVOICE_FIELDS_HIRE)
    sales_to = Connection(name="Involves", table='Sale', fields=INVOICE_FIELDS_SALE)
    customer_data = commence_data(table="Customer", name="Test", fields=INVOICE_FIELDS_CUST, connections=[hires_to, sales_to])
    some_sale_name = 'Woodlands Primary School - 03/10/2023 ref 361'
    some_data = get_sale_data_inv(some_sale_name)
    ...
    ...


def display_test_customer_agent():
    fire_commence_agent(agent_trigger='PYTHON_DDE', category='Customer', command='Test')


do_cmc()
