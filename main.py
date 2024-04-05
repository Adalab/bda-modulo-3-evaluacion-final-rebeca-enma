#%%
from src import soporte_evaluacion as sp
import pandas as pd 

## Realizamos la apertura de los CSV y los convertimos en DF, le asignamos un nombre para poder localizarlos mas facilmente
## lo hacemos mediante la funcion apertura_csv

df_cust_activity = sp.apertura_csv("files/customer_flight_activity.csv")
df_cust_activity.name = "Clientes Actividad"

df_cust_history = sp.apertura_csv("files/customer_loyalty_history.csv")
df_cust_history.name = "Clientes Historial"

## Cambiamos el nombre de las columnas
sp.cambio_nombre_columnas_df(df_cust_activity)
sp.cambio_nombre_columnas_df(df_cust_history)


#Imprimimos por pantalla las 5 primeras lineas de cada DF
# display(df_cust_activity.head(2))
# display(df_cust_history.head(2))

#Exploracion DF
# sp.exploracion_df(df_cust_activity)
# sp.exploracion_df(df_cust_history)

# Realizamos la union de ambos DF, esta funcion tambien guarda una copia en CSV
df_merge = sp.union_datos(df_cust_activity,df_cust_history,"loyalty_number","loyalty_number","left")
df_merge.name = "Customer Actividad - Historial"
df_merge.head()

#Exploracion DF unido
# sp.exploracion_df(df_merge)

#Revisamos que hay 1864 filas duplicadas y procedemos a eliminarlas
# Decidimos eliminar las filas duplicadas, porque no aportan informacion 
df_sin_duplicados = df_merge.drop_duplicates()
df_sin_duplicados.name = "Customer Actividad - Historial sin duplicados"
print(f"El número de filas que tenemos es {df_sin_duplicados.shape[0]}, y el número de columnas es {df_sin_duplicados.shape[1]}")
print(f"Nº Duplicados: {df_sin_duplicados.duplicated().sum()}")

#Exploracion DF sin duplicados
# sp.exploracion_df(df_sin_duplicados)

## Comprobamos los valores nulos en el DF y sacamos el % sobre el total

# sp.comprobacion_valores_nulos(df_sin_duplicados)

## 📍 Decidimos no tratar los valores nulos en la columna "cancellation_year" y "cancellation_month" porque aportan informacion, ya que quiere decir que no se han cancelado, de esta informacion podemos sacar que se han cancelado 12.3% de los vuelos.
#Exploracion columnas
#sp.exploracion_col_df(df_sin_duplicados)

## Documentacion columas 

## ✅ Columna que estan OK: 
# 'LOYALTY_NUMBER' - Nº fidelidad 
# 'YEAR' - Actualmente 2 valores (2017/2018)
# 'MONTH'
# "FLIGHTS_BOOKED" - Vuelos reservados
# "FLIGHTS_WITH_COMPANIONS" - Vuelos con Acompañantes (Escala del 0 al 11)
# 'TOTAL_FLIGHTS' - Vuelos totales  - 33 Valores
# "DISTANCE" -  
# "POINTS_ACCUMULATED" - 
# "POINTS_REDEEMED" - Puntos Canjeados 
# "DOLLAR_COST_POINTS_REDEEMED" - "Cuantificacion en dinero de los puntos canjeados"
# "COUNTRY"  1 unico valor CANADA (No aporta nada) 
# "PROVINCE" - Tipo str 
# "CITY" - Tipo STR 
# "POSTAL_CODE" - Alfanumerico - Tipo str 
# "GENDER" - 2 categorias Tipo str
# "EDUCATION" - 5 categorias Tipo str
# "MARITAL_STATUS" - 3 Categorias Tipo str
# "LOYALTY_CARD" - 3 Valores tipo str
# "CLV" - "Customer Lifetime Value" (beneficio neto de cada cliente.)
# "ENROLLMENT_YEAR" - Año de inscrpcion 
# "ENROLLMENT_MONTH" - Mes de inscripcion 

## Cambiar 
# ENROLLMENT_TYPE - 2 Valores tipo str "Tipo de Inscripción" (Standard,Promotion ) - 
# SALARY - Cambiar a INT, eliminar 0 ⚠️ CUIDADO NULOS
# CANCELLATION_YEAR - Cambiar a INT, eliminar 0 - ⚠️ CUIDADO NULOS
# CANCELLATION_MONTH - Cambiar a INT, eliminar 0 - ⚠️ CUIDADO NULOS


df_sin_duplicados.dtypes

lista_columnas = ["cancellation_year", "cancellation_month"]

for col in lista_columnas:
   df_sin_duplicados[col]= df_sin_duplicados[col].apply(sp.cambiar_numero)

# %%
df_sin_duplicados.dtypes
# df_sin_duplicados["nuva_columna_cancellation_year"].value_counts()
# %%
df_sin_duplicados.dtypes

# %%
