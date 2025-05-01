import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar los datos
df = pd.read_csv("hydropower_consumption.csv", sep=';')

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
columnas_energia = ['Electricity from hydro (TWh)']

for col in columnas_energia:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Reemplazar nulos por 0
df[columnas_energia] = df[columnas_energia].fillna(0.0)

# Verificar que ya no haya nulos
print("Valores nulos por columna:\n", df.isnull().sum())

# Estadísticos personalizados
estadisticas = df[columnas_energia].describe(percentiles=[0, 0.05, 0.5, 0.95, 0.99, 1.0])

# Mostrar la tabla
print(estadisticas)

# Filtrar por países
data = df[df['Entity'].isin(paises_suramericanos)]

#Visualización
fig = px.scatter(data, x="Year", y="Electricity from hydro (TWh)", animation_frame="Year", 
                 animation_group="Entity", size="Electricity from hydro (TWh)", color="Entity", 
                 hover_name="Entity", size_max=55, range_x=[data['Year'].min(), data['Year'].max()], 
                 range_y=[0, data['Electricity from hydro (TWh)'].max()],

            #Traducción a español de leyendas
            labels={
                    "Year": "Año",
                    "Entity": "País",
                    "Electricity from hydro (TWh)": "Electricidad hidroeléctrica (TWh)"
                },

            title="Producción de electricidad hidroeléctrica en Sudamérica"
)

fig.show()

# Filtrar datos de Colombia por los últimos 10 años
colombia_data = df[df['Entity'] == 'Colombia']
año_actual = colombia_data['Year'].max()
ultimos_10_años = colombia_data[colombia_data['Year'] > año_actual - 10]

# Crear gráfico
plt.figure(figsize=(10, 6))
plt.plot(ultimos_10_años['Year'], 
         ultimos_10_años['Electricity from hydro (TWh)'], 
         marker='o', 
         color='blue', 
         linestyle='-')

# Títulos y etiquetas
plt.title("Uso de energía hidroeléctrica en Colombia en los últimos 10 años")
plt.xlabel("Año")
plt.ylabel("Electricidad hidroeléctrica (TWh)")

# Opcional: mostrar los valores en cada punto
for x, y in zip(ultimos_10_años['Year'], ultimos_10_años['Electricity from hydro (TWh)']):
    plt.text(x, y + 0.5, f"{y:.1f}", ha='center')

plt.grid(True)
plt.tight_layout()
plt.show()

# Filtrar datos de Colombia desde el año 2000
ultimos_años = colombia_data[colombia_data['Year'] >= 2000]

# Datos para el gráfico
produccion_hidroelectrica = ultimos_años['Electricity from hydro (TWh)']
años = ultimos_años['Year'].astype(str)  # convertir a string para mostrar en el gráfico

# Encontrar el índice del año con mayor producción
max_index = produccion_hidroelectrica.idxmax()
explode = [0.1 if idx == max_index else 0 for idx in produccion_hidroelectrica.index]

# Crear gráfico de pastel
plt.figure(figsize=(10, 8))
plt.pie(
    produccion_hidroelectrica, 
    labels=años, 
    autopct='%1.1f%%', 
    startangle=140, 
    explode=explode,
    wedgeprops=dict(width=0.5)  # para simular el "hole" de plotly
)

plt.title("Distribución de producción hidroeléctrica en Colombia (últimos 22 años)")
plt.axis('equal')  # Para que el gráfico sea circular
plt.tight_layout()
plt.show()

produccion_total_paises = data.groupby('Entity')['Electricity from hydro (TWh)'].sum().sort_values(ascending=False)

#Visualización
plt.figure(figsize=(14, 8))
bars = plt.bar(produccion_total_paises .index, produccion_total_paises .values, color='coral')
plt.title('Producción total de energía hidroeléctrica de países específicos', fontsize=14, fontweight='bold')
plt.xlabel('País', fontsize=12, fontweight='bold')
plt.ylabel('Electricidad total procedente de energía hidroeléctrica (TWh)', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

for bar in bars:
    if bar.get_x() == produccion_total_paises .index.get_loc("Colombia"):
        bar.set_color('blue')
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom', fontsize=10)

plt.grid(axis='y')
plt.tight_layout()
plt.show()