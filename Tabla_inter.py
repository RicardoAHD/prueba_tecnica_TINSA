import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
import pandas as pd
import plotly.graph_objs as go
from tabulate import tabulate
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.io as pio
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors



ARCHIVO_CSV = 'test_tinsa_data.csv'                                     ##IMPORTANTE CAMBIAR LA RUTA RELATIVA PATH PARA CADA ARCHIVO QUE QUERAMOS ANALIZAR##


# Contadores
contador_unifamiliares = 0
contador_plurifamiliares = 0
contador_tasaciones_vigentes = 0

contador_tasaciones_caducadas = 0
contador_tasaciones_primer_cuatrimestre = 0
contador_tasaciones_segundo_cuatrimestre = 0
contador_tasaciones_tercer_cuatrimestre = 0
contador_ascensor_si = 0
contador_ascensor_no = 0
contador_exterior = 0
contador_interior = 0


# Variables para estadísticas
valores = []
superficies = []
dormitorios = []
banos = []
antiguedades = []
fecha_consulta = datetime.now()
pisos_por_codigo_postal = {}

# Abrir el archivo CSV en modo lectura
with open(ARCHIVO_CSV, 'r', encoding='utf-8') as file:
    lector_csv = csv.DictReader(file, delimiter=';')
    
# Usos cada fila del CSV
    for fila in lector_csv:
        if fila['TIPOLOGIA'] == 'UNIFAMILIAR':
            contador_unifamiliares += 1
        elif fila['TIPOLOGIA'] == 'PLURIFAMILIAR':
            contador_plurifamiliares += 1
        fecha_tasacion = datetime.strptime(fila['FECHA'], '%Y-%m')
        diferencia_tiempo = fecha_consulta - fecha_tasacion
        if diferencia_tiempo <= timedelta(days=180):
            contador_tasaciones_vigentes += 1
        else:
            contador_tasaciones_caducadas += 1
        mes = fecha_tasacion.month
        if mes >= 1 and mes <= 4:
            contador_tasaciones_primer_cuatrimestre += 1
        elif mes >= 5 and mes <= 8:
            contador_tasaciones_segundo_cuatrimestre += 1
        elif mes >= 9 and mes <= 12:
            contador_tasaciones_tercer_cuatrimestre += 1
        if fila['ASCENSOR'] == 'si':
            contador_ascensor_si += 1
        else:
            contador_ascensor_no += 1
        if fila['EXTERIOR_INTERIOR'] == 'EXTERIOR':
            contador_exterior += 1
        else:
            contador_interior += 1

      #CODIGOS POSTAL                                                                      +++++++++++++++++++++++++++++++++++++++++++++++++IDEA
       # codigo_postal = fila['CODPOS']
    # Verificar si el código postal ya está en el diccionario
    #if codigo_postal in pisos_por_codigo_postal:
        # Si ya existe, incrementar el contador
       # pisos_por_codigo_postal[codigo_postal] += 1
    #else:
        # Si es la primera vez que se encuentra, inicializar el contador en 1
        #pisos_por_codigo_postal[codigo_postal] = 1                                         +++++++++++++++++++++++++++++++++++++++++++++++++IDEA


#Valores para estadísticas
        valores.append(float(fila['VALOR']))
        superficies.append(float(fila['SUPERFICIE']))
        dormitorios.append(float(fila['DORMITORIOS']))
        banos.append(float(fila['BANNOS']))
        antiguedades.append(float(fila['ANTIGUEDAD']))    

# Calcular el número total de viviendas
numero_total_viviendas = contador_unifamiliares + contador_plurifamiliares

#Nro total de vivienda CDMUN                                                               +++++++++++++++++++++++++++INFORMACION DEL INE
total_viviendas_familiares = 254658
total_viviendas_construidas = 254736
total_viviendas_principales = 211358

#% Vivienda analizadas respecto al total                                                    +++++++++++++++++++++++++ Si el total % es insignifcante(<60%) uso interno
porcentaje_viviendas_familiares = (numero_total_viviendas / total_viviendas_familiares) * 100
porcentaje_viviendas_construidas = (numero_total_viviendas / total_viviendas_construidas) * 100
porcentaje_viviendas_principales = (numero_total_viviendas / total_viviendas_principales) * 100
porcentaje_viviendas_familiares_formateado = "{:.2f}%".format(porcentaje_viviendas_familiares)
porcentaje_viviendas_construidas_formateado = "{:.2f}%".format(porcentaje_viviendas_construidas)
porcentaje_viviendas_principales_formateado = "{:.2f}%".format(porcentaje_viviendas_principales)

#Tipologia de vivienda 
porcentaje_unifamiliares = (contador_unifamiliares / numero_total_viviendas) * 100
porcentaje_plurifamiliares = (contador_plurifamiliares / numero_total_viviendas) * 100

#tasaciones (vigencia 180días)
porcentaje_tasaciones_vigentes = (contador_tasaciones_vigentes / numero_total_viviendas) * 100
porcentaje_tasaciones_caducadas = (contador_tasaciones_caducadas / numero_total_viviendas) * 100

#Tasaciones por cuatrimestres 
total_tasaciones = numero_total_viviendas
porcentaje_tasaciones1 = (contador_tasaciones_primer_cuatrimestre/ total_tasaciones) * 100
porcentaje_tasaciones2= (contador_tasaciones_segundo_cuatrimestre / total_tasaciones) * 100
porcentaje_tasaciones3 =(contador_tasaciones_tercer_cuatrimestre / total_tasaciones) * 100

#Valores
valor_medio = sum(valores) / len(valores)
valor_maximo = max(valores)
valor_minimo = min(valores)
superficie_minimo = min(superficies)
superficie_maximo = max(superficies)
superficie_media = sum(superficies) / len(superficies)
dormitorios_minimo = min(dormitorios)
dormitorios_maximo = max(dormitorios)
dormitorios_media = sum(dormitorios) / len(dormitorios)
banos_media = sum(banos) / len(banos)
banos_maximo= max(banos)
banos_minimo= min(banos)
antiguedad_media = sum(antiguedades) / len(antiguedades)
antiguedad_minima = min (antiguedades) 
antiguedad_maxima = max(antiguedades)
total_pisos = numero_total_viviendas

#Calcular los porcentajes de ascensor
porcentaje_ascensor_si = (contador_ascensor_si / total_pisos) * 100
porcentaje_ascensor_no = (contador_ascensor_no / total_pisos) * 100

#Calcular los porcentajes de exterior/interior
porcentaje_exterior = (contador_exterior / total_pisos) * 100
porcentaje_interior = (contador_interior / total_pisos) * 100
# Tus resultados
results = [
    ("Nro total de viviendas en el estudio", numero_total_viviendas),
    ("Viviendas en estudio respecto al total de viviendas familiares", 
     f"{porcentaje_viviendas_familiares_formateado} de {total_viviendas_familiares}"),
    ("Viviendas en estudio respecto al total de viviendas construidas", 
     f"{porcentaje_viviendas_construidas_formateado} de {total_viviendas_construidas}"),
    ("Viviendas en estudio respecto al total de viviendas principales", 
     f"{porcentaje_viviendas_principales_formateado} de {total_viviendas_principales}"),
    ("Viviendas unifamiliares analizadas", "{:.2f}%".format(porcentaje_unifamiliares)),
    ("Viviendas plurifamiliares analizadas", "{:.2f}%".format(porcentaje_plurifamiliares)),
    ("Porcentaje de tasaciones vigentes", "{:.2f}%".format(porcentaje_tasaciones_vigentes)),
    ("Porcentaje de tasaciones caducadas", "{:.2f}%".format(porcentaje_tasaciones_caducadas)),
    ("% tasaciones 1er cuatri.", "{:.2f}%".format(porcentaje_tasaciones1)),
    ("% tasaciones 2er cuatri.", "{:.2f}%".format(porcentaje_tasaciones2)),
    ("% tasaciones 3er cuatri.", "{:.2f}%".format(porcentaje_tasaciones3)),
    ("Valor Medio", f"{valor_medio:.2f} €"),
    ("Valor Máximo", f"{valor_maximo:.2f} €"),
    ("Valor Mínimo", f"{valor_minimo:.2f} €"),
    ("Superficie Mínima", f"{superficie_minimo:.2f} metros^2"),
    ("Superficie Máxima", f"{superficie_maximo:.2f} metros^2"),
    ("Superficie Media", f"{superficie_media:.2f} metros^2"),
    ("Dormitorios Mínimo", f"{dormitorios_minimo:.2f} unidades"),
    ("Dormitorios Máximo", f"{dormitorios_maximo:.2f} unidades"),
    ("Dormitorios Media", f"{dormitorios_media:.2f} unidades"),
    ("Baños Máximo", f"{banos_maximo:.2f} unidades"),
    ("Baños Mínimo", f"{banos_minimo:.2f} unidades"),
    ("Baños Media", f"{banos_media:.2f} unidades"),
    ("Antigüedad Máxima", f"{antiguedad_maxima:.2f} años"),
    ("Antigüedad Mínima", f"{antiguedad_minima:.2f} años"),
    ("Antigüedad Media", f"{antiguedad_media:.2f} años"),
    ("Porcentaje de pisos con ascensor", f"{porcentaje_ascensor_si:.2f}%"),
    ("Porcentaje de pisos sin ascensor", f"{porcentaje_ascensor_no:.2f}%"),
    ("Porcentaje de pisos exteriores", f"{porcentaje_exterior:.2f}%"),
    ("Porcentaje de pisos interiores", f"{porcentaje_interior:.2f}%")
]

# Convertir los resultados en un DataFrame de pandas
df = pd.DataFrame(results, columns=["Indicador", "Valor"])

# Crear las figuras de Plotly
fig1 = go.Figure(go.Table(
    header=dict(values=["Indicador", "Valor"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['Indicador'], df['Valor']],
               fill_color='lavender',
               align='left'))
)

fig2 = make_subplots(rows=1, cols=1)

# Añadir gráficos a la figura
# Aquí puedes agregar tus gráficos utilizando Plotly

# Actualizar el diseño y estilo de la tabla
fig1.update_layout(width=1000, height=800, title='Tabla de Resultados', title_x=0.5)

# Mostrar la tabla y los gráficos interactivos
fig1.show()
# fig2.show()  # Muestra los gráficos interactivos, asegúrate de agregar los gráficos a 'fig2' antes de descomentar esta línea
