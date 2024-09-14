import openpyxl

book = openpyxl.load_workbook('nomina/static/nomina/files/excel_copia.xlsm')
sheet = book['EMPLEADOS']

b3 = sheet['B3']
print(b3)