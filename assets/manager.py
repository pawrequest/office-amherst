import json
import os
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Optional

import pandas as pd
from pandas import Series

from in_out.cmc_direct import Commence
from in_out.excel import df_overwrite_wb
from tmplt.entities import LineItem, Product


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
        self.json_file = self.out_file.with_suffix('.json')  # JSON file path with new suffix
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
        if os.path.exists(self.json_file):  # Check if JSON file exists
            self.load_dfs_from_json()
        else:
            self.df_a = pd.read_excel(self.workbook_ast, sheet_name=self.sheet, header=self.header_row, dtype=str)
            self.df_pr_hire = pd.read_excel(self.workbook_prcs, sheet_name='Hire', header=0,
                                            converters={'Price': decimal_from_value})
            self.df_pr_sale = pd.read_excel(self.workbook_prcs, sheet_name='Sale', header=0,
                                            converters={'Price': decimal_from_value})

    def load_dfs_from_json(self):
        with open(self.json_file, 'r') as json_file:
            data = json.load(json_file)
            [setattr(self, dfname, pd.read_json(df, dtype ={'Price': Decimal})) for dfname, df in data.items()]
            ...

    def save_dfs_to_json(self):
        data = {
            'df_a': self.df_a.to_json(),
            'df_pr_hire': self.df_pr_hire.to_json(),
            'df_pr_sale': self.df_pr_sale.to_json()
        }
        ...
        with open(self.json_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        df_overwrite_wb(input_workbook=self.workbook_ast, sheet=self.sheet, header_row=self.header_row,
                        out_file=self.out_file, df=self.asset_manager.df_a)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Hire', header_row=0,
                        out_file=DFLT.WB_PRC.value, df=self.asset_manager.df_pr_hire)
        df_overwrite_wb(input_workbook=DFLT.WB_PRC.value, sheet='Sale', header_row=0,
                        out_file=DFLT.OUT_PRC.value, df=self.asset_manager.df_pr_sale)
        self.save_dfs_to_json()


@dataclass
class HireOrder:
    line_items: [LineItem]
    duration: int

    @property
    def total_price(self):
        return sum([itm.line_price for itm in self.line_items])

    def __str__(self):
        return f"Order for {self.duration} weeks: {self.line_items}"

    # @classmethod
    # def from_dur_and_dict(cls, dur, hire_dict):
    #     items = []
    #     for k, v in hire_dict.items():
    #         price_each = self.get_hire_price(k, v, duration)
    #         return [cls(name=k, quantity=v, duration=duration, price_each=price_each) for k, v in hire_dict.items()]


class AssetManager:

    def __init__(self, df_a, df_pr_hire, df_pr_sale):
        self.df_a = df_a
        self.df_pr_hire = df_pr_hire
        self.df_pr_sale = df_pr_sale
        # self.cmc = Commence()

    def add_price_each_to_df(self):
        ...

    def connect_cmc(self, table_name):
        self.cmc = Commence()

    def make_hire_order(self, hire_dict, duration):
        lineitems = []

        for name, qty in hire_dict.items():
            price = self.get_hire_price(name, quantity=qty, duration=duration)
            name = f'{name}_hire_{duration}_weeks'
            product = Product(name=name, description='desc', price_each=price)
            lineitems.append(LineItem(product=product, quantity=qty))
        order = HireOrder(line_items=lineitems, duration=duration)
        return order

    def row_from_product_name(self, category, product_name: str) -> Series:
        if category == 'Hire':
            row = self.df_pr_hire.loc[self.df_pr_hire['Name'] == product_name]
        elif category == 'Sale':
            row = self.df_pr_sale.loc[self.df_pr_sale['Name'] == product_name]
        else:
            raise ValueError(f"Category {category} not found")
        return handle_row(row)

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
        mp = self.df_pr_sale.loc[self.df_pr_sale['Name'] == product_name]
        mp_prc = mp.loc[mp[DFLT.MIN_QTY.value] <= quantity, 'Price'].min().values
        try:
            return Decimal(mp_prc[0])
        except IndexError:
            raise ValueError(f"Quantity {quantity} not found for {product_name}")

    def get_hire_price(self, product_name: str, quantity: int, duration: int):
        product = self.df_pr_hire.loc[self.df_pr_hire['Name'] == product_name]
        valid_products = product[(product['Min Qty'] <= quantity) & (product['Min Duration'] <= duration)]

        if not valid_products.empty:
            best_product = valid_products.sort_values(by=['Min Qty', 'Min Duration'], ascending=[False, False]).iloc[0]
            price = best_product['Price']
            return Decimal(price)
        else:
            raise ValueError("Product not found or no valid price found")

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
        product_name, qty, dur = self.items_from_hire('Test - 16/08/2023 ref 31619')
        # hire_price = self.get_hire_price(product_name, qty, dur)
        # line_item = HireLineItem(name=product_name, quantity=qty, duration=dur, price_each=hire_price)
        ...
        # a_product = list(matched_products.values())[0]
        # a_price = a_product.get_price(1, 1)
        # assert isinstance(a_price, Decimal)

    def items_from_hire(self):
        return 1
