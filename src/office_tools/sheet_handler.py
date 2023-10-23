from abc import ABC, abstractmethod
from typing import Any

from office_tools.excel import pathy


def one_exists(idx: int or None, id: str or None) -> None:
    if not idx and not id:
        raise ValueError("Must provide idx or id")


class SheetHandler(ABC):
    def __init__(self, sheet):
        self.sheet = sheet

    @abstractmethod
    def get_row(self, row_num: int or None, row_id: str or None) -> Any:
        one_exists(row_num, row_id)

    @abstractmethod
    def set_row(self, row_num: int or None, row_id: str or None, values: list) -> None:
        one_exists(row_num, row_id)

    @abstractmethod
    def get_cell(self, row_idx: int or None, row_id: str or None, col_idx: int or None, col_id: str or None) -> Any:
        one_exists(row_idx, row_id)
        one_exists(col_idx, col_id)

    @abstractmethod
    def set_cell(self, cell_name: str, value: str) -> None:
        ...




class WbHandler(ABC):

    def __init__(self, wb_pathy: pathy, sheet_handler: SheetHandler):
        self.wb_pathy = wb_pathy

    def open_wb(self, wb_pathy: pathy) -> None:
        raise NotImplementedError

    def save_wb(self, wb_pathy: pathy) -> None:
        raise NotImplementedError

    def close_wb(self) -> None:
        raise NotImplementedError

    def get_sheet(self, sheet_name: str) -> None:
        raise NotImplementedError


