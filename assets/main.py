from assets.manager import AssetManagerContext, DFLT, Identity

# with AssetManagerContextOLD(out_file=DFLT.OUTPUT.value) as am:
# # with AssetManagerContext(out_file=DFLT.OUTPUT.value) as am:
#     radio = Identity(am.df, id_or_serial='1111')
    # radio2 = Identity(am.df, id_or_serial='2222')
    # radio3 = Identity(am.df, id_or_serial='3333')
    # ...
    # print(radio.id_number)

...
#
with AssetManagerContext(out_file=DFLT.OUTPUT.value) as am:
    radio3 = Identity(am.df, id_or_serial='3333')

    ...

#
# AMC = AssetManagerContext2(out_file=DFLT.OUTPUT.value)
# ...