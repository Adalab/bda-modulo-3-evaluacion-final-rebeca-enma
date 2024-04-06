#%%
from src import soporte_evaluacion as sp
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


##⭐ EVALUACION PARTE 1 ⭐##
## 1--- Realizamos la apertura de los CSV y los convertimos en DF, le asignamos un nombre para poder localizarlos mas facilmente

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

# 2--- Realizamos la union de ambos DF, esta funcion tambien guarda una copia en CSV
df_merge = sp.union_datos(df_cust_activity,df_cust_history,"loyalty_number","loyalty_number","left")
df_merge.name = "Customer Actividad - Historial"
df_merge.head()

# Exploracion DF unido
# sp.exploracion_df(df_merge)

# 3 ----  Revisamos que hay 1864 filas duplicadas y procedemos a eliminarlas
# Decidimos eliminar las filas duplicadas, porque no aportan informacion de valor y pueden alterar los resultados

df_sin_duplicados = df_merge.drop_duplicates()
df_sin_duplicados.name = "Customer Actividad - Historial sin duplicados"
print(f"El número de filas que tenemos es {df_sin_duplicados.shape[0]}, y el número de columnas es {df_sin_duplicados.shape[1]}")
print(f"Nº Duplicados: {df_sin_duplicados.duplicated().sum()}")

#Exploracion DF sin duplicados
# sp.exploracion_df(df_sin_duplicados)

## Comprobamos los valores nulos en el DF y sacamos el % sobre el total
sp.comprobacion_valores_nulos(df_sin_duplicados)

      ## 📍 Decidimos no tratar los valores nulos en la columna "cancellation_year" y "cancellation_month" porque aportan informacion, ya que quiere decir que no se han cancelado, de estos datos podemos sacar que se han cancelado 12.3% de los vuelos.

df_salario1 = df_sin_duplicados.loc[df_sin_duplicados["salary"].isnull()]
df_salario1["education"].value_counts()

df_salario2 = df_sin_duplicados.loc[(df_sin_duplicados["salary"].notnull()) & (df_sin_duplicados["education"] == "College")]
df_salario2

sns.boxplot(x = "salary",
            y = "education", 
            data = df_sin_duplicados, 
            palette= "rainbow");


      ## 📍 En la columna SALARIO comprobamos que los valores nulos 102260 percetenen a los clientes con EDUCACION = College.
      # Decidimos no modificarlos ya que no podemos imputar media/moda o mediana porque desconocemos todos los datos de ese grupo, y tampoco utilizamos los metodos IterativeImputer o  KNNImputer, ya que aunque podriamos compararlos con otras categorias, no seria fiable por el mismo motivo que anteriormente hemos mencionado, no tenemos ningun referente con la misma educacion.
      

#%%
## EXPLORACION COLUMNAS
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
# ✔️ ENROLLMENT_TYPE - 2 Valores tipo str "Tipo de Inscripción" (Standard,Promotion ) - 
# SALARY -  ⚠️ CUIDADO NULOS, valores negativos
# ✔️ CANCELLATION_YEAR - Categorica/int - ⚠️ CUIDADO NULOS 
# ✔️ CANCELLATION_MONTH - Categorica/int - ⚠️ CUIDADO NULOS

#%%
## CAMBIOS COLUMNAS
   # Vamos a utilizar .loc[:]  para evitar el WARNING "SettingWithCopyWarning" para asegurarnos de modificar el DF original

lista_columnas = ["cancellation_year", "cancellation_month"]
for col in lista_columnas:
   df_sin_duplicados.loc[:,col]= df_sin_duplicados[col].apply(sp.cambio_int)
   
   # Sobre cada celda de la columna "enrollment_type" aplicamos la funcion anonima que devuelve la segunda palabra de la celda si tiene más de una palabra y no es igual a "Standard"

df_sin_duplicados.loc[:,"enrollment_type"] = df_sin_duplicados["enrollment_type"].apply(lambda celda: celda.split()[1] if len(celda.split()) > 1 and celda != "Standard" else celda)

# En la columna salario hay importes negativos, asumo que es un error de mecanografia y hacemos cambio a valores positivos
df_sin_duplicados.loc[:,"salary"] = df_sin_duplicados["salary"].apply(abs) # La funcion abs devuelve el valor absoluto


# lista_cambico_categoricas = ["year", "month"]

# for col in lista_cambico_categoricas:
#    df_sin_duplicados.loc[:,col]= df_sin_duplicados[col].apply(sp.cambio_categoricas)

# numeros_a_meses = {1: "January",2: "February",3: "March", 4: "April", 5: "May",6: "June",7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

# df_sin_duplicados.loc[:,"month"] = df_sin_duplicados["month"].map(numeros_a_meses)
   

#sp.exploracion_col_df(df_sin_duplicados)
#sp.exploracion_df(df_sin_duplicados)

col_categoricas, col_numericas = sp.clasificacion_columnas(df_sin_duplicados)

# %%
## 📊 Graficas y visualizaciones 
sp.exploracion_df(df_sin_duplicados)
sp.generar_graficas(df_sin_duplicados,col_categoricas,col_numericas)
sp.grafica_boxplot(df_sin_duplicados,col_numericas)

## Datos que hemos sacado de la exploracion visual:

# Columnas que deberiamos cambiar a categoricas
      # Year / Month / enrollment_year / enrollment_month


# En la grafica Boxplot podemos observar:
      # las columnas points_redeemed, dolllar_cost_points aportan poca informacion debido a la distribucion de sus valores

#df_sin_duplicados[df_sin_duplicados["salary"] <= 0].sort_values(by="salary")
#df_sin_duplicados[(df_sin_duplicados["salary"] >= 10000) & (df_sin_duplicados["salary"] <10000)].sort_values(by="salary")


# %%

##⭐ EVALUACION PARTE 2⭐##
#1️⃣ ¿Cómo se distribuye la cantidad de vuelos reservados por mes durante el año?

df_meses = df_sin_duplicados.sort_values("month")
numeros_a_meses = {1: "January",2: "February",3: "March", 4: "April", 5: "May",6: "June",7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
df_meses.loc[:,"month"] = df_meses["month"].map(numeros_a_meses)


sns.barplot(x="month", y = "flights_booked", data=df_meses, color="turquoise")
plt.xlabel("Vuelos Reservados")
plt.ylabel("Frecuencia")
plt.xticks(rotation = 45)
plt.title("Distribución de Vuelos Reservados por Mes")

         ## Podemos ver como los meses con el mayor numero de reservas corresponde con los meses de JULIO, JUNIO, AGOSTO y DICIEMBRE, podemos relacionarlo a los meses vacacionales.



#%%
#2️⃣ ¿Existe una relación entre la distancia de los vuelos y los puntos acumulados por los clientes?
sns.regplot(x = "points_accumulated", 
                y = "distance", 
                data = df_sin_duplicados,
                line_kws = {"color": "black", "linewidth": 1},
                color = "darkcyan")


plt.xlabel("Distancia")
plt.ylabel("Puntos clientes")
plt.title("Relación entre la distancia de los vuelos y los puntos acumulados'", fontsize = 10);


correlacion = df_sin_duplicados['distance'].corr(df_sin_duplicados['points_accumulated'], method="pearson")

print("Correlación de Pearson:", correlacion)        

         ## Podemos ver una correlacion positiva entre ambas variables, viendo como aumenta la distancia tambien aumentan los puntosde los clientes.


 #%%
 #3️⃣¿Cuál es la distribución de los clientes por provincia o estado?

fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (15,5))
axes=axes.flat


sns.barplot(x = "province",
            y = "loyalty_number",
            data = df_sin_duplicados,
            palette = "magma", 
            ax = axes[0]
            )

axes[0].set_title("Provincia")
axes[0].set_xlabel("Recuento")
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

sns.barplot(x = "country",
            y = "loyalty_number",
            data = df_sin_duplicados,
            palette = "magma", 
            ax = axes[1]
            )


axes[1].set_title("Estado")
axes[1].set_xlabel("Recuento")


plt.tight_layout()
        
# %%
#4️⃣ ¿Cómo se compara el salario promedio entre los diferentes niveles educativos de los clientes?
plt.figure(figsize=(10, 6))
sns.boxplot(x='education', 
            y='salary', 
            data = df_sin_duplicados
            , palette='twilight_shifted')

plt.title('Distribución de salario por nivel educativo')
plt.xlabel('Nivel educativo')
plt.ylabel('Salario')
plt.xticks(rotation=45);

            # Desconocemos los datos de salario para el segmento con educacion COLLEGE
            # En las demas categorias podemos visualmente podemos ver que los salarios ocupan rangos mas altos cuando el nivel de estudios es mayor, siendo el rango mas bajo ara instituto, seguido de bachillerato, posteriormente las personas con master y por ultimo la gente que ha cursado doctorados.



# %%
#5️⃣¿Cuál es la proporción de clientes con diferentes tipos de tarjetas de fidelidad?

df_tipo_tarjeta = df_sin_duplicados.groupby("loyalty_card")["loyalty_number"].count().reset_index()


colores = ["c", "cadetblue", "turquoise"]
explode = ( 0.1 ,0.1 , 0.) # para sacar los quesitos hacia fuera

plt.figure(figsize=(5,5))

plt.pie("loyalty_number", labels= "loyalty_card",
      data = df_tipo_tarjeta,
      colors = colores,
      textprops={'fontsize': 8},
      autopct=  '%1.1f%%',
      explode = explode)  

plt.title("Distribucion por tipo de tarjeta", color = "teal", fontsize = 16) 
plt.show();


#%%
#6️⃣¿Cómo se distribuyen los clientes según su estado civil y género?

plt.figure(figsize=(10, 6))
sns.countplot(x='marital_status', 
              hue='gender', 
              data=df_sin_duplicados, palette='Spectral')

plt.legend(title='Género')
plt.title('Distribución de clientes por estado civil y genero')
plt.xlabel('Estado civil')
plt.ylabel('Clientes')

df_estado_civil = df_sin_duplicados.groupby(["marital_status", "gender"])["loyalty_number"].count().reset_index(name="Recuento")
total_general = df_estado_civil['Recuento'].sum()
df_estado_civil['Porcentaje'] = round((df_estado_civil['Recuento'] / total_general) * 100, 2)
df_estado_civil


            # El mayor numero de personas se encuentran en el grupo "Casados" siendo ligeramente superior el numero de hombres que de mujeres,  seguido de solteros donde en este caso es levemente superior el numero de mujeres y finalmente divorciados donde tambien hay mas presencia de mujeres.


# %%
