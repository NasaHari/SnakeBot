import serial
import time
import numpy as np

# Establish serial connection with Arduino
arduino_port = 'COM4'  # Update with your Arduino port
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

# Define parameters
num_segments = 6
frequency = 1  # Adjust frequency as desired

def calculate_angles(t):
    speed = 50
    t = t * speed
    angles = []
    for i in range(num_segments):
        angles.append(np.sin(2 * np.pi * frequency * t + i * np.pi/num_segments))
    return angles

def calculate_segment_angles(angles):
    segment_angles = [angles[i+1] - angles[i] for i in range(num_segments - 1)]
    return segment_angles

def send_angles_to_arduino(angles):
    angles = np.array(angles) * 180 / np.pi
    angles = [round(angle) for angle in angles]
    angles = [max(0, min(180, 90 + angle)) for angle in angles]  # Constrain to 0-180

    message = ','.join(map(str, angles))
    ser.write((message + '\n').encode())
    print(f'Sent angles to Arduino: {message}')
    
    # Wait for a short time for Arduino's response
    start_time = time.time()
    while time.time() - start_time < 0.5:  # Wait for up to 0.5 seconds
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            print(f"Arduino says: {response}")
            if response == "Done":
                return
    print("No 'Done' response received from Arduino")

# Main loop to calculate and send angles
try:
    while True:
        for t in np.linspace(0, 2*np.pi, 100):
            angles = calculate_angles(t)
            segment_angles = calculate_segment_angles(angles)
            send_angles_to_arduino(segment_angles)
            time.sleep(0.1)  # Small delay between sends
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    ser.close()
    print("Serial connection closed")