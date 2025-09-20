import cv2
import mediapipe as mp
import math as m
from flask import Flask, render_template, Response, jsonify, request
import winsound
import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

# Initialize Flask
app = Flask(__name__)

# Initialize pose estimation
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Placeholder colors
yellow = (0, 255, 255)
pink = (255, 0, 255)
green = (0, 255, 0)
red = (0, 0, 255)
light_green = (50, 255, 50)

# Default font
font = cv2.FONT_HERSHEY_SIMPLEX

good_frames = 0
bad_frames = 0

# Initialize video capture (None initially)
cap = None
video_streaming = False  # To track if the video is currently streaming
user_email = ""  # Variable to store the user's email

def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

def sendWarning():
    # Windows sound alert (you can use other platforms' libraries for sound alerts)
    frequency = 2500  # Set Frequency to 2500 Hertz
    duration = 1000   # Set Duration to 1000 ms = 1 second
    winsound.Beep(frequency, duration)

def sendWarning2():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()  # Hide the main window
    messagebox.showwarning("Posture Warning", "You have been in bad posture for an extended time! Please correct your posture.")
    print("Popup warning displayed!")

def sendWarning3():
    global user_email
    if user_email:
        # Setup the email parameters
        sender_email = "raomanit270@gmail.com"
        receiver_email = user_email  # Use the email entered by the user
        password = "wopx tcrf lckj ooky"
        
        subject = "Warning: Bad Posture Detected"
        body = "Warning: You have been in bad posture for an extended time! Please correct your posture."

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

def generate_frames():
    global good_frames, bad_frames
    while cap.isOpened() and video_streaming:
        # Capture frames
        success, image = cap.read()
        if not success:
            break

        # Get fps and frame dimensions
        fps = cap.get(cv2.CAP_PROP_FPS)
        h, w = image.shape[:2]

        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image
        keypoints = pose.process(image)

        # Convert RGB back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Acquire landmark coordinates
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        # Left shoulder.
        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

        # Right shoulder.
        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        # Left ear.
        l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
        l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

        # Left hip.
        l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
        l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

        # Check camera alignment
        offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
        if offset < 100:
            cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
        else:
            cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

        # Calculate angles.
        neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

        # Draw landmarks.
        cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

        # Put text, Posture and angle inclination.
        angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

        # Determine whether good posture or bad posture.
        if neck_inclination < 40 and torso_inclination < 10:
            bad_frames = 0
            good_frames += 1

            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

            # Join landmarks.
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

        else:
            good_frames = 0
            bad_frames += 1

            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

            # Join landmarks.
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

        # Calculate time spent in good and bad posture
        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames

        # Display time on screen
        if good_time > 0:
            time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
            cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
        else:
            time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
            cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

        # If bad posture time exceeds 180 seconds, send an alert
        if 3 < bad_time < 3.1:
            sendWarning()

        if 5 < bad_time < 5.1:
            sendWarning2()

        if 6 < bad_time < 6.1:
            sendWarning3()

        # Generate frame
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_video', methods=['POST'])
def start_video():
    global cap, video_streaming
    if not video_streaming:
        cap = cv2.VideoCapture(0)
        video_streaming = True
    return jsonify({'status': 'started'})

@app.route('/stop_video', methods=['POST'])
def stop_video():
    global cap, video_streaming
    if video_streaming:
        cap.release()
        video_streaming = False
    return jsonify({'status': 'stopped'})

@app.route('/set_email', methods=['POST'])
def set_email():
    global user_email
    user_email = request.form.get('email')
    return jsonify({'status': 'email set', 'email': user_email})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    app.run(debug=True, host='0.0.0.0', port=5000)