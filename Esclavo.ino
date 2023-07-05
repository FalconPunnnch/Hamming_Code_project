#include <Wire.h>

void setup() {
  Wire.begin(8);                // Inicializar la comunicación I2C como esclavo con dirección 8
  Wire.onReceive(receiveEvent); // Configurar la función para manejar los datos recibidos
  for (int i = 2; i <= 12; i++) {
    pinMode(i, OUTPUT); // Configurar los pines del 2 al 12 como salidas
  }
  Serial.begin(9600);
}

void loop() {
  // No es necesario hacer nada en el bucle principal del esclavo
}

void receiveEvent(int bytes) {
  char data[bytes];

  for (int i = 0; i < bytes; i++) {
    if (Wire.available()) {
      data[i] = Wire.read(); // Leer los datos recibidos del maestro
    }
  }

  String hamming_code = "";

  for (int i = 0; i < bytes; i++) {
    hamming_code += data[i];
  }

  Serial.println(hamming_code); // Imprimir el código Hamming recibido por el esclavo

  // Mostrar el código Hamming recibido en los LEDs del 2 al 12
  for (int i = 0; i < hamming_code.length(); i++) {
    digitalWrite(i + 2, hamming_code[i] - '0');
  }
}