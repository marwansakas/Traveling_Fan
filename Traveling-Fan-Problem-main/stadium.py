import pygame

pygame.font.init()
textColor = (0, 0, 0)
textFont = pygame.font.SysFont("Arial", 20)


class Stadium:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, manager, show_index=False, point_index=0):
        stadium_image = pygame.image.load(self.image)
        stadium_image = pygame.transform.scale(stadium_image, (100, 100))  # Adjust the size as needed

        # Blit the stadium image onto the screen
        stadium_rect = stadium_image.get_rect(center=(self.x, self.y))
        manager.screen.blit(stadium_image, stadium_rect)

        if show_index:
            # Render and blit the point index
            text_surface = textFont.render(str(point_index), True, textColor)
            text_rectangle = text_surface.get_rect(center=(self.x, self.y - 12))
            manager.screen.blit(text_surface, text_rectangle)


