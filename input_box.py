import pygame, string
from pygame.locals import *
import config

def join(l):
    s = ''
    for i in l:
        s = s + i
    return s

class InputBox():
    def __init__(self):
        pygame.init()
    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass

    def display_box_(self,screen, message, size,position):
        fontobject = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (0, 0, 0),
                         (position[0] - size[0]/2-5,
                          position[1] - size[1]/2-5,
                          size[0]+10,size[1]+10), 0)
        pygame.draw.rect(screen, config.CYAN,
                         [position[0] - size[0] / 2,
                          position[1] - size[1] / 2,
                          size[0], size[1]], )
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (0,0,0)),
                        (position[0]-7, position[1]-8))
        pygame.display.update()


    def display_box(self,screen, message, size):
        fontobject = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (0, 0, 0),
                         ((screen.get_width() / 2) - 100,
                          (screen.get_height() / 2) - 10,
                          200, 20), 0)
        pygame.draw.rect(screen, config.CYAN,
                         [(screen.get_width() / 2) - size[0] / 2,
                          (screen.get_height() / 2) - size[1] / 2,
                          size[0], size[1]], )
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (0,0,0)),
                        ((screen.get_width() / 2) - size[0] / 2 + 20, (screen.get_height() / 2) - size[1] / 2 + 10))
        pygame.display.update()


    def ask(self,screen, question, size):
        pygame.font.init()
        current_string = []
        self.display_box(screen, question + " : " + join(current_string), size)
        while 1:
            inkey = self.get_key()
            if inkey == K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == K_ESCAPE:
                return None
            elif inkey == K_RETURN:
                break
            elif inkey == K_MINUS:
                current_string.append("_")
            elif inkey <= 127:
                current_string.append(chr(inkey))
            self.display_box(screen, question + " : " + join(current_string), size)
            pygame.display.update()
        return join(current_string)

