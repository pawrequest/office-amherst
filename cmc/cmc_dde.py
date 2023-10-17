from typing import Dict, List



def get_fields(conv, table: str, item: str, fields: List[str] = None, delim=';') -> Dict[str, str]:
    if fields is None:
        fields = ['Name']
    fields_arg = ', '.join(fields)
    request_str = f"[GetFields({table}, {item}, {len(fields)}, {fields_arg}, {delim})]"
    response = conv.Request(request_str)
    field_values = response.split(delim)
    result = dict(zip(fields, field_values))
    return result


def get_connected_item_field(conv, from_category: str, from_item: str, connection: str, to_category: str, field: str,
                             delimiter=';') -> str:
    request_str = f"[GetConnectedItemField({from_category}, {from_item}, {connection}, {to_category}, {field}, {delimiter})]"
    response = conv.Request(request_str)
    return response


def get_connected_item_names(conv, from_category: str, from_item: str, connection: str, to_category: str) -> List[str]:
    request_str = f"[GetConnectedItemNames({from_category}, {from_item}, {connection}, {to_category})]"
    response = conv.Request(request_str)
    return response.split(';')


def get_field(conv, category: str, item: str, field: str) -> str:
    request_str = f"[GetField({category}, {item}, {field})]"
    response = conv.Request(request_str)
    return response


def get_field_to_file(conv, category: str, item: str, field: str, filename: str) -> None:
    request_str = f"[GetFieldToFile({category}, {item}, {field}, {filename})]"
    conv.Execute(request_str)


def get_image_field_names(conv, category: str, delim=';') -> List[str]:
    request_str = f"[GetImageFieldNames({category}, {delim})]"
    response = conv.Request(request_str)
    return response.split(delim)


def get_image_field_count(conv, category: str) -> int:
    request_str = f"[GetImageFieldCount({category})]"
    response = conv.Request(request_str)
    return int(response)


def get_image_field_to_file(conv, category: str, item: str, field: str, filename: str) -> None:
    request_str = f"[GetImageFieldToFile({category}, {item}, {field}, {filename})]"
    conv.Execute(request_str)


def get_item_names(conv, category: str) -> List[str]:
    request_str = f"[GetItemNames({category})]"
    response = conv.Request(request_str)
    return response.split('\n')  # Assuming the default delimiter is CR/LF


def get_phone_number(conv, phone_number: str) -> str:
    request_str = f"[GetPhoneNumber({phone_number})]"
    response = conv.Request(request_str)
    return response


def get_reverse_name(conv, name: str, pref_flag: str) -> str:
    request_str = f"[GetReverseName({name}, {pref_flag})]"
    response = conv.Request(request_str)
    return response


def view_connected_field(conv, index: int, connection_name: str, to_category: str, conn_index: int, field: str) -> str:
    request_str = f"[ViewConnectedField({index}, {connection_name}, {to_category}, {conn_index}, {field})]"
    response = conv.Request(request_str)
    return response


def view_connected_fields(conv, index: int, connection_name: str, to_category: str, conn_index: int,
                          fields: List[str]) -> Dict[str, str]:
    fields_arg = ', '.join(fields)
    request_str = f"[ViewConnectedFields({index}, {connection_name}, {to_category}, {conn_index}, {len(fields)}, {fields_arg})]"
    response = conv.Request(request_str)
    field_values = response.split(';')  # Assuming the delimiter is ';'
    result = dict(zip(fields, field_values))
    return result


def view_field(conv, index: int, field: str) -> str:
    request_str = f"[ViewField({index}, {field})]"
    response = conv.Request(request_str)
    return response


def view_fields(conv, index: int, fields: List[str]) -> Dict[str, str]:
    fields_arg = ', '.join(fields)
    request_str = f"[ViewFields({index}, {len(fields)}, {fields_arg})]"
    response = conv.Request(request_str)
    field_values = response.split(';')  # Assuming the delimiter is ';'
    result = dict(zip(fields, field_values))
    return result


def view_field_to_file(conv, index: int, field: str, filename: str) -> None:
    request_str = f"[ViewFieldToFile({index}, {field}, {filename})]"
    conv.Execute(request_str)


def view_image_field_to_file(conv, index: int, field: str, filename: str) -> None:
    request_str = f"[ViewImageFieldToFile({index}, {field}, {filename})]"
    conv.Execute(request_str)


def view_item_index(conv, name_field_value: str) -> str:
    request_str = f"[ViewItemIndex({name_field_value})]"
    response = conv.Request(request_str)
    return response


def view_item_name(conv, index: int) -> str:
    request_str = f"[ViewItemName({index})]"
    response = conv.Request(request_str)
    return response


def view_reverse_name(conv, name: str, pref_flag: str) -> str:
    request_str = f"[ViewReverseName({name}, {pref_flag})]"
    response = conv.Request(request_str)
    return response


###

def get_all_fieldnames(conv, table, delim=';'):
    fields = conv.Request(f"[GetFieldNames({table}, {delim})]")
    field_list = fields.split(';')
    return field_list

