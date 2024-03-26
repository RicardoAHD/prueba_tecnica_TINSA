"""Script to analyze data from a CSV file."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
file_path = 'test_tinsa_data.csv'  
data = pd.read_csv(file_path, delimiter=';')


# Dividir los inmuebles según su superficie
grandes = data[data['SUPERFICIE'] > 165]
medianos = data[(data['SUPERFICIE'] >= 53) & (data['SUPERFICIE'] <= 165)]
pequenos = data[data['SUPERFICIE'] < 53]
# Dividir los inmuebles según si tienen ascensor
con_ascensor = data[data['ASCENSOR'] == 'si']
sin_ascensor = data[data['ASCENSOR'] == 'no']
# Dividir los inmuebles según su antigüedad
nuevos = data[data['ANTIGUEDAD'] <= 15]
medios = data[(data['ANTIGUEDAD'] > 15) & (data['ANTIGUEDAD'] <= 46)]
viejos = data[data['ANTIGUEDAD'] > 46]
# Dividir los inmuebles según si son exteriores o interiores
exteriores = data[data['EXTERIOR_INTERIOR'] == 'EXTERIOR']
interiores = data[data['EXTERIOR_INTERIOR'] == 'INTERIOR']

#_______________________________________________________________________________________________
# Relación Antigüedad/Precios de Inmuebles
def plot_trend_line(x, y, label):
    model = LinearRegression().fit(x.values.reshape(-1, 1), y)
    plt.plot(x, model.predict(x.values.reshape(-1, 1)), color='black', linestyle='--', label=label)
# Graficar los puntos y las líneas de tendencia para cada grupo
precio_medio = data['VALOR'].mean()
antiguedad_media = data['ANTIGUEDAD'].mean()
# Graficar los puntos y las líneas de tendencia para cada grupo
plt.figure(figsize=(10, 6))
plt.scatter(nuevos['ANTIGUEDAD'], nuevos['VALOR'], color='blue', label='Nuevos(<15 años)')
plot_trend_line(nuevos['ANTIGUEDAD'], nuevos['VALOR'], label='Tendencia Nuevos')
plt.scatter(medios['ANTIGUEDAD'], medios['VALOR'], color='green', label='Medios(15<x<46 años)')
plot_trend_line(medios['ANTIGUEDAD'], medios['VALOR'], label='Tendencia Medios')
plt.scatter(viejos['ANTIGUEDAD'], viejos['VALOR'], color='red', label='Viejos(>46 años)')
plot_trend_line(viejos['ANTIGUEDAD'], viejos['VALOR'], label='Tendencia Viejos')
plt.xlabel('Antigüedad (años)')
plt.ylabel('Valor (€)')
plt.title('Relación Antigüedad/ Valor de Inmuebles')
plt.legend()
plt.grid(True)
plt.show()
#________________________________________________________________________________________________________


# Relación Superficie/Precio de Inmuebles
def plot_trend_line_and_mean(x, y, color, label):
    # Ajustar la línea de tendencia
    model = LinearRegression().fit(x.values.reshape(-1, 1), y)
    x_range = np.linspace(min(x), max(x), 100).reshape(-1, 1)
    y_pred = model.predict(x_range)
    plt.plot(x_range, y_pred, 'black', linestyle='--', label=f'Línea de tendencia ({label})')
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    plt.scatter(mean_x, mean_y, color='yellow', marker='x', s=100, label=f'Media ({label})')
plt.figure(figsize=(10, 6))
plt.scatter(grandes['SUPERFICIE'], grandes['VALOR'], color='blue', label='Grandes (>165 m²)')
plot_trend_line_and_mean(grandes['SUPERFICIE'], grandes['VALOR'], color='blue', label='Grandes (>165 m²)')
plt.scatter(medianos['SUPERFICIE'], medianos['VALOR'], color='green', label='Medianos (53-165 m²)')
plot_trend_line_and_mean(medianos['SUPERFICIE'], medianos['VALOR'], color='green', label='Medianos (53-165 m²)')
plt.scatter(pequenos['SUPERFICIE'], pequenos['VALOR'], color='red', label='Pequeños (<53 m²)')
plot_trend_line_and_mean(pequenos['SUPERFICIE'], pequenos['VALOR'], color='red', label='Pequeños (<53 m²)')
plt.xlabel('Superficie (m²)')
plt.ylabel('Valor (€)')
plt.title('Relación Superficie/ Valor de Inmuebles')
# Leyenda y cuadrícula
plt.legend()
plt.grid(True)
plt.show()

#_________________________________________________________________________________________________________________________________
exterior_con_ascensor = data[(data['ASCENSOR'] == 'si') & (data['EXTERIOR_INTERIOR'] == 'EXTERIOR')]
exterior_sin_ascensor = data[(data['ASCENSOR'] == 'no') & (data['EXTERIOR_INTERIOR'] == 'EXTERIOR')]
interior_con_ascensor = data[(data['ASCENSOR'] == 'si') & (data['EXTERIOR_INTERIOR'] == 'INTERIOR')]
interior_sin_ascensor = data[(data['ASCENSOR'] == 'no') & (data['EXTERIOR_INTERIOR'] == 'INTERIOR')]
# Calcular el precio promedio para cada grupo
precio_promedio_ext_con_ascensor = exterior_con_ascensor.groupby('DORMITORIOS')['VALOR'].mean()
precio_promedio_ext_sin_ascensor = exterior_sin_ascensor.groupby('DORMITORIOS')['VALOR'].mean()
precio_promedio_int_con_ascensor = interior_con_ascensor.groupby('DORMITORIOS')['VALOR'].mean()
precio_promedio_int_sin_ascensor = interior_sin_ascensor.groupby('DORMITORIOS')['VALOR'].mean()
# Crear un DataFrame con los precios PROMEDIO para cada grupo
df_precios = pd.DataFrame({
    'Exterior con Ascensor': precio_promedio_ext_con_ascensor,
    'Exterior sin Ascensor': precio_promedio_ext_sin_ascensor,
    'Interior con Ascensor': precio_promedio_int_con_ascensor,
    'Interior sin Ascensor': precio_promedio_int_sin_ascensor})
df_precios.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Número de Habitaciones')
plt.ylabel('Valor Promedio (€)')
plt.title('Relación Habitaciones/Valor medio de los Inmuebles()')
plt.legend(title='Tipo de Piso')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

#______________________________________________________________________________________________________________________________
#Crear la cuarta tabla: Relación Código Postal/Precio de Inmuebles
tipologias = data['TIPOLOGIA'].unique()

# Datos
codigos_postales = exteriores['CODPOS'].unique()
precios_exteriores = {cp: {tipologia: exteriores[(exteriores['CODPOS'] == cp) & (exteriores['TIPOLOGIA'] == tipologia)]['VALOR'].mean() for tipologia in tipologias} for cp in codigos_postales}
precios_interiores = {cp: {tipologia: interiores[(interiores['CODPOS'] == cp) & (interiores['TIPOLOGIA'] == tipologia)]['VALOR'].mean() for tipologia in tipologias} for cp in codigos_postales}

# Crear gráfico de barras apiladas
plt.figure(figsize=(12, 8))

# Definir colores para cada tipo de vivienda
colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray']

bottom = None
for idx, tipologia in enumerate(tipologias):
    precios_tipologia_exteriores = [precios_exteriores[cp][tipologia] for cp in codigos_postales]
    precios_tipologia_interiores = [precios_interiores[cp][tipologia] for cp in codigos_postales]
    
    plt.bar(codigos_postales, precios_tipologia_interiores, bottom=bottom, color=colors[idx], label=f'{tipologia} - Interior')
    plt.bar(codigos_postales, precios_tipologia_exteriores, bottom=bottom, color=colors[idx], alpha=0.5, label=f'{tipologia} - Exterior')
    
    if bottom is None:
        bottom = [0] * len(precios_tipologia_interiores)
    bottom = [bottom[i] + precios_tipologia_interiores[i] for i in range(len(precios_tipologia_interiores))]

plt.xlabel('Código Postal')
plt.ylabel('Valor Promedio (€)')
plt.title('Relación Código Postal/Valor de Inmuebles por Tipología')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.show()

_____________________________________________________________________________________________________________________________________
#valor medio de las propiedades a lo largo del tiempo

data['FECHA'] = pd.to_datetime(data['FECHA'])
valor_medio_mensual = data.groupby(data['FECHA'].dt.to_period('M')).agg({'VALOR':'mean'}).reset_index()
valor_medio_mensual['FECHA'] = valor_medio_mensual['FECHA'].dt.to_timestamp()
plt.figure(figsize=(12, 6))
sns.lineplot(x='FECHA', y='VALOR', data=valor_medio_mensual)
plt.title('Tendencia del Valor Medio de las Propiedades a lo largo del Tiempo')
plt.xlabel('Fecha')
plt.ylabel('Valor Medio (€)')
plt.xticks(rotation=45)
plt.show()
