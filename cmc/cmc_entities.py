from dataclasses import dataclass
from enum import Enum
from typing import Optional, Iterable


@dataclass
class Connector:
    desc: str
    table: str


class Connection(Enum):
    CUSTOMER_HIRES = Connector(desc="Has Hired", table='Hire')
    CUSTOMER_SALES = Connector(desc="Involves", table='Saler')
    HIRES_CUSTOMER = Connector(desc="To", table='Customer')
    SALES_CUSTOMER = Connector(desc="To", table='Customer')
