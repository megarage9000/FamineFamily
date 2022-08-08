import pygame
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

my_font = pygame.font.SysFont('Ariel', 30)


def EndScreen(endgame_text):
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    running = True

    while running:
        # Fill background with white
        screen.fill((255, 255, 255))

        END_GAME_TEXT = my_font.render(endgame_text, True, "#000000")
        END_GAME_RECT = END_GAME_TEXT.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))

        screen.blit(END_GAME_TEXT, END_GAME_RECT)

        # Checks if use clicked closed window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        # Draw Button to quit, reset, and text for game over



        pygame.display.flip()

EndScreen("You won!")
pygame.quit()