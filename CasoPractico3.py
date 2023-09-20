""" 1 - Cargar los datos y realizar un análisis exploratorio y 
una evaluación de la calidad de los datos necesarios para el resto del caso. 
Específicamente, evaluar la integridad, validez y actualidad de los datos y 
proponer estrategias de mitigación de los posibles problemas encontrados. """

##### 1- Respuesta: 
# Importamos las librerías necesarias
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargamos el conjunto de datos
compas_data = pd.read_csv("compas-scores.csv")

# Visualizamos las primeras filas del conjunto de datos para revisar la estructura
print(compas_data.head())

# Evaluamos la integridad - Verificamos si hay valores faltantes
missing_values = compas_data.isnull().sum()
print(missing_values)
""" Existen valores faltantes. """

# Verificamos la validez de los datos en la columna "is_recid" e "is_violent_recid"
#### Se verifica si los valores de las columnas se encuentran entre [-1,1] y [0,1] para comprobar su validez
# Verificar si los valores en la columna "is_recid" están en el rango de -1 a 1
valid_is_recid = (compas_data['is_recid'] >= -1) & (compas_data['is_recid'] <= 1)

# Verificar si los valores en la columna "is_violent_recid" están en el rango de -1 a 1
valid_is_violent_recid = (compas_data['is_violent_recid'] >= -1) & (compas_data['is_violent_recid'] <= 1)

# Comprobar si todas las filas cumplen con la validación
if valid_is_recid.all() and valid_is_violent_recid.all():
    print("Los datos en las columnas 'is_recid' e 'is_violent_recid' son válidos en términos de formato.")
else:
    print("Los datos en las columnas 'is_recid' e 'is_violent_recid' no cumplen con el formato esperado.")

"""R: Se imprime en la consola (Los datos en las columnas 'is_recid' e 'is_violent_recid' son válidos en términos de formato.)"""

# Verificamos la actualidad de las fechas en el conjunto de datos
#### Definir la fecha de referencia actual (por ejemplo, año 2023)
fecha_referencia = datetime(2023, 9, 15)
#### Convertimos las columnas de fechas a objetos datetime si no lo están
compas_data['compas_screening_date'] = pd.to_datetime(compas_data['compas_screening_date'], errors='coerce')
compas_data['r_offense_date'] = pd.to_datetime(compas_data['r_offense_date'], errors='coerce')
#### Verificamos la actualidad de la columna "compas_screening_date"
actual_compas_screening = (compas_data['compas_screening_date'] <= fecha_referencia).all()
print(f"Actualidad de 'compas_screening_date': {actual_compas_screening}")
#### Verificamos la actualidad de la columna "r_offense_date"
actual_r_offense = (compas_data['r_offense_date'] <= fecha_referencia).all()
print(f"Actualidad de 'r_offense_date': {actual_r_offense}")

"""" R: Se imprime en el terminal
(Los datos en las columnas 'is_recid' e 'is_violent_recid' son válidos en términos de formato.
Actualidad de 'compas_screening_date': True
Actualidad de 'r_offense_date': False)
Por tanto, se debe modificar los datos de r_offense_date ya que los mismos no cumplen el formato de actualidad
"""

"""
Estrategias de Mitigación
Para abordar los valores faltantes, podríamos considerar imputar los datos faltantes o eliminar 
las filas o columnas con una cantidad significativa de valores faltantes, según el impacto en el análisis.
Para garantizar la actualidad de los datos, podríamos verificar si las 
fechas de evaluación están dentro del período de tiempo relevante para el análisis y si hay información sobre cambios en 
las políticas o procedimientos de evaluación que puedan afectar la interpretación de los datos. """

""" 2.- ¿Son los campos “is_recid” e “is_violent_recid” en este conjunto de datos adecuados para evaluar la precisión de
las estimaciones de riesgo generadas por el sistema COMPAS? Si no es así, definir y calcular una feature que sí lo sea."""
# Creación de una nueva característica que represente la diferencia entre las puntuaciones de riesgo previstas por COMPAS y
# las observaciones reales de reincidencia. Esta nueva característica podría proporcionar información adicional sobre la precisión de las 
# estimaciones de riesgo. Por ejemplo, podríamos crear una columna llamada "diferencia_de_riesgo" que calcule la diferencia entre "compas_score" y "is_recid" o "is_violent_recid".
# Calcular la diferencia entre las puntuaciones de riesgo y la observación de reincidencia
compas_data['diferencia_de_riesgo'] = compas_data['is_violent_recid'] - compas_data['is_recid']

# Mostrar las primeras filas del DataFrame con la nueva columna
print(compas_data[['is_violent_recid', 'is_recid', 'diferencia_de_riesgo']].head())
"""R: La salida es la siguiente:
   is_violent_recid  is_recid  diferencia_de_riesgo
0                 0         0                     0
1                 0        -1                     1
2                 1         1                     0
3                 0         1                    -1
4                 0         0                     0 
 En esta nueva columna, un valor de 0 indica que ambos campos son iguales, un valor de 1 indica que "is_violent_recid" es mayor que "is_recid", y un valor de -1 indica lo contrario."""

""" 3 - El umbral para establecer medidas preventivas de la reincidencia es de 7 en adelante. Dado este umbral, generar una 
tabla de contingencia, explicando qué caso se considera como “positivo” (y, por lo tanto, cuáles son los errores de tipo I y los errores de tipo II). """

""" Respuesta:
Esta tabla de contingencia mostrará la cantidad de Verdaderos Positivos (VP), Falsos Positivos (FP),
Verdaderos Negativos (VN) y Falsos Negativos (FN) en función del umbral establecido en 7.
Los errores de Tipo I corresponden a los Falsos Positivos (FP), y los errores de Tipo II corresponden a los Falsos Negativos (FN)."""
# Definir el umbral
umbral = 7

# Crear una columna que indique si un individuo es positivo (puntuación >= umbral)
compas_data['es_positivo'] = np.where(compas_data['is_recid'] >= umbral, 1, 0)

# Crear una tabla de contingencia
tabla_contingencia = pd.crosstab(compas_data['es_positivo'], compas_data['is_recid'], margins=True,
                                  rownames=['Es Positivo'], colnames=['Reincidencia'])

# Mostrar la tabla de contingencia
print(tabla_contingencia)

""" R: La salida es la siguiente:
Reincidencia   -1     0     1    All
Es Positivo                         
0             719  7335  3703  11757
All           719  7335  3703  11757
Lo que indica el umbral de 7 parece ser bastante conservador en términos de clasificación, ya que hay 
relativamente pocos Falsos Positivos, lo que significa que no se etiqueta 
erróneamente a muchas personas como reincidentes cuando no lo son. Sin embargo, hay un número notable de Falsos Negativos, 
lo que indica que algunas personas que reinciden según sus puntuaciones de 
"is_recid" no son clasificadas como tal.
"""

""" 4 - El sistema asigna, de media, evaluaciones de riesgo más altas a los hombres que a las mujeres, y a las personas de raza afroamericana que a las de 
raza caucásica. Sin embargo, también las tasas de reincidencia son más altas para esos colectivos, aunque no está claro que la asignación de riesgo sea “justa” o no. 
Mostrar estas diferencias mediante representaciones gráficas y utilizarlas para analizar si la asignación de evaluaciones es justa o no."""

# Crear subconjuntos de datos para género y raza
data_gender = compas_data[['sex', 'is_recid']]
data_race = compas_data[['race', 'is_recid']]

# Gráfico de barras para comparar puntuaciones de riesgo por género
plt.figure(figsize=(10, 5))
sns.barplot(x='sex', y='is_recid', data=data_gender, ci=None)
plt.title('Comparación de Puntuaciones de Riesgo por Género')
plt.xlabel('Género')
plt.ylabel('Puntuación de Riesgo')
plt.show()

# Gráfico de barras para comparar puntuaciones de riesgo por raza
plt.figure(figsize=(10, 5))
sns.barplot(x='race', y='is_recid', data=data_race, ci=None)
plt.title('Comparación de Puntuaciones de Riesgo por Raza')
plt.xlabel('Raza')
plt.ylabel('Puntuación de Riesgo')
plt.xticks(rotation=45)
plt.show()

""" R: La salida se muestra en la Figure_1.PNG, donde se muestra reincidencia por género, y Figure_2.PNG, donde se muestra reincidencia por raza
Se concluye, tras esta representación y el análisis realizado en los apartados anteriores que aunque la evaluación no puede ser definitiva, ya que existen datos erróneos en cuanto a formato, según lo corroborado en apartados
anteriores, la evaluación es justa"""

"""
5 - ¿Para qué tipo de riesgos, el de delitos generales o el de delitos violentos, tiene el sistema más capacidad predictiva?
"""
# Crear subconjuntos de datos para delitos generales y delitos violentos
data_general_crime = compas_data[compas_data['is_violent_recid'] == 0]
data_violent_crime = compas_data[compas_data['is_violent_recid'] == 1]

# Calcular la correlación entre las puntuaciones de riesgo y las tasas de reincidencia reales
correlation_general_crime = data_general_crime['decile_score'].corr(data_general_crime['is_recid'])
correlation_violent_crime = data_violent_crime['v_decile_score'].corr(data_violent_crime['is_recid'])

# Crear gráficos de dispersión para visualizar la relación entre puntuaciones de riesgo y tasas de reincidencia
plt.figure(figsize=(12, 5))

# Gráfico para delitos generales
plt.subplot(1, 2, 1)
sns.scatterplot(x='decile_score', y='is_recid', data=data_general_crime)
plt.title('Relación entre Puntuaciones de Riesgo y Reincidencia (Delitos Generales)')
plt.xlabel('Puntuación de Riesgo')
plt.ylabel('Tasa de Reincidencia')

# Gráfico para delitos violentos
plt.subplot(1, 2, 2)
sns.scatterplot(x='v_decile_score', y='is_recid', data=data_violent_crime)
plt.title('Relación entre Puntuaciones de Riesgo y Reincidencia (Delitos Violentos)')
plt.xlabel('Puntuación de Riesgo')
plt.ylabel('Tasa de Reincidencia')

plt.tight_layout()
plt.show()

# Imprimir las correlaciones
print("Correlación para Delitos Generales:", correlation_general_crime)
print("Correlación para Delitos Violentos:", correlation_violent_crime)

"""" R: La salida se muestra en Figure_3.PNG"""
