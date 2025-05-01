import pandas as pd
from pandasgui import show

# Leer archivo Excel (cambia la ruta al archivo real)
ruta_excel = 'BD.xlsx'

# Si sabes el nombre de la hoja:
df = pd.read_excel(ruta_excel, sheet_name='Base')

# Si no sabes el nombre de la hoja, puedes listar todas:
# xls = pd.ExcelFile(ruta_excel)
# print(xls.sheet_names)

# Mostrar en PandasGUI
show(df)
