# Hamming Code Project: Comunicación I2C entre Arduinos Mega 2560.
## Proyecto para el curso de Comunicación de Datos de la Universidad de Lima.

### Requisitos Funcionales

1. A partir de una cadena de 7 de bits de datos ingresados en la PC1 mediante una interfaz gráfica en Python, al presionar el botón “Generar código Hamming”, se generará el código Hamming correspondiente.

2. Al mismo tiempo, el código Hamming generado se trasmite mediante comunicación serial desde Python a Arduino 1, el cual lo envía al Arduino
2, mediante comunicación I2C.

3. La secuencia de 11 bits, a ser trasmitida por Arduino 1 y la secuencia recibida por Arduino 2 mediante comunicación I2C se debe visualizar
mediante LEDS conectados a cada Arduino.

4. El código recibido en Arduino 2, se debe poder visualizar mediante una interfaz gráfica en Python en la PC 2.

5. En caso en Arduino 1, se altere “a propósito” un bit de datos del código generado en PC1, éste error debe ser detectado en el receptor y se debe indicar por pantalla en qué posición está el bit con error.

## Proyecto presentado con éxito el 04/07/23, clase de las 7-10pm.
