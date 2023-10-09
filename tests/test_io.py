from in_out.dde import get_conversation_func
from in_out.i_o import get_all_fieldnames, get_cursor, get_database, get_fields


def test_gippy():
    # conv = get_conversation_func()
    # fields = ["Delivery Contact", "Delivery Name", "Delivery Address", "Delivery Postcode", "Number UHF",
    #                  "Booked Date", "Name",]
    # data = get_fields(conv, 'Hire', 'Trampoline League - 27/06/2023 ref 31247', fields=fields)
    #
    # conv2 = get_conversation_func()
    # fields2 = get_all_fieldnames(conv2, 'Hire')
    #
    # conv3 = get_conversation_func()
    # data3 = get_fields(conv3, 'Hire', 'Trampoline League - 27/06/2023 ref 31247', fields=fields2)
    #
    # ...
    #
    # # fields2 = get_all_fieldnames(conv, 'Hire')
    # # fields_arg = ', '.join(fields2)
    # # conv2 = get_conversation_func()
    # # data2 = get_fields(conv, 'Hire', 'Trampoline League - 27/06/2023 ref 31247', fields=fields2)
    db = get_database()
    curs = get_cursor(db, 'Customer')
    result = curs.RowCount
    res = curs.GetQueryRowSet(1)
    ...

    ...


successful_fields_arg = "'Delivery Contact, Delivery Name, Delivery Address, Delivery Postcode, Number UHF, Booked Date, Name'"
succ_fields = ['Delivery Contact', 'Delivery Name', 'Delivery Address', 'Delivery Postcode', 'Number UHF',
               'Booked Date', 'Name']
un_arg = "Name, Actual Return Date, All Address, Bar Codes, Booked Date, Boxes, Closed, DB label printed, Delivery Address, Delivery Contact, Delivery Cost, Delivery Description, Delivery Email, Delivery Name, Delivery Postcode, Delivery Ref, Delivery Tel, Discount Description, Discount Percentage, Due Back Date, Hire Sheet Printed, Hire Sheet Text, Inbound ID, Instruc Icom, Instruc Megaphone, Instruc Walkies, Inv Batt Desc, Inv Batt Price, Inv Batt Qty, Inv Bighead Desc, Inv Bighead Price, Inv Bighead Qty, Inv Booked Date, Inv Case Desc, Inv Case Price, Inv Case Qty, Inv Charger Desc, Inv Delivery Desc, Inv Due Back Date, Inv EM Desc, Inv EM Price, Inv EM Qty, Inv EMC Desc, Inv EMC Price, Inv EMC Qty, Inv Headset Desc, Inv Headset Price, Inv Headset Qty, Inv Icom Desc, Inv Icom Price, Inv Icom Qty, Inv Meg Batt Desc, Inv Mega Desc, Inv Mega Price, Inv Mega Qty, Inv Parrot Desc, Inv Parrot Price, Inv Parrot Qty, Inv Purchase Order, Inv Return Desc, Inv Send Desc, Inv Send Out Date, Inv UHF Desc, Inv UHF Price, Inv UHF Qty, Inv VHF Desc, Inv VHF Price, Inv VHF Qty, Inv Wand Desc, Inv Wand Price, Inv Wand Qty, Invoice, Megaphone charger, Missing Kit, Number Aerial Adapt, Number Batteries, Number Cases, Number Clipon Aerial, Number EM, Number EMC, Number Headset, Number Headset Big, Number Icom, Number ICOM Car Lead, Number ICOM PSU, Number Magmount, Number Megaphone, Number Megaphone Bat, Number Parrot, Number Repeater, Number Sgl Charger, Number UHF, Number UHF 6-way, Number VHF, Number VHF 6-way, Number Wand, Number Wand Battery, Number Wand Charger, Outbound ID, Packed By, Packed Date, Packed Time, Payment Terms, Pickup Arranged, PreShip Emailed, Purchase Order, Purpose, Radio Type, Recurring Hire, Reference Number, Reprogrammed, Return Notes, Send / Collect, Send Method, Send Out Date, Sending Status, ShipMe, Special Kit, Status, Unpacked by, Unpacked Date, Unpacked Time, Weeks"
unf_fields = ['Name', 'Actual Return Date', 'All Address', 'Bar Codes', 'Booked Date', 'Boxes', 'Closed',
              'DB label printed', 'Delivery Address', 'Delivery Contact', 'Delivery Cost', 'Delivery Description',
              'Delivery Email', 'Delivery Name', 'Delivery Postcode', 'Delivery Ref', 'Delivery Tel',
              'Discount Description', 'Discount Percentage', 'Due Back Date', 'Hire Sheet Printed', 'Hire Sheet Text',
              'Inbound ID', 'Instruc Icom', 'Instruc Megaphone', 'Instruc Walkies', 'Inv Batt Desc', 'Inv Batt Price',
              'Inv Batt Qty', 'Inv Bighead Desc', 'Inv Bighead Price', 'Inv Bighead Qty', 'Inv Booked Date',
              'Inv Case Desc', 'Inv Case Price', 'Inv Case Qty', 'Inv Charger Desc', 'Inv Delivery Desc',
              'Inv Due Back Date', 'Inv EM Desc', 'Inv EM Price', 'Inv EM Qty', 'Inv EMC Desc', 'Inv EMC Price',
              'Inv EMC Qty', 'Inv Headset Desc', 'Inv Headset Price', 'Inv Headset Qty', 'Inv Icom Desc',
              'Inv Icom Price', 'Inv Icom Qty', 'Inv Meg Batt Desc', 'Inv Mega Desc', 'Inv Mega Price', 'Inv Mega Qty',
              'Inv Parrot Desc', 'Inv Parrot Price', 'Inv Parrot Qty', 'Inv Purchase Order', 'Inv Return Desc',
              'Inv Send Desc', 'Inv Send Out Date', 'Inv UHF Desc', 'Inv UHF Price', 'Inv UHF Qty', 'Inv VHF Desc',
              'Inv VHF Price', 'Inv VHF Qty', 'Inv Wand Desc', 'Inv Wand Price', 'Inv Wand Qty', 'Invoice',
              'Megaphone charger', 'Missing Kit', 'Number Aerial Adapt', 'Number Batteries', 'Number Cases',
              'Number Clipon Aerial', 'Number EM', 'Number EMC', 'Number Headset', 'Number Headset Big', 'Number Icom',
              'Number ICOM Car Lead', 'Number ICOM PSU', 'Number Magmount', 'Number Megaphone', 'Number Megaphone Bat',
              'Number Parrot', 'Number Repeater', 'Number Sgl Charger', 'Number UHF', 'Number UHF 6-way', 'Number VHF',
              'Number VHF 6-way', 'Number Wand', 'Number Wand Battery', 'Number Wand Charger', 'Outbound ID',
              'Packed By', 'Packed Date', 'Packed Time', 'Payment Terms', 'Pickup Arranged', 'PreShip Emailed',
              'Purchase Order', 'Purpose', 'Radio Type', 'Recurring Hire', 'Reference Number', 'Reprogrammed',
              'Return Notes', 'Send / Collect', 'Send Method', 'Send Out Date', 'Sending Status', 'ShipMe',
              'Special Kit', 'Status', 'Unpacked by', 'Unpacked Date', 'Unpacked Time', 'Weeks']
