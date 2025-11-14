import cv2
import pygame
import time
import game
from gesture import get_hand_direction

cap = cv2.VideoCapture(0)

# Countdown before game starts
for i in range(3, 0, -1):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, f"Starting in {i}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Hand Detection", frame)
    cv2.waitKey(1000)

pygame.time.set_timer(pygame.USEREVENT, 1500)
jump_timer = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    gesture = get_hand_direction(frame)

    if gesture == "LEFT":
        game.player_lane = max(0, game.player_lane - 1)
    elif gesture == "RIGHT":
        game.player_lane = min(2, game.player_lane + 1)
    elif gesture == "UP" and not game.jump:
        game.jump = True
        jump_timer = pygame.time.get_ticks()

    if game.jump:
        t = (pygame.time.get_ticks() - jump_timer) / 200.0
        if t < 1:
            game.jump_height = int(50 * (1 - (t - 1) ** 2))
        else:
            game.jump = False
            game.jump_height = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()
        elif event.type == pygame.USEREVENT:
            game.spawn_obstacle()

    game.update_game()
    game.draw_game()

    if game.check_collision():
        print("💥 Game Over!")
        cv2.putText(frame, "Game Over!", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Hand Detection", frame)
        pygame.time.wait(3000)
        break

    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
