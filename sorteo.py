import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from shapely.geometry import point
import geopandas as gpd
import pandas as pd
import random
import reverse_geocoder as rg
import pprint

def pcd_leer_mgn():
    fp = r"C:\Users\javie\Desktop\MGN2020_URB_AREA_CENSAL\MGN_URB_AREA_CENSAL.shp"
    data = gpd.read_file(fp)
    print(data.head())
    f= data.plot()

df = pd.read_excel(r"D:\Censo2018.xlsx", engine='openpyxl')

import reverse_geocoder as rg
import pprint

def sortear(df_f,puntos, ciudad, nse, j):
    npersonas = df_f[nse].cumsum()
    maximo = npersonas.tail(1)

    # Extrae las personas al azar
    persona = []
    for x in range(puntos):
        c = random.randint(1,  maximo.values[0])
        persona.append(c)

    k = 0
    # Halla la manzana donde esta la persona
    for x in persona:
        acumulado = 0 
        i = 0
        for z in df_f.iterrows():
            if acumulado >= persona[k]:            
                #print (z)  
                manzana = df_f['Manzana'].iloc[i]
                lat = df_f['LATITUD'].iloc[i]
                long = df_f['LONGITUD'].iloc[i]
                df_puntos.loc[j] = [ciudad, str(j) + " - " + nse, manzana , nse, lat, long]
                break        
            acumulado = acumulado + df_f[nse].iloc[i]
            i = i + 1
        j = j + 1
        k = k + 1
        print(j)

    
    
df_puntos = pd.DataFrame(columns=['Ciudad', 'Punto', 'Manzana', 'Estrato' , 'Latitud', 'Longitud'])    

nse1 = "Bajo"
nse2 = "Medio"
nse3 = "Alto"


# Filtro de Ciudad
#df_f =   df[(df.Ciudad== 'Bogota') | (df.Ciudad== 'Soacha')]
#puntos1 = 29
#puntos2 =19
#puntos3 = 4
#ciudad = "Bogota y Soacha"


#df_f =   df[(df.Ciudad== 'Medellin') | (df.Ciudad== 'Valle de Aburra')]
#puntos1 = 18
#puntos2 =12
#puntos3 = 10
#ciudad = "Medellin y Valle de Aburra"

#df_f =   df[(df.Ciudad== 'Cali')]
#puntos1 = 22
#puntos2 =12
#puntos3 = 7
#ciudad = "Cali"

#df_f =   df[(df.Ciudad== 'Barranquilla') | (df.Ciudad== 'Soledad')]
#puntos1 = 23
#puntos2 =8
#puntos3 = 9
#ciudad = "Barranquilla y Soledad"

#df_f =   df[(df.Ciudad== 'Bucaramanga') | (df.Ciudad== 'Floridablanca') | (df.Ciudad== 'Piedecuesta')]
#puntos1 = 8
#puntos2 =7
#puntos3 = 5
#ciudad = "Bucaramanga - Floridablanca - Piedecuesta"

#df_f =   df[(df.Ciudad== 'Cartagena')]
#puntos1 = 28
#puntos2 =9
#puntos3 = 4
#ciudad = "Cartagena"

#Selector de ciudades
def dfSelector(ciudad):
    if ciudad == "Bogota y Soacha":
        df_f = df[(df.Ciudad== 'Bogota') | (df.Ciudad== 'Soacha')]
    if ciudad == "Medellin y Valle de Aburra":
        df_f = df[(df.Ciudad== 'Medellin') | (df.Ciudad== 'Valle de Aburra')]
    if ciudad == "Barranquilla y Soledad":
        df_f = df[(df.Ciudad== 'Barranquilla') | (df.Ciudad== 'Soledad')]
    if ciudad == "Bucaramanga - Floridablanca - Piedecuesta":
        df_f = df[(df.Ciudad== 'Bucaramanga') | (df.Ciudad== 'Floridablanca') | (df.Ciudad== 'Piedecuesta')]
    if ciudad == "Cartagena":
        df_f = df[(df.Ciudad== 'Cartagena')]
    if ciudad == "Cali":
        df_f = df[(df.Ciudad== 'Cali')]
    if ciudad == "Pereira y Dosquebradas":
        df_f = df[(df.Ciudad== 'Pereira') | (df.Ciudad== 'Dosquebradas')]
    return df_f

#Establece los parametros del sorteo
def mainSorteo(ciudad,puntos1,puntos2,puntos3):
    df_f =   dfSelector(ciudad)
    ciudad = ciudad
    # Numero de puntos muestrales en el estrado
    j = 1
    sortear(df_f,puntos1,ciudad,nse1,j)

    j = j + puntos1
    sortear(df_f,puntos2,ciudad,nse2,j)

    j = j + puntos2
    sortear(df_f,puntos3,ciudad,nse3,j)
    
    df_puntos.to_csv('Puntos.csv',index = False)

