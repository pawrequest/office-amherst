from assets.manager import Asset, ManagerContext
from assets.entities import DFLT

#
with ManagerContext(out_file=DFLT.OUT_AST.value) as am:
    while True:
        # radio = Asset(am.df, id_or_serial=input("Enter ID or Serial: "))
        radio2 = Asset(am.df_a, id_or_serial='1111')
        rad = am.row_to_asset(0)
        res = rad == radio2
        rads = am.row_to_asset(am.df_a, 0, 2)

        am.set_fw(radio, fw="some firmware")
        if input("Continue? (y/n)").lower() != 'y':
            break

9
