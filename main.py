import timeit

from account.check_invoice_paid import check_paid

asset_input = './assets_in.xls'
asset_output = './asset_example_output.xlsx'
serial_numbers = ['719336170G0064']

ac_input = './ac_example.xls'
invoice_nums = [r'R:\ACCOUNTS\invoices\a24301.docx']

# edit_ex_col(
#     workbook=asset_input,
#     outfile=asset_output,
#     sheet='Sheet1',
#     header_i=2,
#     col_with_name='Barcode',
#     data_to_check=serial_numbers,
#     data_insert="yes edited",
#     col_edit='REPROG'
# )
#
starting_time = timeit.default_timer()

check_paid(workbook=ac_input, data_to_check=invoice_nums)
time_taken = timeit.default_timer() - starting_time
print ('time taken: ', time_taken, 'seconds')
