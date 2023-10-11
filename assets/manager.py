import json
import os
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

import pandas as pd
from pandas import Series

from assets.entities import DFLT
from in_out.excel import df_overwrite_wb
from transactions.tran_manager import TransactionManager


# from word.dde import items_from_hire


def an_id(id_or_serial):
    return len(str(id_or_serial)) == 4


def get_id_and_serial(id_or_serial, df):
    try:
        if an_id(id_or_serial):
            id_num = id_or_serial
            serial = df[df[DFLT.ID.value] == id_num][DFLT.SERIAL.value].values[0]
        else:
            id_num = df[df[DFLT.SERIAL.value] == id_or_serial][DFLT.ID.value].values[0]
            serial = id_or_serial
    except Exception as e:
        raise e
    # except ValueError:
    #     print(f"Error: {id_or_serial} not found in {DFLT.WB.value}")
    # except KeyError:
    #     print(f"Error: {DFLT.ID.value} or {DFLT.SERIAL.value} not found in {DFLT.WB.value}")

    else:
        return id_num, serial


def handle_row(row):
    if row.empty:
        raise ValueError(f"Asset not found")
    if row.shape[0] > 1:
        raise ValueError(f"More than one asset found")
    return row.iloc[0]


@dataclass
class Asset:
    id_number: str = field
    serial_number: str = field
    fw_version: Optional[str] = None
    model: Optional[str] = None

    def __eq__(self, other):
        return self.id_number == other.id_number and self.serial_number == other.serial_number


def decimal_from_value(value):
    return Decimal(value)


class ManagerContext:
    def __init__(self, workbook_ast=None, sheet=None, header_row=None, out_file=None, workbook_prcs=None,
                 df_pr_hire=None, df_pr_sale=None):
        self.workbook_ast = workbook_ast or DFLT.WB_AST.value
        self.workbook_prcs = workbook_prcs or DFLT.WB_PRC.value
        self.out_file = out_file or DFLT.OUT_AST.value
        self.json_file = self.out_file.with_suffix('.json')  # JSON file path with new suffix
        self.sheet = sheet or DFLT.SHEET.value
        self.header_row = header_row or int(DFLT.HEAD.value)
        self.get_dfs()
        if out_file and not out_file.exists():
            self.df_a.to_excel(out_file, index=False)

    def __enter__(self):
        self.asset_manager = AssetManager(self.df_a)
        self.transaction_manager = TransactionManager(self.df_pr_hire, self.df_pr_sale)
        return (self.asset_manager, self.transaction_manager)

    def get_dfs(self):
        assert self.workbook_ast.exists()
        assert self.workbook_prcs.exists()
        if os.path.exists(self.json_file):  # Check if JSON file exists
            self.dfs_from_json()
        else:
            self.dfs_from_excel()

    def dfs_from_excel(self):
        self.df_a = pd.read_excel(self.workbook_ast, sheet_name=self.sheet, header=self.header_row, dtype=str)
        self.df_pr_hire = pd.read_excel(self.workbook_prcs, sheet_name='Hire', header=0,
                                        converters={'Price': decimal_from_value})
        self.df_pr_sale = pd.read_excel(self.workbook_prcs, sheet_name='Sale', header=0,
                                        converters={'Price': decimal_from_value})


    def dfs_from_json(self):
        with open(self.json_file, 'r') as json_file:
            data = json.load(json_file)
            [setattr(self, dfname, pd.read_json(df)) for dfname, df in data.items()]
        self.df_pr_hire['Price'] = self.df_pr_hire['Price'].apply(decimal_from_value)
        self.df_pr_sale['Price'] = self.df_pr_sale['Price'].apply(decimal_from_value)
        self.df_a['Number'] = self.df_a['Number'].astype(str)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_dfs_to_json()
        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        df_overwrite_wb(input_workbook=self.workbook_ast, sheet=self.sheet, header_row=self.header_row,
                        out_file=self.out_file, df=self.df_a)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Hire', header_row=0,
                        out_file=DFLT.WB_PRC.value, df=self.df_pr_hire)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Sale', header_row=0,
                        out_file=DFLT.OUT_PRC.value, df=self.df_pr_sale)

    def save_dfs_to_json(self):
        data = {
            'df_a': self.df_a.to_json(),
            'df_pr_hire': self.df_pr_hire.to_json(),
            'df_pr_sale': self.df_pr_sale.to_json()
        }
        ...
        with open(self.json_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)


class AssetManager:

    def __init__(self, df_a):
        self.df_a = df_a


    def row_from_id_or_serial(self, id_or_serial: str) -> Series:
        if an_id(id_or_serial):
            row = self.df_a.loc[self.df_a[DFLT.ID.value] == id_or_serial]
        else:
            row = self.df_a.loc[self.df_a[DFLT.SERIAL.value] == id_or_serial]
        assert row.shape[0] == 1
        return handle_row(row)

    def set_field_by_id_or_serial(self, id_or_serial: str, field: str, value):
        if an_id(id_or_serial):
            self.df_a.loc[self.df_a[DFLT.ID.value] == id_or_serial, field] = value
        else:
            self.df_a.loc[self.df_a[DFLT.SERIAL.value] == id_or_serial, field] = value


    def field_from_id_or_serial(self, id_or_serial: str, field: str):
        try:
            if an_id(id_or_serial):
                return self.df_a.loc[self.df_a[DFLT.ID.value] == id_or_serial, field].values[0]
            else:
                return self.df_a.loc[self.df_a[DFLT.SERIAL.value] == id_or_serial, field].values[0]
        except IndexError:
            raise ValueError(f"Field {field} not found for {id_or_serial}")
        except Exception as e:
            raise e

    def check_fw(self, id_or_serial: str, fw_version=None):
        fw_1 = self.field_from_id_or_serial(id_or_serial=id_or_serial, field=DFLT.FW.value)
        if fw_version is None:
            assert fw_1
        else:
            assert fw_1 == fw_version
        ...