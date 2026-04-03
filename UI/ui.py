import pygame
from manager import manual_width, manual_height, screen_width, screen_height


def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2) * ((value - min1) / (max1 - min1))


class Button:
    def __init__(self, text, position=(screen_width - 230, 400), w=100, h=50, border=0, color=(0, 0, 0),
                 border_color=(0, 0, 0)):
        self.text = text
        self.position = position
        self.w = w
        self.h = h
        self.border = border
        self.temp = color
        self.color = color
        self.border_color = border_color
        self.font = 'freesansbold.ttf'
        self.fontSize = 25
        self.textColor = (255, 255, 255)
        self.state = False
        self.action = None
        self.clicked = False

    def handle_mouse(self, mouse_clicked, hover_color=(32, 178, 170)):
        m = pygame.mouse.get_pos()
        if self.position[0] <= m[0] <= self.position[0] + self.w:
            if self.position[1] <= m[1] <= self.position[1] + self.h:
                self.color = hover_color
                if mouse_clicked:
                    self.color = (200, 200, 200)
                    if self.action is None and mouse_clicked == True:
                        self.state = not self.state
            else:
                self.color = self.temp
        else:
            self.color = self.temp

    def render(self, screen, mouse_clicked, checker=True):
        if checker:
            self.handle_mouse(mouse_clicked)
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.textColor)
        textRect = text.get_rect()
        textRect.center = (self.position[0] + self.w // 2, self.position[1] + self.h // 2)
        if self.border > 0:
            pygame.draw.rect(screen, self.border_color,
                             pygame.Rect(self.position[0] - self.border // 2, self.position[1] - self.border // 2,
                                         self.w + self.border, self.h + self.border), border_radius=15)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h), border_radius=15)
        screen.blit(text, textRect)


class Panel:
    def __init__(self, position=(screen_width - 400,0), w=385, h=screen_height, color=(2, 3, 12), alpha=50):
        self.position = position
        self.w = w
        self.h = h
        self.color = color
        self.alpha = alpha

    def render(self, screen):
        s = pygame.Surface((self.w, self.h))
        s.set_alpha(self.alpha)
        s.fill(self.color)
        screen.blit(s, (self.position[0], self.position[1]))


class DropDownButton:
    def __init__(self, text="Select", position=(screen_width - 230, 400), w=100, h=50, children_size=2, border=0,
                 color=(0, 0, 0), border_color=(0, 0, 0)):
        self.text = text
        self.position = position
        self.w = w
        self.h = h
        self.border = border
        self.temp = color
        self.color = color
        self.children_size = children_size
        self.childs = []
        for i in range(self.children_size):
            button = Button("button " + str(i), (position[0], position[1] + h + h * i + 2), w, h, border, color,
                            border_color)
            self.childs.append(button)
        self.border_color = border_color
        self.font = 'freesansbold.ttf'
        self.fontSize = 25
        self.textColor = (255, 255, 255)
        self.state = False
        self.action = None
        self.selected = False
        self.folded = False
        self.current_index = None

    def handle_mouse(self, mouse_clicked, hover_color=(50, 120, 140)):
        m = pygame.mouse.get_pos()
        if self.position[0] <= m[0] <= self.position[0] + self.w:
            if self.position[1] <= m[1] <= self.position[1] + self.h:
                self.color = hover_color
                if mouse_clicked:
                    self.folded = not self.folded
                    self.color = (200, 200, 200)
                    if self.action is None and mouse_clicked:
                        self.state = not self.state
            else:
                self.color = self.temp
        else:
            self.color = self.temp
        if self.folded:
            for child in self.childs:
                m = pygame.mouse.get_pos()
                if child.position[0] <= m[0] <= child.position[0] + child.w:
                    if child.position[1] <= m[1] <= child.position[1] + child.h:
                        child.color = hover_color
                        if mouse_clicked:
                            child.color = (200, 200, 200)
                            self.text = child.text
                            self.current_index = self.childs.index(child)
                            self.folded = not self.folded
                            if child.action is None and mouse_clicked:
                                child.state = not child.state
                    else:
                        child.color = child.temp
                else:
                    child.color = child.temp

    def render(self, screen, mouse_clicked, checker=True):
        if checker:
            self.handle_mouse(mouse_clicked)
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.textColor)
        textRect = text.get_rect()
        textRect.center = (self.position[0] + self.w // 2, self.position[1] + self.h // 2)
        if self.border > 0:
            pygame.draw.rect(screen, self.border_color,
                             pygame.Rect(self.position[0] - self.border // 2, self.position[1] - self.border // 2,
                                         self.w + self.border, self.h + self.border), border_radius=15)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h), border_radius=15)
        screen.blit(text, textRect)
        if self.folded:
            for child in self.childs:
                child.render(screen, mouse_clicked, False)
