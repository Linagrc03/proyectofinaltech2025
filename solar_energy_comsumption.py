import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar los datos
df = pd.read_csv("solar_energy_comsumption.csv", sep=';')

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
columnas_energia = ['Electricity from solar (TWh)']

for col in columnas_energia:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reemplazar nulos por 0
df[columnas_energia] = df[columnas_energia].fillna(0.0)

# Verificar que ya no haya nulos
print("Valores nulos por columna:\n", df.isnull().sum())

#Asignar años
def asignacion_año(year):
    for decada in decadas:
        if year >= decada and year < decada + 10:
            return decada
    return "2020s" 

#Definir los años por rangos para las decadas
decadas = list(range(2000, 2022, 10))

#Filtra los paises suramericanos
produccion = df[df['Entity'].isin(paises_suramericanos)].copy()
#Asignamos la columna Decada
produccion['Decade'] = produccion['Year'].apply(asignacion_año)

#Se agrupan las columnas paises y decada para sacar el total y sumar
grupo_produccion = produccion.groupby(['Entity', 'Decade'])['Electricity from solar (TWh)'].sum().unstack(fill_value=0)

#Visualización
grupo_produccion.plot(kind='bar', figsize=(15, 10))
plt.title("Generación de electricidad solar en países seleccionados a lo largo de décadas", fontweight='bold')
plt.xlabel("Paises", fontweight='bold')
plt.ylabel("Electricidad total procedente de energía solar (TWh)", fontweight='bold')
plt.legend(title="Decada")
plt.show()

#visualización mapa mundial
fig = px.choropleth(
    df,
    locations="Entity",
    locationmode="country names",
    color="Electricity from solar (TWh)",
    animation_frame="Year",
    color_continuous_scale="YlGnBu",
    range_color=(0, df["Electricity from solar (TWh)"].max())
)

fig.update_geos(projection_type="natural earth")

fig.update_layout(
    title="Mapa mundial de producción de energía solar",
    coloraxis_colorbar={"title": "Solar Energy Production (TWh)"}
)

fig.show()