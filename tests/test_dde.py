from decimal import Decimal

import pytest

from invoice.products import HirePrice, HireProduct, Price, SaleProduct, get_all_hire_products, get_all_sale_products
from word.dde import Connection, INVOICE_FIELDS_CUST, INVOICE_FIELDS_HIRE, INVOICE_FIELDS_SALE, get_commence_data

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
