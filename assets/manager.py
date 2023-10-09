from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import Series

from in_out.excel import df_overwrite_wb
from word.dde import items_from_hire


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


@dataclass
class Asset:
    id_number: str = field
    serial_number: str = field
    fw_version: Optional[str] = None
    model: Optional[str] = None

    def __eq__(self, other):
        return self.id_number == other.id_number and self.serial_number == other.serial_number


class DFLT(Enum):
    MIN_DUR = 'Min Duration'
    MODEL = "Model"
    SERIAL = 'Barcode'
    ID = 'Number'
    FW = 'FW'
    FW_VERSION = 'XXXX'
    WB_AST = Path(__file__).resolve().with_name("assets_in.xlsx")
    OUT_AST = Path(__file__).resolve().with_name("assets_out.xlsx")
    SHEET = 'Sheet1'
    HEAD = 2
    WB_PRC = Path(__file__).resolve().with_name("prices.xlsx")
    OUT_PRC = Path(__file__).resolve().with_name("prices.xlsx")
    MIN_QTY = 'Min Qty'
    PRICE = 'Price'


def decimal_from_value(value):
    return Decimal(value)


class AssetManagerContext:
    def __init__(self, workbook_ast=None, sheet=None, header_row=None, out_file=None, workbook_prcs=None,
                 df_pr_hire=None, df_pr_sale=None):
        self.workbook_ast = workbook_ast or DFLT.WB_AST.value
        self.out_file = out_file or DFLT.OUT_AST.value
        self.sheet = sheet or DFLT.SHEET.value
        self.workbook_prcs = workbook_prcs or DFLT.WB_PRC.value
        self.header_row = header_row or int(DFLT.HEAD.value)
        self.get_dfs()
        if out_file and not out_file.exists():
            self.df_a.to_excel(out_file, index=False)

    def __enter__(self):
        self.asset_manager = AssetManager(self.df_a, self.df_pr_hire, self.df_pr_sale)
        return self.asset_manager

    def get_dfs(self):
        self.df_a = pd.read_excel(self.workbook_ast, sheet_name=self.sheet, header=self.header_row, dtype=str)
        self.df_pr_hire = pd.read_excel(self.workbook_prcs, sheet_name='Hire', header=0,
                                        converters={'Price': decimal_from_value})
        self.df_pr_sale = pd.read_excel(self.workbook_prcs, sheet_name='Sale', header=0,
                                        converters={'Price': decimal_from_value})
        return self.df_a, self.df_pr_hire, self.df_pr_sale

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        df_overwrite_wb(input_workbook=self.workbook_ast, sheet=self.sheet, header_row=self.header_row,
                        out_file=self.out_file, df=self.asset_manager.df_a)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Hire', header_row=0,
                        out_file=DFLT.WB_PRC.value, df=self.asset_manager.df_pr_hire)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Sale', header_row=0,
                        out_file=DFLT.OUT_PRC.value, df=self.asset_manager.df_pr_sale)


@dataclass
class HireLineItem:
    name: str
    quantity: int
    duration: int
    price_each: Decimal
    @property
    def price_total(self):
        return self.quantity * self.price_each


def handle_row(row):
    if row.empty:
        raise ValueError(f"Asset not found")
    if row.shape[0] > 1:
        raise ValueError(f"More than one asset found")
    return row.iloc[0]


class AssetManager:

    def __init__(self, df_a, df_pr_hire, df_pr_sale):
        self.df_a = df_a
        self.df_pr_hire = df_pr_hire
        self.df_pr_sale = df_pr_sale

    # def row_from_product_name(self, category, product_name: str) -> Series:
    #     if category == 'Hire':
    #         row = self.df_pr_hire.loc[self.df_pr_hire['Name'] == product_name]
    #     elif category == 'Sale':
    #         row = self.df_pr_sale.loc[self.df_pr_sale['Name'] == product_name]
    #     else:
    #         raise ValueError(f"Category {category} not found")
    #     return handle_row(row)

    def row_from_serial_or_id(self, id_or_serial: str) -> Series:
        if an_id(id_or_serial):
            row = self.df_a.loc[self.df_a[DFLT.ID.value] == id_or_serial]
        else:
            row = self.df_a.loc[self.df_a[DFLT.SERIAL.value] == id_or_serial]
        return handle_row(row)

    def set_field(self, id_or_serial: str, field: str, value):
        if an_id(id_or_serial):
            self.df_a.loc[self.df_a[DFLT.ID.value] == id_or_serial, field] = value
        else:
            self.df_a.loc[self.df_a[DFLT.SERIAL.value] == id_or_serial, field] = value

    def get_sale_price(self, product_name: str, quantity: int):
        mp = mp = self.df_pr_sale.loc[self.df_pr_sale['Name'] == product_name]
        mp_prc = mp.loc[mp[DFLT.MIN_QTY.value] <= quantity, 'Price'].values
        try:
            return mp_prc[0]
        except IndexError:
            raise ValueError(f"Quantity {quantity} not found for {product_name}")

    def get_hire_price(self, product_name: str, quantity: int, duration: int):
        product = self.df_pr_hire.loc[self.df_pr_hire['Name'] == product_name]
        qty_prices = product.loc[product[DFLT.MIN_QTY.value] <= quantity]
        qty_dur_products = qty_prices.loc[qty_prices[DFLT.MIN_DUR.value] <= duration]
        hire_price = qty_dur_products['Price'].min()
        return hire_price

    def get_field_from_row(self, row: Series, field) -> str:
        res = row[field]
        ...
        return res

    def get_field(self, id_or_serial: str, field: str):
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
        fw_1 = self.get_field(id_or_serial=id_or_serial, field=DFLT.FW.value)
        if fw_version is None:
            assert fw_1
        else:
            assert fw_1 == fw_version
        ...

    def get_hire_line_item(self, product_name: str, quantity: int, duration: int):
        product_name, qty, dur = items_from_hire('Test - 16/08/2023 ref 31619')
        hire_price = self.get_hire_price(product_name, qty, dur)
        line_item = HireLineItem(name=product_name, quantity=qty, duration=dur, price_each=hire_price)
        ...
        # a_product = list(matched_products.values())[0]
        # a_price = a_product.get_price(1, 1)
        # assert isinstance(a_price, Decimal)
