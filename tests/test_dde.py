from decimal import Decimal

import pytest

from invoice.products import get_all_hire_products, get_all_sale_products
from word.dde import get_commence_data, \
    get_hire_data_inv, get_sale_data_inv
from tmplt.entities import Connection, HirePrice, HireProduct, Price, SaleProduct
from tmplt.fields import INVOICE_FIELDS_CUST, INVOICE_FIELDS_HIRE, INVOICE_FIELDS_SALE

PRICES_WB = r'input_files/prices.xlsx'


def test_sales_products():
    products = get_all_sale_products(PRICES_WB)
    for name, p in products.items():
        assert isinstance(p, SaleProduct)
        assert isinstance(p.prices[0], Price)
        assert isinstance(p.get_price(1), Decimal)


def test_hire_products():
    products = get_all_hire_products(PRICES_WB)
    for name, p in products.items():
        assert isinstance(p, HireProduct)
        assert isinstance(p.prices[0], HirePrice)
        assert isinstance(p.get_price(1, 1), Decimal)


def test_customer_data():
    hires_to = Connection(name="Has Hired", table='Hire', fields=INVOICE_FIELDS_HIRE)
    sales_to = Connection(name="Involves", table='Sale', fields=INVOICE_FIELDS_SALE)
    customer_data = get_commence_data(table="Customer", name="Test", fields=INVOICE_FIELDS_CUST,
                                      connections=[hires_to, sales_to])
    assert all(field in customer_data['Customer'] for field in
               INVOICE_FIELDS_CUST), f"Missing fields in customer_data['Customer']"
    for hire_record in customer_data['Hire'].values():
        assert all(field in hire_record for field in
                   INVOICE_FIELDS_HIRE), f"Missing fields in a Hire record"

    for sale_record in customer_data['Sale'].values():
        assert all(field in sale_record for field in
                   INVOICE_FIELDS_SALE), f"Missing fields in a Sale record"

def test_wrong_customer_name():
    with pytest.raises(ValueError):
        customer_data = get_commence_data(table="Customer", name="FAKENAME", fields=INVOICE_FIELDS_CUST)

def test_get_hire():
    some_hire_name = 'Trampoline League - 27/06/2023 ref 31247'
    some_hire = get_hire_data_inv(some_hire_name)
    assert some_hire['Hire']['Name'] == some_hire_name

def test_get_sale():
    some_sale_name = 'Truckline Services - 26/10/2022 ref 11'
    some_sale = get_sale_data_inv(some_sale_name)
    assert some_sale['Sale']['Name'] == some_sale_name


def test_get_wrong_hire_name():
    with pytest.raises(ValueError):
        some_hire_name = 'FAKE HIRE NAME'
        some_hire = get_hire_data_inv(some_hire_name)