import serial
import time
from datetime import datetime

# Configure serial connection
arduino = serial.Serial(port='COMX', baudrate=9600, timeout=1)  # Replace 'COMX' with your Arduino's port

def send_command(command):
    """
    Send a command to Arduino and return its response.
    """
    arduino.write(f"{command}\n".encode())  # Send command as bytes
    time.sleep(1)
    if arduino.in_waiting > 0:
        return arduino.readline().decode('utf-8').strip()
    return None

def control_servo_by_time():
    """
    Determine servo position based on the current time and send the command to Arduino.
    """
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        response = send_command("SERVO 45")
        print("Servo set to 45° for morning. Message: Take morning tablets.")
        lcd_message("Morning: Take tablets")
    elif 12 <= current_hour < 18:
        response = send_command("SERVO 90")
        print("Servo set to 90° for afternoon. Message: Take afternoon tablets.")
        lcd_message("Afternoon: Take tablets")
    else:
        response = send_command("SERVO 180")
        print("Servo set to 180° for evening. Message: Take evening tablets.")
        lcd_message("Evening: Take tablets")

def lcd_message(message):
    """
    Send a message to be displayed on the LCD via Arduino.
    """
    send_command(f"LCD {message}")

def check_temperature():
    """
    Request temperature data from Arduino and determine if there is a fever.
    """
    response = send_command("TEMP")
    if response:
        try:
            temp = float(response)  # Convert response to float
            print(f"Current temperature: {temp}°C")
            if temp > 38.0:
                send_command("BUZZER ON")
                lcd_message("Alert! Fever detected")
                print("Alert! High temperature detected.")
            else:
                send_command("BUZZER OFF")
                lcd_message("Normal temperature")
                print("Temperature is normal.")
        except ValueError:
            print(f"Error: Non-numeric response received: {response}")
    else:
        print("No temperature data received.")

def main():
    """
    Main program logic.
    """
    try:
        while True:
            # Check temperature and control servo
            check_temperature()
            control_servo_by_time()

            # Wait 10 seconds before repeating
            time.sleep(10)

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        send_command("BUZZER OFF")
        send_command("SERVO 0")
        arduino.close()

if __name__ == "__main__":
    main()
