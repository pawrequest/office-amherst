from assets.manager import Asset, AssetManagerContext, DFLT

#
with AssetManagerContext(out_file=DFLT.OUTPUT.value) as am:
    while True:
        # radio = Asset(am.df, id_or_serial=input("Enter ID or Serial: "))
        radio2 = Asset(am.df, id_or_serial='1111')
        rad = am.row_to_asset(0)
        res = rad == radio2
        rads = am.row_to_asset(am.df, 0, 2)

        am.set_fw(radio, fw="some firmware")
        if input("Continue? (y/n)").lower() != 'y':
            break

9
