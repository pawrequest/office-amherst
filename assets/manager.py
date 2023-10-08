from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import pandas as pd

from excel.excel import check_data, convert, df_overwrite_wb, get_data_from_excel, set_data


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

    def __eq__(self, other):
        return self.id_number == other.id_number and self.serial_number == other.serial_number



class Radio(Asset):
    fw_version: str = ''


class DFLT(Enum):
    SERIAL = 'Barcode'
    ID = 'Number'
    FW = 'FW'
    FW_VERSION = 'XXXX'
    WB = Path(__file__).resolve().with_name("assets_in.xlsx")
    OUTPUT = Path(__file__).resolve().with_name("assets_out.xlsx")
    SHEET = 'Sheet1'
    HEAD = 2


class AssetManagerContext:
    def __init__(self, workbook=DFLT.WB.value, sheet=DFLT.SHEET.value, header_row=int(DFLT.HEAD.value), out_file=None):
        self.out_file = out_file or workbook
        self.workbook = workbook
        self.sheet = sheet
        self.header_row = header_row
        self.df = pd.read_excel(workbook, sheet_name=sheet, header=header_row, dtype=str)

    def __enter__(self):
        self.asset_manager = AssetManager(self.df)
        return self.asset_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if input("Save changes? (y/n)").lower() != 'y':
        #     return
        df_overwrite_wb(input_workbook=self.workbook, sheet=self.sheet, header_row=self.header_row, out_file=self.out_file,
                        df=self.asset_manager.df)


class AssetManager:

    def __init__(self, df):
        self.df = df
        
    def get_asset(self, id_or_serial: str):
        if id_or_serial is None:
            raise ValueError("Must provide either ID or serial number.")
        id_number, serial = get_id_and_serial(id_or_serial, df=self.df)
        # id_number = get_id(id_or_serial, df=self.df)
        # serial_number = get_serial(id_or_serial, df=self.df)
        return Asset(id_number=id_number, serial_number=serial)

    def set_fw(self, asset: Asset, fw: Optional[str] = DFLT.FW_VERSION.value):
        radio_id = asset.id_number
        asset.fw_version = fw or DFLT.FW_VERSION.value
        self.df[DFLT.FW.value][self.df[DFLT.ID.value].astype(str) == str(radio_id)] = asset.fw_version

        # set_data(self.df, id_data=radio_id, id_header=DFLT.ID.value, value_header=DFLT.FW.value,
        #          value_data=fw)
        return True

    def check_progged(self, id_to_check: Asset, fw_version=DFLT.FW_VERSION.value):
        return check_data(self.df, id_data=id_to_check.id_number, id_header=DFLT.ID.value, value_header=DFLT.FW.value,
                          value_data=fw_version)

    def row_to_asset(self, row_number, end_row=None):
        if end_row is not None:
            id_nums = self.df[DFLT.ID.value].loc[row_number:end_row - 1].values
            return [self.get_asset(id_or_serial=id_num) for id_num in id_nums]
        id_num = self.df[DFLT.ID.value].iloc[row_number]
        return self.get_asset(id_or_serial=id_num)
