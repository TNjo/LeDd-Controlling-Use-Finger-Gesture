import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe
import serial # pip install pyserial

ser = serial.Serial('COM3', 9600) # Change the COM port to the one you are using
prev_upCount = -1
totalFingers = 0

cap = cv2.VideoCapture(0) # Change the camera index to the one you are using
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8) # Increase the detection confidence for better results

while True:
    success, img = cap.read()
    right_hand_details, img = detector.findRightHand(img)  # Use the modified findRightHand method
    # print(len(right_hand_details))

    if len(right_hand_details) == 1:
        list_fingers = detector.fingersUp(right_hand_details[0]) # Use the modified fingersUp method
        totalFingers = sum(list_fingers)
        print(totalFingers)

    if totalFingers != prev_upCount:
        ser.write(str(totalFingers).encode()) # Send the data to the Arduino
        prev_upCount = totalFingers

    cv2.putText(img, str(totalFingers), (256, 256), cv2.FONT_HERSHEY_PLAIN, 10, (255, 200, 0), 6)
    # x axis coordination
    # img = cv2.line(img, (128, 0), (128, img.shape[1]), (255, 0, 0), 3)
    # img = cv2.line(img, (256, 0), (256, img.shape[1]), (0, 255, 0), 3)
    # img = cv2.line(img, (384, 0), (384, img.shape[1]), (0, 0, 255), 3)
    # y axis coordination
    # img = cv2.line(img, (0, 128), (img.shape[1], 128), (255, 0, 0), 3)
    # img = cv2.line(img, (0, 256), (img.shape[1], 256), (0, 255, 0), 3)
    # img = cv2.line(img, (0, 384), (img.shape[1], 384), (0, 0, 255), 3)

    cv2.imshow("IronMan", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
# Close the serial port
ser.close()