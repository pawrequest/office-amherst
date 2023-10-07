from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pandas as pd

from excel.excel import check_data, convert, df_to_wb, set_data


def an_id(id_or_serial):
    return len(id_or_serial) == 4


# @id_exception_handler
def id_to_serial(radio_id, df):
    return convert(df=df, value=radio_id, key_column=DFLT.ID.value, result_column=DFLT.SERIAL.value)


# @id_exception_handler
def get_serial(id_or_serial, df):
    return id_or_serial if not an_id(id_or_serial) else id_to_serial(id_or_serial, df=df)


# @id_exception_handler
def serial_to_id(serial, df):
    return convert(df=df, value=serial, key_column=DFLT.SERIAL.value, result_column=DFLT.ID.value)


def get_id(id_or_serial, df):
    return id_or_serial if an_id(id_or_serial) else serial_to_id(id_or_serial, df=df)


@dataclass
class Identity:
    def __init__(self, df, id_or_serial=None):
        self.df = df
        if id_or_serial is None:
            raise ValueError("Must provide either ID or serial number.")
        self.id_number = get_id(id_or_serial, df=self.df)
        self.serial_number = get_serial(id_or_serial, df=self.df)



@dataclass
class Radio:
    identity: Identity


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
        self.df = pd.read_excel(workbook, sheet_name=sheet, header=header_row)

    def __enter__(self):
        self.asset_manager = AssetManager(self.df)
        return self.asset_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        if input("Save changes? (y/n)").lower() != 'y':
            return
        df_to_wb(workbook=self.workbook, sheet=self.sheet, header_row=self.header_row, out_file=self.out_file,
                 df=self.asset_manager.df)


class AssetManager:

    def __init__(self, df):
        self.df = df

    def set_fw(self, radio: Identity):
        radio_id = radio.id_number
        set_data(self.df, id_data=radio_id, id_header=DFLT.ID.value, value_header=DFLT.FW.value,
                 value_data=DFLT.FW_VERSION.value)
        return True

    def check_progged(self, id_to_check: Identity, fw_version=DFLT.FW_VERSION.value):
        return check_data(self.df, id_data=id_to_check.id_number, id_header=DFLT.ID.value, value_header=DFLT.FW.value,
                          value_data=fw_version)
