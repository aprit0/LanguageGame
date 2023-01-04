import pygame


class Button:
    """Create a button, then blit the surface in the while loop"""
    def __init__(self, name, pos, font=25, bg="black", bg_hover='grey'):
        self.name = name
        self.font = pygame.font.SysFont("Arial", font)
        self.bg = bg
        self.bg_hover = bg_hover
        self.text = self.font.render(self.name, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.x, self.y = [int(pos[i] - 0.5 * self.size[i]) for i in range(len(pos))]
        self.surface = pygame.Surface(self.size)

        self.draw(self.bg)

    def draw(self, colour):
        # draw button
        self.surface.fill(colour)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])


    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.draw(self.bg_hover)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                return 1
        else:
            self.draw(self.bg)
        return 0

class Im_Button:
    def __init__(self, name, pose, im):
        self.name = name
        self.pose = pose
        self.im = im
        self.size = self.im.get_size()
        self.x, self.y = self.pose # [int(pose[i] - 0.5 * self.size[i]) for i in range(len(pose))]

    def draw(self, text):
        # draw button
        self.text = self.font.render(, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                return 1
        return 0



def text_box(font, text, colour, pose):
    text = font.render(text, True, colour)
    size = text.get_size()
    pose = [int(pose[i] - 0.5 * size[i]) for i in range(len(pose))]
    return text, pose



