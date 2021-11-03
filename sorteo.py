from flask.scaffold import F
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from shapely.geometry import point
import pandas as pd
import random
import reverse_geocoder as rg
from sqlalchemy import or_
from .models import db,puntosModel






def sortear(df_f,df_puntos,puntos, ciudad, nse, j):
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
                manzana = df_f['manzana'].iloc[i]
                lat = df_f['latitud'].iloc[i]
                long = df_f['longitud'].iloc[i]
                df_puntos.loc[j] = [ciudad, str(j) + " - " + nse, manzana , nse, lat, long]
                break        
            acumulado = acumulado + df_f[nse].iloc[i]
            i = i + 1
        j = j + 1
        k = k + 1
        print(j)

    
    
   

nse1 = "bajo"
nse2 = "medio"
nse3 = "alto"




def querySelector(ciudad):
    if ciudad == "Bogota y Soacha":
       query = db.session.query(puntosModel).filter(or_(puntosModel.ciudad == "Bogota",puntosModel.ciudad == "Soacha")).statement
    if ciudad == "Medellin y Valle de Aburra":
        query = db.session.query(puntosModel).filter(or_(puntosModel.ciudad == "Medellin",puntosModel.ciudad == "Valle de Aburra")).statement
    if ciudad == "Barranquilla y Soledad":
       query =db.session.query(puntosModel).filter(or_(puntosModel.ciudad == "Barranquilla",puntosModel.ciudad == "Soledad")).statement
    if ciudad == "Bucaramanga - Floridablanca - Piedecuesta":
        query =db.session.query(puntosModel).filter(or_(puntosModel.ciudad == "Bucaramanga",puntosModel.ciudad == "Floridablanca",puntosModel.ciudad == "Piedecuesta")).statement
    if ciudad == "Cartagena":
        query =db.session.query(puntosModel).filter(puntosModel.ciudad == "Cartagena").statement
    if ciudad == "Cali":
        query = db.session.query(puntosModel).filter(puntosModel.ciudad == "Cali").statement
    if ciudad == "Pereira y Dosquebradas":
       query = db.session.query(puntosModel).filter(or_(puntosModel.ciudad == "Pereira",puntosModel.ciudad == "Dosquebradas")).statement
    return query

#Establece los parametros del sorteo
def mainSorteo(ciudad,puntos1,puntos2,puntos3,archivo1,archivo2):
     
    # Hace la query en la base de datos filtrando por ciudad
    df = pd.read_sql(querySelector(ciudad), db.session.bind)
    df_puntos = pd.DataFrame(columns=['ciudad', 'Punto', 'Manzana', 'Estrato' , 'Latitud', 'Longitud']) 
    
    ciudad = ciudad
    # Numero de puntos muestrales en el estrado
    j = 1
    sortear(df,df_puntos,puntos1,ciudad,nse1,j)

    j = j + puntos1
    sortear(df,df_puntos,puntos2,ciudad,nse2,j)

    j = j + puntos2
    sortear(df,df_puntos,puntos3,ciudad,nse3,j)
    
    df_puntos.to_csv(archivo1,index = False)
    df_puntos.to_excel(archivo2,index = False)
    dt = df_puntos.to_numpy()
    arreglo = []
    for index,row in enumerate(dt):
        a = row[0]
        b = row[1]
        c = row[2]
        d = row[3]
        e = row[4] 
        f = row[5]
        g = index + 1
        r = [a,b,c,d,e,f,g]
        arreglo.append(r)
    else:
        df_puntos = df_puntos.iloc[0:0]
    return arreglo
 