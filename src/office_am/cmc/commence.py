from typing import ContextManager, List

from .cmc_funcs import clean_dict, clean_hire_dict, connected_records_to_qs, get_cmc, qs_from_name, \
    qs_to_dicts
from .auto_cmc import ICommenceDB, ICommenceEditRowSet
from .cmc_entities import Connection_e, CmcError


### functions to call

class CmcContext(ContextManager):
    def __init__(self, cmc: ICommenceDB = None):
        self.cmc = cmc or get_cmc()

    def __enter__(self):
        return CmcManager(self.cmc)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cmc = None



class CmcManager:
    def __init__(self, cmc_db):
        self.cmc_db = cmc_db


    def get_customer(self, record_name) -> dict:
        qs = qs_from_name(self.cmc_db, 'Customer', record_name)
        return clean_dict(qs_to_dicts(qs, 1)[0])


    def get_hire(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc_db, 'Hire', record_name)
        hire =  clean_hire_dict(qs_to_dicts(qs, 1)[0])
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
        connection = Connection_e.CUSTOMER_SALES
        qs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        dicts = qs_to_dicts(qs)
        dicts = [clean_dict(d) for d in dicts]
        return dicts


    def hires_by_customer(self, customer_name: str) -> List[dict]:
        connection = Connection_e.HIRES_CUSTOMER
        recs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        dicts = qs_to_dicts(recs)
        dicts = [clean_hire_dict(d) for d in dicts]
        return dicts

    def edit_hire(self, hire_name, package: dict):
        edit_set: ICommenceEditRowSet = qs_from_name(self.cmc_db, 'Hire', hire_name, edit=True)
        for key, value in package.items():
            try:
                col_idx = edit_set.GetColumnIndex(key, 0)
                edit_set.ModifyRow(0, col_idx, str(value), 0)
            except:
                raise CmcError(f"Could not modify {key} to {value}")
        edit_set.Commit(0)
        ...

# def lots_of_hires(num=20):
#     csr = get_csr('Customer')
#     csr = filter_by_fieldnew(csr, 'Hire Customer', 'yes')
#     csr = filter_by_fieldnew(csr, 'Date Last Contact', 'after', '1/1/2020')
#     # csr.SeekRow(0, 1000)
#     qs = csr.GetQueryRowSet(num, 0)
#     cust = qs_to_dicts(qs)
#     cust = [clean_hire_dict(d) for d in cust]
#     hire_dict = {}
#     wrong = []
#     for custom in cust:
#         if 'Has Hired Hire' not in custom.keys():
#             wrong.append(custom)
#             continue
#         if custom['Date Last Contact'] < datetime.date(2020, 1, 1):
#             wrong.append(custom)
#             continue
#         hired_str = custom['Has Hired Hire']
#         hired = hired_str.split(', ')
#         hires = [CmcManager.get_hire(h) for h in hired]
#         hire_dict[custom['Name']] = hires
#
#     return hire_dict


#
#
# def edit_hire(cmc_db, hire_name, package:dict):
#     edit_set:ICommenceEditRowSet = qs_from_name(cmc_db, 'Hire', hire_name, edit=True)
#     for key, value in package.items():
#         col_idx = edit_set.GetColumnIndex(key, 0)
#         try:
#             edit_set.ModifyRow(0, col_idx, str(value), 0)
#         except:
#             raise CmcError(f"Could not modify {key} to {value}")
#         edit_set.Commit(0)
#         ...
#
#
#
