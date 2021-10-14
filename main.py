from flask import Flask,request,render_template
from sorteo import mainSorteo

app = Flask(__name__, static_url_path = '/static')

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
    coordenadas = []
    for punto in arreglo:
        coordenadas.append([punto[4],punto[5],punto[3],punto[6]])
    mensaje = "Puntos de " + ciudad
    return render_template('Form.html',mensaje = mensaje,arreglo=arreglo,coordenadas=coordenadas)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)