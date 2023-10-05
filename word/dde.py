from typing import Iterable

import win32com.client

from tmplt.entities import Connection, Connections, Fields


def fire_commence_agent(agent_trigger, category, command):
    conv = get_conversation()
    conv.Execute(f"[FireTrigger({agent_trigger}, {category}, {command})]")


def get_commence_data(table, name, fields: Iterable[str], connections: Iterable[Connection] = None):
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




def get_data_generic(record_name, table_name):
    table_name_enum = Fields[table_name.upper()]
    connection_to = Connections.TO_CUSTOMER.value
    try:
        data = get_commence_data(table=table_name, name=record_name, fields=table_name_enum.value,
                                 connections=[connection_to])
    except Exception as e:
        raise ValueError(f"Error getting {table_name} data for {record_name}:\n{e}")
    else:
        return data




def get_connected_data_limited(conv, connection: Connection, limit=1):
    connected_name = conv.Request(f"[ViewConnectedItem(1, {connection.name}, {connection.table}, {limit},)]")
    connected_conv = get_record(conv, connection.table, connected_name)
    connected_data = get_data(connected_conv, connection.fields)
    return connected_data


def get_all_connected(conv, from_table, from_item, connection: Connection):
    connected_names = conv.Request(
        f"[GetConnectedItemNames({from_table}, {from_item}, {connection.name}, {connection.table}, ;)]")
    if not connected_names or connected_names == '(none)':
        raise ValueError(
            f'{from_table}:  {from_item} has no connected items  "{connection.name}" in {connection.table}')
    cons = connected_names.split(';')
    results = {}
    for c_name in cons:
        connected_conv = get_record(conv, connection.table, c_name)
        connected_data = get_data(connected_conv, connection.fields)
        # results.append(connected_data)
        results[c_name] = connected_data
    return results


def get_customer_sales(conv, customer_name):
    return get_all_connected(conv, 'Customer', customer_name,
                             Connection(name='Involves', table='Sale', fields=Fields.SALE.value))


def get_conversation():
    cmc = win32com.client.Dispatch("Commence.DB")
    conv = cmc.GetConversation("Commence", "GetData")
    return conv


def get_record(conv, table, name):
    conv.Request(f"[ViewCategory({table})]")
    conv.Request(f"[ViewFilter(1, F,,Name, Equal to, {name},)]")
    item_count = conv.Request("[ViewItemCount]")
    if int(item_count) != 1:
        raise ValueError(f"{item_count} entries found for {table} : {name}")
    return conv


def get_data(conv, fields: Iterable[str]):
    try:
        data = {field: conv.Request(f"[ViewField(1, {field})]") for field in fields}
    except Exception as e:
        raise ValueError(f"Error getting data: {e}")
    else:
        return data


def display_test_customer_agent():
    fire_commence_agent(agent_trigger='PYTHON_DDE', category='Customer', command='Test')


def stuff():
    hires_to = Connection(name="Has Hired", table='Hire', fields=Fields.HIRE.value)
    sales_to = Connection(name="Involves", table='Sale', fields=Fields.SALE.value)
    customer_data = get_commence_data(table="Customer", name="Test", fields=Fields.CUSTOMER.value,
                                      connections=[hires_to, sales_to])
    ...

# stuff()


# deprecated
# def get_sale_data_inv(sale_name):
#     sales_to = Connections.TO_CUSTOMER.value
#     return get_commence_data(table="Sale", name=sale_name, fields=Fields.SALE.value, connections=[sales_to])
#
#
# def get_hire_data_inv(hire_name):
#     hires_to = Connections.TO_CUSTOMER.value
#     try:
#         data = get_commence_data(table="Hire", name=hire_name, fields=Fields.HIRE.value, connections=[hires_to])
#     except Exception as e:
#         raise ValueError(f"Error getting hire data: for {hire_name}:\n{e}")
#     else:
#         return data
#
