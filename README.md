# ✋ Hand Gesture Controlled Robotic Arm

A real-time robotic arm control system using **computer vision + ESP32** to control servos through hand gestures.

---

## 🚀 Overview

This project captures hand movements via webcam and translates them into robotic arm motion.

Pipeline:

* Detect hand → Compute finger angles → Map to servo angles → Send via serial → Move servos

---

## 📁 Project Structure

```bash
.
├── hand_control.py              # Python (Computer Vision + Serial Communication)
├── hand_control_arduino.ino    # ESP32 (Servo Control + Parsing)
└── README.md
```

---

## ⚙️ Features

* Real-time hand tracking (MediaPipe)
* 21 landmark detection
* Finger angle computation using vector math
* Smooth servo control (20 Hz)
* Serial communication (UART - 115200 baud)
* Safety watchdog (auto reset)

---

## 🛠️ Tech Stack

### Software

* Python
* OpenCV
* MediaPipe
* NumPy
* PySerial

### Hardware

* ESP32
* PCA9685 PWM Driver
* Servo Motors
* Webcam

---

## ▶️ How to Run

### 1. Install Dependencies

```bash
pip install opencv-python mediapipe numpy pyserial
```

### 2. Run Python Script

```bash
python hand_control.py
```

### 3. Upload Arduino Code

* Open `hand_control_arduino.ino` in Arduino IDE
* Select ESP32 board
* Upload to ESP32

---

## 🔌 Hardware Setup

* ESP32 ↔ PCA9685 via I2C

  * SDA → GPIO21
  * SCL → GPIO22
* Servos → PCA9685 channels (0–4)
* External 5V power for servos
* USB connection between PC and ESP32

---

## 📊 Key Parameters

| Parameter     | Value   |
| ------------- | ------- |
| Resolution    | 640×480 |
| Baud Rate     | 115200  |
| Update Rate   | 20 Hz   |
| Servo Range   | 0°–180° |
| PWM Frequency | 50 Hz   |

---

## ⚠️ Limitations

* Single-hand only
* Lighting sensitive
* No feedback (open-loop)
* Wired system

---

## 🔮 Future Scope

* Wireless control (WiFi / Bluetooth)
* Dual-hand gestures
* Depth-based tracking
* Closed-loop feedback system

---

## 👥 Team

* Harsha – Integration
* Aisiri – Computer Vision
* Upendra – Hardware
* Jayarathna – Algorithms

---

## 📽️ Demo

https://drive.google.com/file/d/1FIV2spZmgYVHlwHsqFWBenhmv_bq3Q1j/view?usp=drivesdk

---

## 🏁 Conclusion

A complete **real-time gesture-controlled robotic system**, integrating computer vision with embedded hardware.

---

## 📜 License

Academic project.
