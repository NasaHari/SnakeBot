import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import serial
import math
import time

# Establish serial connection with Arduino
arduino_port = 'COM4'  # Update with your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
def read_from_arduino():
    if ser.in_waiting <= 0:
       print("No data available")
    while ser.in_waiting > 0:
        message = ser.readline()
        print("Message from Arduino:", message)
def send_angles_to_arduino(angles,frame):
    angles=np.array(angles)*180/np.pi
    # Construct message
    angles= [round(angle) for angle in angles]
    angles= [90+angle for angle in angles]

    message = ','.join(map(str, angles))
    # Send message to Arduino
    ser.write((message + '\n').encode())
    print(f'Sent angles to Arduino: {frame} frame  :{message}')
    time.sleep(1)
    
    
# Define parameters
num_segments = 6
segment_length = 10
frequency = 1  # Adjust frequency as desired

# Time array2

# Function to calculate angles for each joint
def calculate_angles(t):
    speed=50
    t=t*speed
    angles = []
    for i in range(num_segments):
        angles.append(np.sin(2 * np.pi * frequency * t + i * np.pi/num_segments))
    return angles

# Function to calculate positions of joints
def calculate_positions(angles):
    x = [0]
    y = [0]
    for i in range(num_segments):
        x.append(x[-1] + segment_length * np.cos(angles[i]))
        y.append(y[-1] + segment_length * np.sin(angles[i]))
    return x, y

# Function to calculate angles between segments
def calculate_segment_angles(angles):
    segment_angles = [angles[i+1] - angles[i] for i in range(num_segments - 1)]
    return segment_angles

# Animation function
def animate(frame):
    angles = calculate_angles(frame)
    x, y = calculate_positions(angles)
    
    # Update snake bot line
    line.set_data(x, y)
    
    # Update position of initial point
    init_point.set_data(x[0], y[0])
    
    # Update angle annotations
    segment_angles = calculate_segment_angles(angles)
    for i, (angle, joint) in enumerate(zip(segment_angles, joint_annot)):
        joint.set_position((x[i+1]*5, y[i+1]))
        joint.set_text(f'Angle  turn:{angle*180/np.pi:.2f} \n \n a:{angles[i]*180/np.pi:.2f}    ')
    send_angles_to_arduino(segment_angles,frame)
    return line, init_point, *joint_annot

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, num_segments*segment_length + 1)
ax.set_ylim(-num_segments*segment_length - 1, num_segments*segment_length + 1)
line, = ax.plot([], [], 'bo-')

# Initial point
init_point, = ax.plot([], [], 'ro')

# Angle annotations
joint_annot = [ax.annotate('', xy=(0, 0), xytext=(5, 5), textcoords='offset points') for _ in range(num_segments - 1)]

def toggle_animation(event):
    global is_running
    if is_running:
        ani.event_source.stop()
        button.label.set_text('Start Animation')
    else:
        ani.event_source.start()
        button.label.set_text('Pause Animation')
    is_running = not is_running

# Animation
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2*np.pi, 100), blit=True)

# Create button to toggle animation
button_ax = plt.axes([0.7, 0.01, 0.2, 0.05])
button = Button(button_ax, 'Pause Animation')
button.on_clicked(toggle_animation)

# Initialize animation state
is_running = True
plt.show()
