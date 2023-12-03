from commence_py import CmcCursor, CmcDB
from commence_py.cmc_entities import Connection

from office_am.commence.cmc_funcs import clean_dict


class CONNECTIONS:
    CUSTOMER_HIRES = Connection(from_table='Customer', desc='Has Hired', to_table='Hire')
    CUSTOMER_SALES = Connection(from_table='Customer', desc='Involves', to_table='Sale')
    HIRES_CUSTOMER = Connection(from_table='Hire', desc='To', to_table='Customer')
    SALES_CUSTOMER = Connection(from_table='Sale', desc='To', to_table='Customer')


class AmherstCommence:
    def __init__(self):
        self.cmc_db = CmcDB()

    def get_customer(self, record_name) -> dict:
        cursor:CmcCursor = self.cmc_db.get_cursor('Customer')

        cursor.get_record(record_name)

        cursor.filter_by_name(record_name)
        qs = cursor.get_query_row_set(1)
        customer = qs.get_rows_dict()
        return clean_dict(customer)

    def get_hire(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc_db, 'Hire', record_name)
        hire = clean_hire_dict(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', hire['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        hire['customer'] = customer
        return hire

    def get_sale(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc_db, 'Sale', record_name)
        sale = clean_dict(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', sale['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        sale['customer'] = customer
        return sale

    def get_record_with_customer(self, table, record_name: str) -> dict:
        cleaner = clean_hire_dict if table == 'Hire' else clean_dict
        qs = qs_from_name(self.cmc_db, table, record_name)
        trans = cleaner(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', trans['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        trans['customer'] = customer
        return trans

    def sales_by_customer(self, customer_name: str, cmc=None) -> List[dict]:
        connection = CONNECTION.CUSTOMER_SALES
        qs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        sales = qs_to_dicts(qs)
        for sale in sales:
            sale['customer'] = self.get_customer(sale['To Customer'])

        sales = [clean_dict(d) for d in sales]
        return sales

    def hires_by_customer(self, customer_name: str) -> List[dict]:
        connection = CONNECTION.HIRES_CUSTOMER
        recs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        hires = qs_to_dicts(recs)
        for hire in hires:
            hire['customer'] = self.get_customer(hire['To Customer'])
        hires = [clean_hire_dict(d) for d in hires]
        return hires



