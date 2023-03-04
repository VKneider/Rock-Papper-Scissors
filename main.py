import mediapipe as mp
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import random

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)


start_game = False
state_result = False
player_score = 0
computer_score = 0
last_winner = "None"
timer = 0
new_game = True

user_win = cv2.imread("img/userwin.png")
ai_win = cv2.imread("img/aiwin.png")

while new_game:
    background_image = cv2.imread("img/background.png")

    # Captures the image from the camera
    success, my_camera = cap.read()

    # Flips the image horizontally
    my_camera = cv2.flip(my_camera, 1)

    # Resizes camera image
    resized_camera = cv2.resize(my_camera, (300, 305))

    hands, my_camera = detector.findHands(resized_camera, flipType=False)

    if start_game:

        if state_result is False:
            timer = time.time() - initial_time
            cv2.putText(background_image, str(int(timer)), (990, 190),
                        cv2.FONT_HERSHEY_PLAIN, 8, (235, 69, 95), 2)

            if timer > 3:
                state_result = True
                timer = 0

                if hands:

                    player_move = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        player_move = 1
                    if fingers == [0, 1, 1, 1, 1] or fingers == [1, 1, 1, 1, 1]:
                        player_move = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        player_move = 3

                    ai_movement = random.randint(1, 3)
                    movement_image = cv2.imread(
                        f'img/{ai_movement}.png', cv2.IMREAD_UNCHANGED)
                    background_image = cvzone.overlayPNG(
                        background_image, movement_image, (572, 225))

                    # Player Wins
                    if (player_move == 1 and ai_movement == 3) or \
                            (player_move == 2 and ai_movement == 1) or \
                            (player_move == 3 and ai_movement == 2):
                        last_winner = "Player"
                        player_score += 1

                    # ai_movement Wins
                    if (player_move == 3 and ai_movement == 1) or \
                            (player_move == 1 and ai_movement == 2) or \
                            (player_move == 2 and ai_movement == 3):
                        last_winner = "Computer"
                        computer_score += 1

                    if player_move == ai_movement:
                        last_winner = "Draw"

                    hand_detected = True
                else:
                    hand_detected = False

    background_image[185:490, 100:400] = resized_camera

    if state_result and hand_detected:
        background_image = cvzone.overlayPNG(
            background_image, movement_image, (572, 225))

    # Attaches the camera image to the background image
    cv2.putText(background_image, str(player_score), (220, 610),
                cv2.FONT_HERSHEY_PLAIN, 4, (235, 69, 95), 2)
    cv2.putText(background_image, str(computer_score), (475, 610),
                cv2.FONT_HERSHEY_PLAIN, 4, (235, 69, 95), 2)
    cv2.putText(background_image, last_winner, (650, 610),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (235, 69, 95), 2)

    cv2.imshow("Rock Papper Scissors", background_image)

    if (player_score == 3):
        cv2.imshow("Rock Papper Scissors", user_win)
        new_game = False
        another_game = cv2.waitKey(0)
        if (another_game == 32):
            new_game = True
            player_score = 0
            computer_score = 0
            last_winner = "None"
            timer = 0

        

    if (computer_score == 3):
        cv2.imshow("Rock Papper Scissors", ai_win)
        new_game = False
        another_game = cv2.waitKey(0)
        if (another_game == 32):
            new_game = True
            player_score = 0
            computer_score = 0
            last_winner = "None"
            timer = 0
  

    start_key = cv2.waitKey(1)
    if (start_key == 32):  # 32 is the ASCII value of the space bar
        start_game = True
        initial_time = time.time()
        state_result = False






# Movments

# 1 = Rock
# 2 = Paper
# 3 = Scissors
