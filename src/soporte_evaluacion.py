#%%

# Importaciones necesarias
import pandas as pd 
import numpy as np
from word2number import w2n
import re 

# Imputación de nulos usando métodos avanzados estadísticos
# -----------------------------------------------------------------------
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Librerías de visualización
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames


# %%


def apertura_csv(ruta, quitar_primera_columna=False):
    """Funcion creada para la apertura de un CSV a traves de metodos de Pandas, 
    recibira como 1ª argumento la ruta y 2º (opcional) si queremos cambiar el indice """
    
    if quitar_primera_columna:
        df = pd.read_csv(ruta, index_col=0)
    else:    
        df = pd.read_csv(ruta)
    return df


def cambio_nombre_columnas_df(dataframe):
    """Con esta funcion podemos cambiar el nombre de las columnas de un DF, 
    recibimos un mensaje de confrimacion con el nombre del DF y el nuevo nombre de las columnas
    MODIFICA EL DF """

    dataframe.columns = [col.lower().strip().replace(" ","_") for col in dataframe.columns]
    print(f"Se ha cambiado el nombre en las columnas del DF {dataframe.name}, actualmente son:\n{dataframe.columns}\n")



def exploracion_df(df):

    """función diseñada para proporcionar un resumen detallado de un DF
    Nombre del DataFrame: Se imprime 
    Información Básica del DataFrame: Se muestra información los tipos de datos de cada columna y la cantidad de valores no nulos.
    Recuento de Filas y Columnas: Se imprime .
    Valores Nulos: Se presenta la cantidad de valores nulos en cada columna
    Valores Duplicados: Se indica la cantidad de filas duplicadas en el DF
    Estadísticas Descriptivas para Columnas Numéricas
    Estadísticas Descriptivas para Columnas Categóricas """

    print(f"La informacion del DF : _______ {df.name}: ______\n")
    df.info()
    print("__________________________________")


    print(f"El número de filas que tenemos es {df.shape[0]}, y el número de columnas es {df.shape[1]}\n")
    print("__________________________________")

    print(f"El DF {df.name} tiene nulos: \n")
    display(df.isnull().sum())
    print("__________________________________")

    print(f"El DF {df.name} tiene duplicados: {df.duplicated().sum()} \n")
    print("__________________________________")
    try:
        print(f"Datos estadisticos del DF {df.name} columnas numericas: \n")
        display(df.describe().T)
        print("__________________________________")

    except:
        print("No hay columnas de tipo numerico con datos en el DataFrame.")

    try:

        print(f"Datos estadisticos del DF {df.name} columnas categoricas: \n")
        display(df.describe(include = "object").T)
        print("__________________________________")

    except:
        print("No hay columnas de tipo objeto con datos en el DataFrame.")




def exploracion_col_df(df):
    """ Funcion diseñada para realizar una exploración detallada de las columnas de un DF
        Nombre de la Columna
        Número de Datos: Total de datos en la columna.
        Frecuencia de Valores: frecuencia de cada valor en la columna.
        Cantidad de Valores Únicos: Se indica cuántos valores únicos hay en la columna.
        Tipo de Datos: Se muestra el tipo de datos de la columna.
        Valores Nulos: Se imprime la cantidad de valores nulos en la columna.
        Valores Duplicados: Se indica la cantidad de valores duplicados en la columna.
    
    """

    print(f" _______ {df.name}: ______\n")
    for columna in df.columns:

        print(f" \n----------- ESTAMOS ANALIZANDO LA COLUMNA: '{columna.upper()}' -----------\n")
        print(f"* Nº de datos: {len(df[columna].to_list())}\n")
        print(f"* Frecuencia de valores en la columna: \n {df[columna].value_counts()}\n")
        print(f"* Datos unicos en la columna {len(df[columna].unique())}\n")
        print(f"* Los valores son de tipo: {df[columna].dtypes}\n")
        print(f"La suma de datos nulos {df[columna].isnull().sum()}\n")
        print(f"La suma de datos duplicados {df[columna].duplicated().sum()}\n")
        # print(df[columna].unique()) 



def union_datos(df1, df2, col_union_left, col_union_right, tipo_union = "left"):
    """Realiza una unión entre dos DataFrames y guarda el resultado en un archivo CSV.

    Parámetros:
    - df1: DataFrame izquierdo.
    - df2: DataFrame derecho.
    - col_union_left: Nombre de la columna en el DataFrame izquierdo para la unión.
    - col_union_right: Nombre de la columna en el DataFrame derecho para la unión.
    - tipo_union: Tipo de unión a realizar (por defecto es "left")"""

    df_mergeado = df1.merge(df2, left_on = col_union_left , right_on = col_union_right , how = tipo_union)
    df_mergeado.to_csv('files/csv_merged.csv')

    return df_mergeado

def comprobacion_valores_nulos(df):
    """Tomamos un DF como entrada, y revisamos el % de Nulos por columna
        Filtramos para mostrar el % de nulos en las columnas que los contengan"""
    
    # calculamos el % de nulos por columna
    df_nulos = pd.DataFrame((df.isnull().sum() / df.shape[0]) * 100, columns = ["%_nulos"])
    # filtramos el DataFrame para quedarnos solo con aquellas columnas que tengan nulos
    
    return df_nulos[df_nulos["%_nulos"] > 0]


def cambio_int(celda):
    try:
        print(celda.astype(int))
        return celda.astype(int)

    except:
        return np.nan



# %%
