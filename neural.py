from flask import Blueprint,render_template,request
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np
import math

neural = Blueprint('neural', __name__)


datos, metadatos = tfds.load('fashion_mnist', as_supervised=True, with_info=True)

    #Obtenemos en variables separadas los datos de entrenamiento (60k) y pruebas (10k)
datos_entrenamiento, datos_pruebas = datos['train'], datos['test']
print(datos['test'])
    #Etiquetas de las 10 categorias posibles
nombres_clases = metadatos.features['label'].names


        #Funcion de normalizacion para los datos (Pasar de 0-255 a 0-1)
        #Hace que la red aprenda mejor y mas rapido
def normalizar(imagenes, etiquetas):
        imagenes = tf.cast(imagenes, tf.float32)
        imagenes /= 255 #Aqui lo pasa de 0-255 a 0-1
        return imagenes, etiquetas

    #Normalizar los datos de entrenamiento y pruebas con la funcion que hicimos
datos_entrenamiento = datos_entrenamiento.map(normalizar)
datos_pruebas = datos_pruebas.map(normalizar)

    #Agregar a cache (usar memoria en lugar de disco, entrenamiento mas rapido)
datos_entrenamiento = datos_entrenamiento.cache()
datos_pruebas = datos_pruebas.cache()





    #Crear el modelo
modelo = tf.keras.Sequential([
tf.keras.layers.Flatten(input_shape=(28,28)), #1 - blanco y negro
tf.keras.layers.Dense(70, activation=tf.nn.relu),
tf.keras.layers.Dense(70, activation=tf.nn.relu),
tf.keras.layers.Dense(10, activation=tf.nn.softmax) #Para redes de clasificacion
    ])

    #Compilar el modelo
modelo.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    #Los numeros de datos en entrenamiento y pruebas (60k y 10k)
num_ej_entrenamiento = metadatos.splits["train"].num_examples
num_ej_pruebas = metadatos.splits["test"].num_examples
plt.figure(figsize=(10,10))
for i, (imagen, etiqueta) in enumerate(datos_entrenamiento.take(25)):
  imagen = imagen.numpy().reshape((28,28))
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(imagen, cmap=plt.cm.binary)
  plt.xlabel(nombres_clases[etiqueta])
  plt.savefig('static/pruebas.png')

    #El trabajo por lotes permite que entrenamientos con gran cantidad de datos se haga de manera mas eficiente
TAMANO_LOTE = 64

    #Shuffle y repeat hacen que los datos esten mezclados de manera aleatoria para que la red
    #no se vaya a aprender el orden de las cosas
datos_entrenamiento = datos_entrenamiento.repeat().shuffle(num_ej_entrenamiento).batch(TAMANO_LOTE)
datos_pruebas = datos_pruebas.shuffle(num_ej_pruebas).batch(TAMANO_LOTE)
 

historial = modelo

@neural.route('/neural')
def neuralnet():
    #Entrenar
    historial = modelo.fit(datos_entrenamiento, epochs=7, steps_per_epoch= math.ceil(num_ej_entrenamiento/TAMANO_LOTE))

    for imagenes_prueba, etiquetas_prueba in datos_pruebas.take(1):
        imagenes_prueba = imagenes_prueba.numpy()
        etiquetas_prueba = etiquetas_prueba.numpy()
        predicciones = modelo.predict(imagenes_prueba)
    
    def graficar_imagen(i, arr_predicciones, etiquetas_reales, imagenes):
        arr_predicciones, etiqueta_real, img = arr_predicciones[i], etiquetas_reales[i], imagenes[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
    
        plt.imshow(img[...,0], cmap=plt.cm.binary)

        etiqueta_prediccion = np.argmax(arr_predicciones)
        if etiqueta_prediccion == etiqueta_real:
            color = 'blue'
        else:
            color = 'red'
    
        plt.xlabel("{} {:2.0f}% ({})".format(nombres_clases[etiqueta_prediccion],
                                        100*np.max(arr_predicciones),
                                        nombres_clases[etiqueta_real]),
                                        color=color)
    
    def graficar_valor_arreglo(i, arr_predicciones, etiqueta_real):
        arr_predicciones, etiqueta_real = arr_predicciones[i], etiqueta_real[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        grafica = plt.bar(range(10), arr_predicciones, color="#777777")
        plt.ylim([0, 1]) 
        etiqueta_prediccion = np.argmax(arr_predicciones)
        
        grafica[etiqueta_prediccion].set_color('red')
        grafica[etiqueta_real].set_color('blue')



    filas = 5
    columnas = 5
    num_imagenes = filas*columnas
    plt.figure(figsize=(2*2*columnas, 2*filas))
    for i in range(num_imagenes):
        plt.subplot(filas, 2*columnas, 2*i+1)
        graficar_imagen(i, predicciones, etiquetas_prueba, imagenes_prueba)
        plt.subplot(filas, 2*columnas, 2*i+2)
        graficar_valor_arreglo(i, predicciones, etiquetas_prueba)
        
    #Probar una imagen suelta
    imagen = imagenes_prueba[4] #AL ser la variable imagenes_prueba solo tiene lo que se le puso en el bloque anterior heheh
    imagen = np.array([imagen])
   
    prediccion = modelo.predict(imagen)
    plt.savefig('static/new_plot.png')
    print("Prediccion: " + nombres_clases[np.argmax(prediccion[0])])
    return render_template("neural.html")


from PIL import Image
from io import BytesIO
import cv2


def input_prepare(img):
    img = np.asarray(img)              # convert to array 
    img = cv2.resize(img, (28, 28 ))   # resize to target shape 
    img = cv2.bitwise_not(img)         # [optional] my input was white bg, I turned it to black - {bitwise_not} turns 1's into 0's and 0's into 1's
    img = img / 255                    # normalize 
    
    img = img.reshape(1, 28, 28)          # reshaping 
    return img 


def makeOutro(imgplt,prediccion,porcentaje):
        plt.figure()
        plt.imshow(imgplt, cmap=plt.cm.binary)
        plt.colorbar()
        plt.grid(False)
      

        etiqueta_prediccion = np.argmax(prediccion)
        
        plt.xlabel(str(nombres_clases[etiqueta_prediccion]) + " " + "{:.2f}".format(porcentaje) + "%" )
        plt.savefig('static/outro.png')


@neural.route('/neural', methods =['POST'])
def neuralImage():
    try:
        # check if the post request has the file part
        file = request.files['myImage']
        file = file.read()
        img = Image.open(BytesIO(file))
        imgplt = np.array(img.resize((28, 28 ), Image.ANTIALIAS))
        plt.figure()
        plt.imshow(imgplt, cmap=plt.cm.binary)
        plt.colorbar()
        plt.grid(False)
        plt.savefig('static/intro.png')
        
   
        img = img.convert("L")
        img = input_prepare(img)
       
     
        prediccion = modelo.predict(img)
        porcentaje = 100*np.max(prediccion)
        makeOutro(imgplt,prediccion,porcentaje)
        print(prediccion)
        
        print("Prediccion: " + nombres_clases[np.argmax(prediccion[0])])
        return render_template("neuralimage.html")
       
    except Exception as err:
        print("Error occurred")
        print(err)
        return("Error, image not received.")
