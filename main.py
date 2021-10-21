from flask import Flask,request,render_template
from sorteo import mainSorteo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd

app = Flask(__name__, static_url_path = '/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/app"
db= SQLAlchemy(app)
migrate = Migrate(app, db)

class puntosModel(db.Model):
    __tablename__ = 'Puntos'

    manzana = db.Column(db.String, primary_key=True)
    ciudad = db.Column(db.String())
    personas = db.Column(db.String())
    latitud = db.Column(db.Numeric())
    longitud = db.Column(db.Numeric())
    bajo = db.Column(db.Integer())
    medio = db.Column(db.Integer())
    alto = db.Column(db.Integer())

    def __init__(self,manzana, ciudad, personas):
        self.manzana = manzana
        self.ciudad = ciudad
        self.personas = personas

    def __repr__(self):
        return f"<Manzana {self.manzana}>"

@app.route('/')
def form():
    #Pagina del formulario
    mensaje = ""
    return render_template('Form.html',mensaje = mensaje)

@app.route('/data', methods =['POST'])

def data():
    #Conversion de sql a dataframe
    data = puntosModel.__tablename__
    datapuntos = pd.read_sql_table(data,db.session.bind)
    
    #Pide los datos del formulario
    ciudad = request.form['ciudad']
    puntos1 = int(request.form['puntos1'])
    puntos2 = int(request.form['puntos2'])
    puntos3 = int(request.form['puntos3'])
    # Hace sorteo con los datos del formulario
    
    arreglo=mainSorteo(datapuntos,ciudad,puntos1,puntos2,puntos3)
    
    coordenadas = []
    for punto in arreglo:
       coordenadas.append([punto[4],punto[5],punto[3],punto[6]])
    mensaje = "Puntos de " + ciudad
    return render_template('Form.html',mensaje = mensaje,arreglo=arreglo,coordenadas=coordenadas)
    return 'ehh'

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
