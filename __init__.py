from flask import Flask,request,render_template
import pandas as pd
import os
from sorteo import mainSorteo
from sorteo import db
app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/app"
db.init_app(app)


@app.route('/')
def form():
    #Pagina del formulario
    mensaje = ""
    return render_template('Form.html',mensaje = mensaje)

@app.route('/data', methods =['POST'])

def data():
    #Conversion de sql a dataframe
    
    
    #Pide los datos del formulario
    ciudad = request.form['ciudad']
    puntos1 = int(request.form['puntos1'])
    puntos2 = int(request.form['puntos2'])
    puntos3 = int(request.form['puntos3'])
    # Hace sorteo con los datos del formulario
    archivo1 = os.path.join(app.root_path, 'static/Puntos.csv')
    archivo2 = os.path.join(app.root_path, 'static/Puntos.xlsx')
    arreglo=mainSorteo(ciudad,puntos1,puntos2,puntos3,archivo1,archivo2)
    
    coordenadas = []
    for punto in arreglo:
       coordenadas.append([punto[4],punto[5],punto[3],punto[6]])
    mensaje = "Puntos de " + ciudad
    return render_template('Form.html',mensaje = mensaje,arreglo=arreglo,coordenadas=coordenadas)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
