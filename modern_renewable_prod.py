import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar los datos
df = pd.read_csv("modern_renewable_prod.csv", sep=';')

# Filtrar por países suramericanos
paises_suramericanos = [
     'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia',
      'Ecuador', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela',
      'Surinam', 'Guyana'      
]

# Filtrar por países y años
df = df[
    (df['Entity'].isin(paises_suramericanos)) &
    (df['Year'] >= 2012) &
    (df['Year'] <= 2022)
]

# Convertir columnas de energía a tipo numérico
columnas_energia = [
    'Electricity from wind (TWh)',
    'Electricity from hydro (TWh)',
    'Electricity from solar (TWh)',
    'Other renewables including bioenergy (TWh)'
]

for col in columnas_energia:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reemplazar nulos por 0
df[columnas_energia] = df[columnas_energia].fillna(0.0)

# Verificar que ya no haya nulos
print("Valores nulos por columna:\n", df.isnull().sum())

# Agrupación: Consumo total por tipo de energía y año
grupo_energia = df.groupby('Year')[['Electricity from wind (TWh)', 'Electricity from hydro (TWh)', 'Electricity from solar (TWh)', 'Other renewables including bioenergy (TWh)']].sum()

# Visualización
plt.figure(figsize=(12, 6))
sns.lineplot(data=grupo_energia)
plt.title('Consumo Total por Tipo de Energía en Suramérica (2012-2022)')
plt.xlabel('Año')
plt.ylabel('Consumo (TWh)')
plt.grid(True)
plt.tight_layout()
plt.show()


#Generación de electricidad en Colombia por fuentes de energía entre 2000 y 2022
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
produccion_energetica = data_year[fuentes_energia].sum()

df_energ = pd.DataFrame({'Fuentes de energía': fuentes_energia, 'Producción': produccion_energetica})
df_energ = df_energ.sort_values(by='Producción', ascending=False)

#Visualización
fig = px.bar(
    df_energ, 
    x='Fuentes de energía', 
    y='Producción', 
    title=f"Generación de electricidad en Colombia por fuentes de energía entre {inicio}-{final}",
    labels={'Producción': 'Generación de electricidad (TWh)'}
)

colors = px.colors.qualitative.Plotly[:len(fuentes_energia)]
fig.update_traces(marker=dict(color=colors))
fig.show()



