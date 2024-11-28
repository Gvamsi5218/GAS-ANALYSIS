import serial
import time

def read_sensor_data():
    # Connect to the Arduino serial port (replace 'COM3' with the correct port)
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Allow time for connection

    ser.write(b"R")  # Command to request sensor data
    line = ser.readline().decode().strip()
    ser.close()

    if line:
        try:
            # Assume data in the format: ammonia,phosphorus,temperature,humidity
            ammonia, phosphorus, temperature, humidity = map(float, line.split(","))
            return {"ammonia": ammonia, "phosphorus": phosphorus, "temperature": temperature, "humidity": humidity}
        except ValueError:
            print("Failed to parse sensor data")
            return None
    return None
