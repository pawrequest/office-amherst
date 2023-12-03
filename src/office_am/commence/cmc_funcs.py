import datetime
from decimal import Decimal
from typing import List

from win32com.client import Dispatch

from . import auto_cmc
from .cmc_entities import CONNECTION, CommenceNotInstalled



ALLOWED_ZERO_KEYS = ['Delivery Cost']


def clean_dict(in_dict: dict) -> dict:
    out_dict = {}
    zero_values = ['', False, 0, 'FALSE', '0']

    for k, v in in_dict.items():
        if v in zero_values:
            out_dict[k] = None
            continue
        if v == 'TRUE':
            out_dict[k] = True
        if v == 'FALSE':
            out_dict[k] = False
        else:
            try:
                out_dict[k] = datetime.datetime.strptime(v, '%d/%m/%Y').date()
            except Exception:  # noqa
                try:
                    out_dict[k] = Decimal(v)
                except Exception:  # noqa
                    try:
                        out_dict[k] = int(v)
                    except Exception:  # noqa
                        out_dict[k] = v
    return out_dict


def clean_hire_dict(hire: dict):
    out_dict = {}
    for k, v in hire.items():
        # if k.startswith('Number '):
        #     out_dict[k[7:]] = v
        if k.startswith('Inv '):
            continue
        # if k == 'Closed':
        #     out_dict[k] = None
        else:
            out_dict[k] = v

    return clean_dict(out_dict)
