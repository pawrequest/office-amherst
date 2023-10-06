from pprint import pprint
from typing import Iterable

import win32com.client

from invoice.products import get_all_hire_products
from tmplt.entities import Connection, Connections, Fields, PRICES_WB, HireProduct


def fire_commence_agent(agent_trigger, category, command):
    conv = get_conversation()
    conv.Execute(f"[FireTrigger({agent_trigger}, {category}, {command})]")


def get_commence_data(table, name, fields: Iterable[str], connections: Iterable[Connection] = None):
    results = {}
    conv = get_conversation()
    record = get_record(conv, table, name)
    results[table] = get_data(record, fields)
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


def get_all_fields(conv_record, table):
    fields = conv_record.Request(f"[GetFieldNames({table}, ;)]")
    field_list = fields.split(';')
    return field_list


def get_all_field_values(conv_record, table, fields):
    get_all_fields(conv_record, table)
    values = conv_record.Request(f"[GetFieldValues({table}, {fields}, ;)]")
    return values


def get_data(conv, fields: Iterable[str]):
    data = {}
    for field in fields:
        try:
            data[field] = conv.Request(f"[ViewField(1, {field})]")
        except Exception as e:
            raise ValueError(f"Error getting {field}: {e}")
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
    get_table(conv, table)
    conv.Request(f"[ViewFilter(1, F,,Name, Equal to, {name},)]")
    item_count = conv.Request("[ViewItemCount]")
    if int(item_count) != 1:
        raise ValueError(f"{item_count} entries found for {table} : {name}")
    return conv


def get_table(conv, table):
    conv.Request(f"[ViewCategory({table})]")


def display_test_customer_agent():
    fire_commence_agent(agent_trigger='PYTHON_DDE', category='Customer', command='Test')


def stuff():
    hires_to = Connection(name="Has Hired", table='Hire', fields=Fields.HIRE.value)
    sales_to = Connection(name="Involves", table='Sale', fields=Fields.SALE.value)
    customer_data = get_commence_data(table="Customer", name="Test", fields=Fields.CUSTOMER.value,
                                      connections=[hires_to, sales_to])
    ahire = get_data_generic('Test - 16/08/2023 ref 31619', 'Hire')['Hire']
    return customer_data

def items_from_hire(hire_name):
    conv = get_conversation()
    record = get_record(conv, 'Hire', hire_name)
    fields = get_all_fields(conv, 'Hire')
    # field_values = get_all_field_values(record, 'Hire', fields)
    data = get_data(record, fields)
    order_items = {i[7:]: n for i, n in data.items() if i.startswith('Number ') and int(n) > 0}
    return order_items


def match_hire_products(hire_items, products):
    matched_products = {k: products[k] for k in hire_items if k in products}
    return matched_products



# hire_items = items_from_hire('Test - 16/08/2023 ref 31619')
# products = get_all_hire_products(PRICES_WB)
# matched_products = match_hire_products(hire_items, products)
# a_product = list(matched_products.values())[0]
# a_price = a_product.get_price(1, 1)

#
# hire_items = products_from_hire('Test - 16/08/2023 ref 31619')
# products = get_all_hire_products(PRICES_WB)

...




