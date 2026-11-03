# Arduino Control System

## Overview

The Arduino code controls the agricultural robot's movement, soil moisture measurement mechanism, ultrasonic distance detection, and automatic water pump.

## Hardware Connections

| Component | Arduino Pins |
|---|---|
| Left Motor | 3, 4, 5 |
| Right Motor | 11, 12, 6 |
| Soil Motor | 13, 2, 9 |
| Ultrasonic Sensor | Trigger: 10, Echo: 7 |
| Soil Moisture Sensor | A0 |
| Water Pump Relay | 8 |

## Main Functions

- **Robot Movement:** Controls forward movement and stopping.
- **Obstacle Detection:** Measures distance using an ultrasonic sensor.
- **Soil Moisture Measurement:** Reads soil moisture values using an analog sensor.
- **Soil Sensor Mechanism:** Moves the soil sensor down and up using a motor.
- **Automatic Irrigation:** Controls the water pump through a relay.
- **Serial Communication:** Receives commands from the Raspberry Pi.

## Fruit-Based Irrigation

The irrigation duration depends on the received fruit type:

| Fruit Type | Watering Duration |
|---|---:|
| Apple | 3 seconds |
| Guava | 5 seconds |
| Pomegranate | 7 seconds |

If the soil moisture value is greater than 500, an additional 2 seconds are added to the watering duration.

## Serial Commands

| Command | Function |
|---|---|
| `plant` | Stops the robot and waits for fruit classification. |
| `apple` | Starts apple irrigation settings. |
| `guava` | Starts guava irrigation settings. |
| `pomegranate` | Starts pomegranate irrigation settings. |
| `go` | Resumes robot movement. |

## Operating Workflow

1. The robot moves forward.
2. The ultrasonic sensor measures the distance.
3. When a plant is detected through the received command, the robot stops.
4. The system waits for the fruit type.
5. The soil sensor moves down to measure soil moisture.
6. The sensor returns to its original position.
7. The irrigation duration is determined.
8. The water pump is activated.
9. The pump stops automatically after the specified duration.
10. The robot continues moving to the next plant. 
