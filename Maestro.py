import serial
import time
import tkinter
from tkinter import *
from tkinter import ttk

# Definir Arduino1 (maestro que recibe datos desde Python para luego enviarlos al esclavo).
arduino1 = serial.Serial('COM14', 9600)

class Hamming1:
    def __init__(self, root):
        self.wind = root
        self.wind.title('Cliente')
        self.wind.geometry('450x400')
        self.wind.config(bg='teal')

        frame1 = LabelFrame(self.wind, text="Código a Ingresar", font=("times new roman", 14))
        frame2 = LabelFrame(self.wind, text="Código Hamming", font=("times new roman", 14))

        frame1.pack(fill="both", expand="yes", padx=10, pady=10)
        frame2.pack(fill="both", expand="yes", padx=10, pady=10)

        lbl2 = Label(frame1, text=" ", width=20)
        lbl2.grid(row=0, column=0, padx=5, pady=3)

        lbl1 = Label(frame1, text="Código de 7 dígitos: ", width=20)
        lbl1.grid(row=1, column=0, padx=5, pady=3)
        self.ent1 = Entry(frame1)
        self.ent1.grid(row=1, column=1, padx=5, pady=10)

        lbl2 = Label(frame1, text=" ", width=20)
        lbl2.grid(row=2, column=0, padx=5, pady=3)

        btn1 = Button(frame1, text="Procesar", width=12, height=2, command=self.generate_hamming_code)
        btn1.grid(row=3, column=1, padx=10, pady=10)

        self.trv = ttk.Treeview(frame2, columns=(1), show="headings", height="5")
        self.trv.pack()

        self.trv.heading(1, text="Código Generado")

    def generate_hamming_code(self):
        # Obtener la cadena de bits ingresada
        data_bits = self.ent1.get()

        # Verificar que se ingresaron exactamente 7 bits
        if len(data_bits) != 7:
            self.trv.delete(*self.trv.get_children())
            self.trv.insert('', 'end', values=("Error: La cadena debe tener 7 bits",))

        else:
           # Calcular los bits de paridad
            p1 = int(data_bits[0]) ^ int(data_bits[1]) ^ int(data_bits[3]) ^ int(data_bits[4]) ^ int(data_bits[6])
            p2 = int(data_bits[0]) ^ int(data_bits[2]) ^ int(data_bits[3]) ^ int(data_bits[5]) ^ int(data_bits[6])
            p4 = int(data_bits[1]) ^ int(data_bits[2]) ^ int(data_bits[4]) ^ int(data_bits[5]) ^ int(data_bits[6])
            p8 = int(data_bits[3]) ^ int(data_bits[4]) ^ int(data_bits[5]) ^ int(data_bits[6])


            # Construir el código Hamming
            hamming_code = str(p1) + str(p2) + data_bits[0] + str(p4) + data_bits[1:4] + str(p8) + data_bits[4:]

            # Mostrar el código Hamming generado
            self.trv.delete(*self.trv.get_children())
            self.trv.insert('', 'end', values=(hamming_code))

            # Enviar el código Hamming a Arduino2 (Esclavo)
            arduino1.write(hamming_code.encode())

            # Cerrar el puerto serie
            arduino1.close()

# Crear la ventana principal
window = Tk()
app = Hamming1(window)
window.mainloop()