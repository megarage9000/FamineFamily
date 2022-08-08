import pygame
from Button import Button
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

my_font = pygame.font.SysFont('Ariel', 30)



def end_screen(endgame_text):
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    running = True
    while running:
        # Fill background with white
        screen.fill((255, 255, 255))

        # End game text
        end_game_text = my_font.render(endgame_text, True, "#000000")
        end_game_rect = end_game_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        screen.blit(end_game_text, end_game_rect)

        # Button leave
        leave_pos = (SCREEN_WIDTH/4, SCREEN_HEIGHT / 2)
        leave_text = my_font.render("Leave Game", True, "#000000")
        leave_rect = leave_text.get_rect(center=(leave_pos[0], leave_pos[1] + 100))
        screen.blit(leave_text, leave_rect)
        leave_button = Button(image=pygame.image.load("assets/quit-icon.png"),
                              pos=leave_pos,
                              text_input="",
                              font=my_font,
                              base_color="#000000",
                              hovering_color="white")

        leave_button.update(screen)

        # Button to go to main menu
        return_pos = (3 * SCREEN_WIDTH/4, SCREEN_HEIGHT/2)
        return_text = my_font.render("Return to Start", True, "#000000")
        return_rect = return_text.get_rect(center=(return_pos[0], return_pos[1] + 100))
        screen.blit(return_text, return_rect)
        return_to_menu = Button(image=pygame.image.load("assets/enter.png"),
                              pos=return_pos,
                              text_input="",
                              font=my_font,
                              base_color="#000000",
                              hovering_color="white")

        return_to_menu.update(screen)

        mouse_pos = pygame.mouse.get_pos()

        # Checks if user clicked closed window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_menu.checkForInput(mouse_pos):
                    print("Returning to menu...")
                elif leave_button.checkForInput(mouse_pos):
                    print("Leaving game...")
                    running = False

        pygame.display.flip()


end_screen("You won!")
end_screen("You lost!")
pygame.quit()