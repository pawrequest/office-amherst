from in_out import commence
from managers.transact import TransactionContext


def test_get_customer(customer_name):
    customer_name = customer_name or 'Test'
    with TransactionContext() as tm:
        customer = commence.get_customer(customer_name)
        assert customer.Name == customer_name
        return customer


def test_get_hire(hire_name):
    hire_name = hire_name or 'you didnt fill in the test hire name'
    hire = commence.get_hire(hire_name)
    assert hire.Name == hire_name
    return hire


def test_get_sale(sale_name):
    sale_name = sale_name or 'you didnt put test sale name'
    sale = commence.get_sale(sale_name)
    assert sale.Name == sale_name




def test_customer_connections(customer_name):
    test_customer_trans(customer_name, 'Hire')
    test_customer_trans(customer_name, 'Sale')

def test_customer_trans(customer_name, category):
    if category == 'Hire':
        fun = commence.hires_by_customer
        check = commence.get_hire
    elif category == 'Sale':
        fun = commence.sales_by_customer
        check = commence.get_sale
    else:
        raise ValueError('Wrong category')


    transactions = fun(customer_name)
    for g in transactions:
        sngl = transactions.iloc[g]
        assert sngl.Name == check(sngl).Name
