from flask import Blueprint,render_template,render_template, redirect, url_for, request, flash
import os
from .sorteo import mainSorteo

synapsis = Blueprint('synapsis', __name__)

@synapsis.route('/puntos_muestrales')
def puntos_muestrales():
    #Pagina del formulario
    mensaje = ""
    return render_template('puntos_muestrales.html',mensaje = mensaje) 

@synapsis.route('/data', methods =['POST'])
def data():
    #Conversion de sql a dataframe
    
    
    #Pide los datos del formulario
    ciudad = request.form['ciudad']
    puntos1 = int(request.form['puntos1'])
    puntos2 = int(request.form['puntos2'])
    puntos3 = int(request.form['puntos3'])
    # Hace sorteo con los datos del formulario
    archivo1 = os.path.join(synapsis.root_path, 'static/Puntos.csv')
    archivo2 = os.path.join(synapsis.root_path, 'static/Puntos.xlsx')
    arreglo=mainSorteo(ciudad,puntos1,puntos2,puntos3,archivo1,archivo2)
    
    coordenadas = []
    for punto in arreglo:
       coordenadas.append([punto[4],punto[5],punto[3],punto[6]])
    mensaje = "Puntos de " + ciudad
    return render_template('puntos_muestrales.html',mensaje = mensaje,arreglo=arreglo,coordenadas=coordenadas)
@synapsis.route('/diferencias_significativas')
def diferencias_significativas():
    #Pagina del formulario
    mensaje = ""
    return render_template('diferencias_significativas.html',mensaje = mensaje)     

@synapsis.route('/diferenciasMedia')
def diferencias_significativasMedia():
    #Pagina del formulario
    mensaje = ""
    return render_template('DiferenciaMedias.html',mensaje = mensaje)   

