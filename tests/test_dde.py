import pytest

from in_out.dde import get_commence_data, get_conversation_func, get_customer_sales, get_dde_data
from assets.entities import Connections, Fields


# @pytest.fixture
# def dde_context():
#     with DDEContext() as conv:
#         yield conv

# @pytest.fixture
# def dde_manager_fxt():
#     dde_man = DDEManager()
#     return dde_man


def test_is_running():
    running = get_conversation_func(topic='Commence', command='System')
    res = running.Request("Status")
    assert res == "Ready"


@pytest.fixture
def hire_name():
    return 'Trampoline League - 27/06/2023 ref 31247'


@pytest.fixture
def sale_name():
    return 'Truckline Services - 26/10/2022 ref 11'


@pytest.fixture
def customer_name():
    return 'Test'


#
# def test_manager1(dde_manager_fxt, hire_name):
#     # dde_man = dde_manager_fxt
#     dde_man = dde_man = DDEManager()
#
#     # some_Striong = '23424'
#     # some_hire = dde_man.get_cmc_data('Hire', hire_name, Fields.HIRE.value)
#     some_hire = dde_man.cmc_to_df('Hire', hire_name, Fields.HIRE.value)
#     # dde_man.conv = None
#     ...

def test_get_conv():
    conv = get_conversation_func()
    assert conv is not None


def test_customer_data(customer_name):
    hires_to = Connections.CUSTOMER_HIRES.value
    sales_to = Connections.CUSTOMER_SALES.value
    customer_data = get_commence_data(table="Customer", name=customer_name, fields=Fields.CUSTOMER.value,
                                      connections=[hires_to, sales_to])
    assert all(field in customer_data['Customer'] for field in Fields.CUSTOMER.value)
    for hire_record in customer_data['Hire'].values():
        assert all(field in hire_record for field in Fields.HIRE.value)

    for sale_record in customer_data['Sale'].values():
        assert all(field in sale_record for field in Fields.SALE.value)


#
#
def test_wrong_customer_name():
    with pytest.raises(ValueError):
        customer_data = get_commence_data(table="Customer", name="FAKENAME", fields=Fields.CUSTOMER.value)


def test_get_hire():
    some_hire_name = 'Trampoline League - 27/06/2023 ref 31247'
    some_hire = get_dde_data(some_hire_name, 'Hire')
    assert some_hire['Hire']['Name'] == some_hire_name


def test_get_sale(sale_name):
    some_sale = get_dde_data(sale_name, 'Sale')
    assert some_sale['Sale']['Name'] == sale_name


def test_get_generic(hire_name, sale_name):
    some_hire = get_dde_data(hire_name, 'Hire')
    assert some_hire['Hire']['Name'] == hire_name
    some_sale = get_dde_data(sale_name, 'Sale')
    assert some_sale['Sale']['Name'] == sale_name


def test_get_wrong_hire_name():
    with pytest.raises(ValueError):
        some_hire_name = 'FAKE HIRE NAME'
        some_hire = get_dde_data(some_hire_name, 'Hire')


def test_get_customer_sales(customer_name):
    conv = get_conversation_func()
    sales = get_customer_sales(conv=conv, customer_name=customer_name)
    assert sales

#
# def test_fields_df(hire_name):
#     conv = get_conversation_func()
#     record = get_record(conv, 'Hire', 'Trampoline League - 27/06/2023 ref 31247')
#     df = record_to_df(record_conv=record, table='Hire', name=hire_name)
# #     # assert isinstance(f_df, pd.DataFrame)
# #     # some_str = '23424'
# #     # pass
# #     ...
#
