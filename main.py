# import pygame
from audio import main_audio_loop
import colorama
colorama.init()

if __name__ == "__main__":
    # pygame.init()
    # FPS = pygame.time.Clock()
    # DISPLAYSURF = pygame.display.set_mode((1440, 900), pygame.FULLSCREEN)
    # DISPLAYSURF.fill((0, 0, 0))
    
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #     pygame.display.update()
    #     FPS.tick(60)
    main_audio_loop()