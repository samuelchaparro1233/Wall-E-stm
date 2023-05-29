import tkinter as tk
from PIL import ImageTk, Image
import time


def tablero(matrix):
    # Definir la matriz con los nombres de los archivos de las imágenes (sin la extensión)
    image_matrix = matrix

    # Extensión de archivo de las imágenes
    image_extension = '.png'
    ruta='wall-e/'

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Wall-E Recolector")

    # Crear una cuadrícula para las imágenes
    for i in range(5):
        for j in range(5):
            # Obtener el nombre del archivo de imagen de la matriz
            image_filename = ruta + str(image_matrix[i][j]) + image_extension

            # Cargar la imagen utilizando PIL (Python Imaging Library)
            image = Image.open(image_filename)
            # Redimensionar la imagen si es necesario
            image = image.resize((100, 100))  # Ajusta el tamaño según tus necesidades

            # Convertir la imagen en un objeto compatible con Tkinter
            tk_image = ImageTk.PhotoImage(image)

            # Crear una etiqueta para mostrar la imagen
            label = tk.Label(root, image=tk_image)
            label.image = tk_image  # Mantener una referencia para evitar que la imagen se elimine por el recolector de basura

            # Ubicar la etiqueta en la cuadrícula
            label.grid(row=i, column=j)
    
    root.after(3000, root.destroy)
    # Iniciar el bucle de eventos de la ventana principal
    root.mainloop()
    
