import sys

from win32com import client
from win32com.client import makepy

from win32com.gen_py import auto_cmc

from win32com.client import gencache


gencache.EnsureModule('{C92C33EC-2A72-11D0-8A93-444553540000}', 0, 1, 0)
