import tkinter as tk

def mover_adelante():
    # Lógica para mover el carrito hacia adelante
    print("Moviendo hacia adelante")

def mover_atras():
    # Lógica para mover el carrito hacia atrás
    print("Moviendo hacia atrás")

def girar_izquierda():
    # Lógica para girar el carrito a la izquierda
    print("Girando a la izquierda")

def girar_derecha():
    # Lógica para girar el carrito a la derecha
    print("Girando a la derecha")

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Carrito de Robot")

# Crear botones para controlar el carrito
btn_adelante = tk.Button(root, text="Adelante", command=mover_adelante)
btn_adelante.pack()

btn_atras = tk.Button(root, text="Atrás", command=mover_atras)
btn_atras.pack()

btn_izquierda = tk.Button(root, text="Izquierda", command=girar_izquierda)
btn_izquierda.pack()

btn_derecha = tk.Button(root, text="Derecha", command=girar_derecha)
btn_derecha.pack()

# Ejecutar la aplicación
root.mainloop()
