import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#carga de datos
df = pd.read_csv("modern_renewable_prod.csv", sep=';')

#filtrar los paises suramericanos
paises_suramericanos = [
     'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia',
     'Ecuador', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela',
     'Surinam', 'Guyana'      
]

#se filtran por años y paises
df = df[
    (df['Entity'].isin(paises_suramericanos)) &
    (df['Year'] >= 2000) &  # Para incluir Colombia desde el 2000
    (df['Year'] <= 2022)
]

#Se conviernes todas las columnas en formato numerico
columnas_energia = [
    'Electricity from wind (TWh)',
    'Electricity from hydro (TWh)',
    'Electricity from solar (TWh)',
    'Other renewables including bioenergy (TWh)'
]

for col in columnas_energia:
    df[col] = pd.to_numeric(df[col], errors='coerce')

#Reemplazar nulos por 0
df[columnas_energia] = df[columnas_energia].fillna(0.0)

#Verificar que ya no haya nulos
print("Valores nulos por columna:\n", df.isnull().sum())

#Estadisticos personalizados
estadisticas = df[columnas_energia].describe(percentiles=[0, 0.05, 0.5, 0.95, 0.99, 1.0])
print(estadisticas)

#Dato atipico en la columna other... identificarlo
col_outlier = 'Other renewables including bioenergy (TWh)'

#Se identifica el valor mas alto de la columan
valor_max = df[col_outlier].max()
#Acá se identifica por la fila con el valor más alto el pais 
fila_outlier = df[df[col_outlier] == valor_max]
print("\nDato atípico encontrado:\n", fila_outlier)

#Reemplazar por promedio sin el outlier, donde no se incluye el valor atipico
promedio = df[df[col_outlier] < valor_max][col_outlier].mean()
#acá se reemplaza el valor atipico, por el promedio 
df.loc[df[col_outlier] == valor_max, col_outlier] = promedio

#Generación de electricidad en Colombia por fuentes de energía entre 2000 y 2022
df_sur = df[(df['Year'] >= 2012) & (df['Year'] <= 2022)]
#Consumo total por tipo de energía y año
grupo_energia = df_sur.groupby('Year')[columnas_energia].sum()

#visualización
plt.figure(figsize=(12, 6))
sns.lineplot(data=grupo_energia)
plt.title('Consumo Total por Tipo de Energía en Suramérica (2012-2022)', fontweight='bold')
plt.xlabel('Año', fontweight='bold')
plt.ylabel('Consumo (TWh)', fontweight='bold')
plt.grid(True)
plt.tight_layout()
plt.show()

#Grafico interactivo
#Filtro por los datos de Colombia
colombia_data = df[df['Entity'] == 'Colombia']

#años de inicio y final
inicio = 2000
final = 2022

#Filtro por años
data_year = colombia_data[(colombia_data['Year'] >= inicio) & (colombia_data['Year'] < final)]

#Se eligen las columnas donde quiero la información
fuentes_energia = ['Electricity from wind (TWh)', 'Electricity from hydro (TWh)', 'Electricity from solar (TWh)', 'Other renewables including bioenergy (TWh)']

#Saco sumatoria total de producción energetica
produccion_energetica = data_year[columnas_energia].sum()

df_energ = pd.DataFrame({'Fuentes de energía': fuentes_energia, 'Producción': produccion_energetica})
df_energ = df_energ.sort_values(by='Producción', ascending=False).round(3)

fig = px.bar(
    df_energ,
    x='Fuentes de energía',
    y='Producción',
    title="Generación de electricidad en Colombia por fuentes de energía entre 2000-2022",
    labels={'Producción': 'Generación de electricidad (TWh)'}
)

colors = px.colors.qualitative.Plotly[:len(columnas_energia)]
fig.update_traces(marker=dict(color=colors))
fig.show()
