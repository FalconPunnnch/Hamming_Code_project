#include <Wire.h>

// Definir los pines de los LEDs
const int LED1_PIN = 2;
const int LED2_PIN = 3;
const int LED3_PIN = 4;
const int LED4_PIN = 5;
const int LED5_PIN = 6;
const int LED6_PIN = 7;
const int LED7_PIN = 8;
const int LED8_PIN = 9;
const int LED9_PIN = 10;
const int LED10_PIN = 11;
const int LED11_PIN = 12;

void setup() {
  // Configurar los pines de los LEDs como salidas
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(LED4_PIN, OUTPUT);
  pinMode(LED5_PIN, OUTPUT);
  pinMode(LED6_PIN, OUTPUT);
  pinMode(LED7_PIN, OUTPUT);
  pinMode(LED8_PIN, OUTPUT);
  pinMode(LED9_PIN, OUTPUT);
  pinMode(LED10_PIN, OUTPUT);
  pinMode(LED11_PIN, OUTPUT);

  // Inicializar el puerto serie
  Serial.begin(9600);
  Serial1.begin(9600); // Conexión con el Esclavo
  Wire.begin();        // Inicializar la comunicación I2C como maestro
}

void loop() {
  // Leer el código Hamming enviado desde Python
  if (Serial.available()) {
    String hamming_code = Serial.readStringUntil('\n');

    // Identificación de Esclavo
    id_esclavo();

    // Rutina de limpieza del buffer del puerto serial
    while (Serial.available() > 0) {
      Serial.read();
    }

    // Enviar mediante I2C al Esclavo
    Wire.beginTransmission(8);
    Wire.write(hamming_code.c_str());
    Wire.endTransmission();

    // Decodificar el código Hamming
    int decoded_data = 0;
    for (int i = 0; i < hamming_code.length(); i++) {
      decoded_data |= (hamming_code.charAt(i) - '0') << i;
    }

    // Imprimir el valor decodificado
    Serial.println(decoded_data);

    // Encender los LEDs según el código decodificado
    digitalWrite(LED1_PIN, (decoded_data & 1) ? HIGH : LOW);
    digitalWrite(LED2_PIN, (decoded_data & 2) ? HIGH : LOW);
    digitalWrite(LED3_PIN, (decoded_data & 4) ? HIGH : LOW);
    digitalWrite(LED4_PIN, (decoded_data & 8) ? HIGH : LOW);
    digitalWrite(LED5_PIN, (decoded_data & 16) ? HIGH : LOW);
    digitalWrite(LED6_PIN, (decoded_data & 32) ? HIGH : LOW);
    digitalWrite(LED7_PIN, (decoded_data & 64) ? HIGH : LOW);
    digitalWrite(LED8_PIN, (decoded_data & 128) ? HIGH : LOW);
    digitalWrite(LED9_PIN, (decoded_data & 256) ? HIGH : LOW);
    digitalWrite(LED10_PIN, (decoded_data & 512) ? HIGH : LOW);
    digitalWrite(LED11_PIN, (decoded_data & 1024) ? HIGH : LOW);
  }
}

void id_esclavo() {
  while (Serial1.peek() == 'a') {  // Discriminación de la letra como diferenciador del esclavo
    Serial.println("Espere...");    // Mensaje de espera por datos de verificación
    Serial1.write('a');             // Redireccionamiento del mensaje al Esclavo 1
    break;
  }
}