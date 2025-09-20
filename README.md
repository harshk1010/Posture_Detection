# Posture Detection Web Application 
A posture detection web application developed to help users maintain a healthy posture, especially during prolonged periods of sitting. The application uses real-time video analysis to detect poor posture and provides multi-modal alerts to encourage immediate correction.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Requirements](#requirements)  
- [Installation](#installation)    
- [Modules](#modules)  
- [Contributing](#contributing)  

---

# Features

Real-Time Posture Monitoring: Continuously analyzes user posture through a webcam feed using MediaPipe.

Multi-Modal Alerts: Notifies users of poor posture through:

Visual Popups: On-screen messages for immediate feedback.

Sound Notifications: Auditory alerts to grab attention.

Email Alerts: Sends emails for extended periods of incorrect posture, ensuring the user is aware even if other alerts are missed.

Web-Based Interface: Accessible through a user-friendly web interface built with Flask, HTML, and CSS.

Browser Integration: A Chrome Extension built with Manifest V3 allows for seamless monitoring during online meetings and virtual classes.


# Tech Stack
Backend

Flask: A lightweight Python web framework for handling the application's backend logic and serving the web interface.

MediaPipe: An open-source framework by Google for real-time pose estimation and landmark detection.

OpenCV (cv2): Used for capturing video from the webcam and processing individual frames.

smtplib: A Python library for sending email notifications via the Simple Mail Transfer Protocol (SMTP).

winsound: A Python library for playing audio alerts on Windows systems.

tkinter: Python's standard library for creating graphical user interfaces, used here to display popup alerts.

Frontend

HTML/CSS: For structuring and styling the web interface.

JavaScript: For interactivity and dynamic elements within the web interface and browser extension.

# Requirements
Hardware

Processor (CPU): Dual-core processor (e.g., Intel Core i3 or equivalent).

Memory (RAM): 4 GB or higher.

Storage: 40 GB SSD or HDD.

Graphics Card: Integrated GPU with OpenGL 3.3 support or higher.

Camera: Integrated or external webcam.

Software

Operating System: Windows 10/11, macOS, or Linux (Ubuntu 20.04 or later).

Programming Language: Python 3.8 or higher.

Browser: A modern web browser, such as Chrome or Edge, for the extension.

Package Manager: pip for Python dependency management.

# Installation
Clone the repository:

Bash

git clone https://github.com/your-username/posture-detection-app.git
cd posture-detection-app
Install Python dependencies:

Bash

pip install -r requirements.txt
Note: The requirements.txt file should include Flask, MediaPipe, opencv-python, and other necessary libraries. Since winsound and tkinter are built-in, they may not need to be listed.

Running the Application
Start the Flask server:

Bash

python app.py
(Assuming your main application file is named app.py)

Open the web application:
Navigate to http://127.0.0.1:5000 in your web browser.

Use the browser extension:
Follow the instructions to install the Chrome Extension and enable it for seamless monitoring.

# Modules

The project is built with several key modules that handle specific functionalities:

Video Input Module: Uses OpenCV (cv2) for capturing and processing video from the webcam.

Pose Detection Module: Employs MediaPipe to detect and track human body landmarks for posture analysis.

Calculation Module: A built-in Python module used for performing mathematical operations like calculating angles between landmarks.

Web Framework Module: Flask is used to create the web application, handle user input, and serve the video feed.

Alert Modules: winsound, tkinter, and smtplib are used to provide different types of alerts when bad posture is detected.

Multithreading Module: threading is used to handle video streaming and frame generation concurrently, ensuring the Flask app remains responsive.



# Contributing
Contributions are welcome! If you have suggestions or find any bugs, please follow these steps:

Fork the repository.

Create a new branch: git checkout -b feature-name.

Make your changes and commit them: git commit -m 'Add new feature'.

Push to the branch: git push origin feature-name.

Submit a pull request.
