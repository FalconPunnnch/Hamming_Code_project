import serial
import time
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Definir Arduino2 (Esclavo que recibe datos de Arduino1 y los procesa mediante la interfaz de Python):
arduino2 = serial.Serial('COM12', baudrate=9600, timeout=1.0)

class Hamming2:
    def __init__(self, root):
        self.wind = root
        self.wind.title('Cliente')
        self.wind.geometry('440x230')
        self.wind.config(bg='teal')

        frame1 = LabelFrame(self.wind, text="Código Hamming!", font=("times new roman", 14))

        frame1.pack(fill="both", expand="yes", padx=10, pady=10)

        lbl2 = Label(frame1, text=" ", width=20)
        lbl2.grid(row=0, column=0, padx=5, pady=3)

        lbl1 = Label(frame1, text="Hamming recibido: ", width=20)
        lbl1.grid(row=1, column=0, padx=5, pady=3)
        self.ent1 = Entry(frame1)
        self.ent1.grid(row=1, column=1, padx=5, pady=10)

        lbl2 = Label(frame1, text=" ", width=20)
        lbl2.grid(row=2, column=0, padx=5, pady=3)

        btn1 = Button(frame1, text="Recibir", width=12, height=2, command=self.receive_hamming_code)
        btn1.grid(row=3, column=1, padx=10, pady=10)

    def receive_hamming_code(self):
        # Esperar a recibir datos desde Arduino1 (Maestro)
        while True:
            if arduino2.in_waiting > 0:
                data = arduino2.readline().decode().rstrip()

                # Obtener el código Hamming recibido
                hamming_code = data

                # Mostrar el código Hamming recibido
                self.ent1.delete(0, END)
                self.ent1.insert(0, hamming_code)

                # Calcular los bits de paridad
                p1 = int(hamming_code[0]) ^ int(hamming_code[2]) ^ int(hamming_code[4]) ^ int(hamming_code[6])
                p2 = int(hamming_code[1]) ^ int(hamming_code[2]) ^ int(hamming_code[5]) ^ int(hamming_code[6])
                p4 = int(hamming_code[3]) ^ int(hamming_code[4]) ^ int(hamming_code[5]) ^ int(hamming_code[6])

                # Forzar error en bit de paridad determinado
                bit_recibido = 0  # Valor recibido, puede ser 0 o 1

                if bit_recibido == 0:
                    # Cambiar 0 por 1 en la posición p4
                    hamming_code = hamming_code[:4] + '1' + hamming_code[5:]
                else:
                    # Cambiar 1 por 0 en la posición p4
                    hamming_code = hamming_code[:4] + '0' + hamming_code[5:]

                # Verificar si hay errores
                error_detected = []

                if p1 != 0:
                    error_detected.append(1)
                if p2 != 0:
                    error_detected.append(2)
                if p4 != 0:
                    error_detected.append(4)

                # Mostrar mensaje de error si se detectó un error en los bits de paridad
                if error_detected:
                    error_message = "Se detectaron errores en los bits de paridad: "
                    for error_bit in error_detected:
                        error_message += str(error_bit) + ", "
                    error_message = error_message[:-2]  # Eliminar la coma y el espacio al final
                    messagebox.showerror("Error", error_message)

                # Enviar confirmación de recepción a Arduino1
                arduino2.write('OK'.encode())

                # Salir del bucle
                break

# Crear la ventana principal
window = Tk()
app = Hamming2(window)
window.mainloop()