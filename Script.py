import serial
import sqlite3
from datetime import datetime

# Configuración del puerto serie
puerto_serial = '/dev/ttyUSB0'  # Cambia esto según tu sistema
baud_rate = 9600

# Conectar al puerto serie
ser = serial.Serial(puerto_serial, baud_rate, timeout=1)

# Conectar a la base de datos SQLite
conn = sqlite3.connect('sensores.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS mediciones (
        id_medicion INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_sensor INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

while True:
    try:
        # Leer datos del puerto serie
        if ser.in_waiting > 0:
            valor_sensor = ser.readline().decode().strip()
            
            if valor_sensor.isdigit():
                # Obtener el timestamp actual
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Insertar datos en la base de datos con timestamp
                c.execute('''
                    INSERT INTO mediciones (valor_sensor, timestamp)
                    VALUES (?, ?)
                ''', (int(valor_sensor), timestamp))
                
                # Confirmar los cambios
                conn.commit()
                print(f"Datos almacenados: Valor: {valor_sensor}, Timestamp: {timestamp}")
    
    except KeyboardInterrupt:
        print("Interrupción del teclado. Cerrando...")
        break

# Cerrar conexiones
ser.close()
conn.close() 