#include <Servo.h>

// Define the number of servos and their pins
const int num_servos = 6;
const int servo_pins[num_servos] = { 2, 3, 4, 5, 6, 7 };  // Adjust pin numbers as needed

// Create servo objects
Servo servos[num_servos];

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  while (!Serial)
    ;  // Wait for serial port to connect

  Serial.println("Arduino is ready.");

  // Attach servos to pins
  for (int i = 0; i < num_servos; i++) {
    servos[i].attach(servo_pins[i]);
  }
}

void loop() {
  // Check if there's data available to read from serial port
  int angle_index = 0;
    int servo_angles[num_servos];
    int start_index = 0;
  if (Serial.available() > 0) {
    // Read the incoming message
    String message = Serial.readStringUntil('\n');
    Serial.print(message);

    // Parse the message into individual angle values
    
    for (int i = 0; i < message.length(); i++) {
      if (message.charAt(i) == ',') {
        servo_angles[angle_index++] = message.substring(start_index, i).toInt();
        start_index = i + 1;
      }
    }
  }

  // Set angles for each servo
  for (int i = 0; i < num_servos; i++) {
    if (i < angle_index) {
      // Map angle values to servo range (0 to 180)
      int servo_angle = map(servo_angles[i], -90, 90, 0, 180);
      servos[i].write(servo_angle);
      Serial.print("Set servo ");
      Serial.print(i);
      Serial.print(" angle: ");
      Serial.println(servo_angle);
    } else {
      // Default angle (e.g., 90 degrees) if not provided
      servos[i].write(90);
      Serial.print("Set servo ");
      Serial.print(i);
      Serial.println(" angle: 90");
    }
  }
}
