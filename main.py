from flask import Flask,request,render_template
from sorteo import mainSorteo

app = Flask(__name__)

@app.route('/')
def form():
    #Pagina del formulario
    mensaje = ""
    return render_template('Form.html',mensaje = mensaje)

@app.route('/data', methods =['POST'])
def data():
    #Pide los datos del formulario
    ciudad = request.form['ciudad']
    puntos1 = int(request.form['puntos1'])
    puntos2 = int(request.form['puntos2'])
    puntos3 = int(request.form['puntos3'])
    # Hace sorteo con los datos del formulario
    
    arreglo=mainSorteo(ciudad,puntos1,puntos2,puntos3)
    mensaje = "Sorteo exitoso"
    return render_template('Form.html',mensaje = mensaje,arreglo=arreglo)

app.run(debug= True)