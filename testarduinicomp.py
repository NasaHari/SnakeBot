import serial
import time

arduino_port = 'COM4'  # Update with your Arduino port
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for connection to establish

def send_angles_to_arduino(angles):
    angles_str = ','.join(map(str, angles))
    ser.write(f"{angles_str}\n".encode())
    print(f"Sent angles: {angles_str}")
    
    # Read and print Arduino's response
    while True:
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            print(f"Arduino says: {response}")
            if response == "Done":
                break

# Test with some angles
test_angles = [
    [-45, 90, 90, 90, 90, 90],
    
]


for angles in test_angles:
    send_angles_to_arduino(angles)
    
    time.sleep(1)

ser.close()