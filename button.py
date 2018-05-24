# from function import *
import pygame, string
#from pygame.locals import *
import config
import time

def text_objects(text, font):
    textSurf = font.render(text, True, config.SILVER1)
    return textSurf, textSurf.get_rect()

def is_inside(start, size, point):
    return ((point[0] - start[0]) * (point[0] - start[0] - size[0]) < 0) and (
        (point[1] - start[1]) * (point[1] - start[1] - size[1]) < 0)

pygame.init()
myfont = pygame.font.Font("freesansbold.ttf", 20)
myfont2 = pygame.font.Font("freesansbold.ttf", 30)
class Button():
    def __init__(self, normal_image, selected_image, size):
        self.images = [normal_image, selected_image]
        self.image = normal_image
        self.size = size
        self.is_selected = False

    def select(self):
        self.is_selected = True
        self.image = self.images[1]

    def de_select(self):
        if self.is_selected:
            self.is_selected = False
            self.image = self.images[0]

    def showButton(self, screen, button_position, mouse_position):
        if self.is_selected == True:
            img = pygame.transform.scale(pygame.image.load(self.image), self.size)
            screen.blit(img, button_position)
            pygame.draw.rect(screen, config.RED, [button_position[0], button_position[1], self.size[0], self.size[1]],
                             2)
        else:
            if is_inside(button_position, self.size, mouse_position):
                img = pygame.transform.scale(pygame.image.load(self.images[1]), self.size)
                screen.blit(img, button_position)
            else:
                img = pygame.transform.scale(pygame.image.load(self.image), self.size)
                screen.blit(img, button_position)

class BasicButton():
    def __init__(self, text, size, text_size, curv=0):
        self.text = text
        self.size = size
        self.text_size = text_size
        self.curv = curv
        self.font = pygame.font.Font("freesansbold.ttf", self.text_size)

    def show(self, screen, colour, position):
        pygame.draw.polygon(screen, colour, [[position[0] + self.curv, position[1]],
                                             [position[0] - self.curv + self.size[0], position[1]],

                                             [position[0] + self.size[0], position[1] + self.curv],
                                             [position[0] + self.size[0], position[1] - self.curv + self.size[1]],
                                             [position[0] + self.size[0] - self.curv, position[1] + self.size[1]],
                                             [position[0] + self.curv, position[1] + self.size[1]],
                                             [position[0] - self.curv + self.size[0], position[1] + self.size[1]],
                                             [position[0] + self.curv, position[1] + self.size[1]],
                                             [position[0], position[1] - self.curv + self.size[1]],
                                             [position[0], position[1] + self.curv]
                                             ], )
        TextSurf, TextRect = text_objects(self.text, self.font)
        TextRect.center = (position[0] + self.size[0] / 2, position[1] + self.size[1] / 2)
        screen.blit(TextSurf, TextRect)

    def showButton(self, screen, position, mouse_position):
        if is_inside(position, self.size, mouse_position):
            self.show(screen, config.CYAN, position)
        else:
            self.show(screen, config.SILVER, position)

class BasicText():
    def __init__(self, text, text_size):
        self.text = text
        self.size = text_size
        self.font = pygame.font.Font("freesansbold.ttf", self.size)

    def showText(self, screen, position):
        TextSurf, TextRect = text_objects(self.text, self.font)
        TextRect.center = (position[0], position[1])
        screen.blit(TextSurf, TextRect)




class ImageButton():
    def __init__(self, normal_image, selected_image, size = [60,60],position = None):
        self.images = [normal_image, selected_image]
        self.image = normal_image
        self.size = size
        self.position = position
        self.is_selected = False

    def select(self):
        self.is_selected = True
        self.image = self.images[1]

    def de_select(self):
        if self.is_selected:
            self.is_selected = False
            self.image = self.images[0]

    def display(self, screen):
        if self.position == None:
            return None
        mouse_position = pygame.mouse.get_pos()
        if self.is_selected == True:
            img = pygame.transform.scale(pygame.image.load(self.image), self.size)
            screen.blit(img, self.position)
            pygame.draw.rect(screen, Config.RED, [self.position[0], self.position[1], self.size[0], self.size[1]],
                             2)
        else:
            if is_inside(self.position, self.size, mouse_position):
                img = pygame.transform.scale(pygame.image.load(self.images[1]), self.size)
                screen.blit(img, self.position)
            else:
                img = pygame.transform.scale(pygame.image.load(self.image), self.size)
                screen.blit(img, self.position)


class Label():
    def __init__(self, text = '', text_size = 20,position = None):
        self.text = text
        self.size = text_size
        self.position = position
        self.font = pygame.font.Font("freesansbold.ttf", self.size)

    def display(self, screen):
        if self.position == None:
            return None
        TextSurf, TextRect = text_objects(self.text, self.font)
        TextRect.center = (self.position[0], self.position[1])
        screen.blit(TextSurf, TextRect)


class TextButton():
    def __init__(self, size=[100, 50], text='', textSize=20, position=None, curv=0, func=None, argv=()):
        self.size = size
        self.text = text
        self.textSize = textSize
        self.position = position
        self.func = func
        self.argv = argv
        self.curv = curv
        self.font = pygame.font.Font("freesansbold.ttf", self.textSize)

    def run(self):
        if self.func == None:
            return None
        self.func(*self.argv)

    def setSize(self, size):
        self.size = size

    def setText(self, text):
        self.text = text

    def setTextSize(self, textSize):
        self.textSize = textSize

    def show(self, screen, colour):
        if self.position == None:
            return None
        pygame.draw.polygon(screen, colour, [[self.position[0] + self.curv, self.position[1]],
                                             [self.position[0] - self.curv + self.size[0], self.position[1]],

                                             [self.position[0] + self.size[0], self.position[1] + self.curv],
                                             [self.position[0] + self.size[0],
                                              self.position[1] - self.curv + self.size[1]],
                                             [self.position[0] + self.size[0] - self.curv,
                                              self.position[1] + self.size[1]],
                                             [self.position[0] + self.curv, self.position[1] + self.size[1]],
                                             [self.position[0] - self.curv + self.size[0],
                                              self.position[1] + self.size[1]],
                                             [self.position[0] + self.curv, self.position[1] + self.size[1]],
                                             [self.position[0], self.position[1] - self.curv + self.size[1]],
                                             [self.position[0], self.position[1] + self.curv]
                                             ], )
        TextSurf, TextRect = text_objects(self.text, self.font)
        TextRect.center = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
        screen.blit(TextSurf, TextRect)

    def display(self, screen):
        mouse_position = pygame.mouse.get_pos()
        if is_inside(self.position, self.size, mouse_position):
            self.show(screen, Config.CYAN2)
        else:
            self.show(screen, Config.SILVER)
        if pygame.mouse.get_pressed()[0]:
            mouse_position_down = pygame.mouse.get_pos()
            if is_inside(self.position, self.size, mouse_position_down):
                time.sleep(0.1)
                self.run()


