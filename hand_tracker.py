import cv2
import os
import mediapipe as mp
from math import *
from statistics import *
import spotify_controller as spc

def start_hand_tracker(show_image=False):

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils
    sp = spc.connect_to_spotify()
    cap = cv2.VideoCapture(0)

    if 'beans_ear' not in os.listdir():
        with open('beans_ear', 'w') as f:
            f.write('False')

    # while cap.isOpened():
    while(True):
        success, image = cap.read()
        if not success:
            break
        
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image with MediaPipe
        results = hands.process(image_rgb)
        
        # Draw hand landmarks on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                x_list = []
                y_list = []
                z_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    x, y, z = lm.x, lm.y, lm.z
                    x_list.append(x)
                    y_list.append(y)
                    z_list.append(z)
                mx = mean(x_list)
                my = mean(y_list)
                mz = mean(z_list)
                sdx = sqrt(variance(x_list))
                sdy = sqrt(variance(y_list))
                sdz = sqrt(variance(z_list))
                if sdy > 0.055 and sdx > 0.035:
                    with open('beans_ear', 'w') as f:
                        f.write('True')
                else:
                    with open('beans_ear', 'w') as f:
                        f.write('False')

                with open('beans_ear', 'r') as f:
                    res = f.readline()
                    # print(res)
                # print(f'X Mean: {mx}')
                # print(f'X SD: {sdx}')
                # print('')
                # print(f'Y Mean: {my}')
                # print(f'Y SD: {sdy}')
                # print('')
                # print(f'Z Mean: {mz}')
                # print(f'Z SD: {sdz}')
                # print('')

                # if my < 0.2:
                #     print(f'xsd: {sdx}')
                #     print(f'ysd: {sdy}')
                    # if sdx > 0.05:
                    #     spc.change_volume('down', sp=sp)
                    # elif sdy > 0.05:
                    #     spc.change_volume('up', sp=sp)
        else:
            with open('beans_ear', 'w') as f:
                f.write('False')
        
        # Display the image
        if show_image:
            cv2.imshow('MediaPipe Hands', image)
        
        # Exit loop if 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()