from input_box import *
gameExit = False
from button import *
from composer import *
import tkinter
from tkinter.filedialog import askopenfilename
# import re
import os
from threading import Thread
from subprocess import call
from model import *

def play(song):
    os.system('timidity ' + song)
def create_thread_play(song):
    thread = Thread(target=play, args=(song,))
    return thread

def display(screen, a, x, y):
    basicfont = pygame.font.SysFont(None, 40)
    text = basicfont.render(a, True, (230, 230, 230), )
    screen.blit(text, [x, y])


def small_display(screen, a, x, y):
    basicfont = pygame.font.SysFont(None, 25)
    text = basicfont.render(a, True, (0, 0, 0), )
    screen.blit(text, [x, y])

def is_inside(start, size, point):
    return ((point[0] - start[0]) * (point[0] - start[0] - size[0]) < 0) and (
        (point[1] - start[1]) * (point[1] - start[1] - size[1]) < 0)

pygame.init()
screen = pygame.display.set_mode([960,540])
pygame.display.set_caption('AI')
bg = pygame.transform.scale(pygame.image.load('bg.jpg'), (960,540))
status = 'INIT'
c = InputBox()

add_midi_button = BasicButton('Add', [400, 50], 30, 5)

new_composer_button = BasicButton('NEW COMPOSER',[360,80],35,5)
ok_button = BasicButton('OK', [200,70],35,5)
pianist = None
asked = False
index = 0
try:
    f = open('composer.dat','rb')
    list_composers = pickle.load(f)
except:
    list_composers = []
while not gameExit:
    for event in pygame.event.get():
        screen.blit(bg,(0,0))
        if event.type == pygame.QUIT:
            gameExit = True
        if status == 'INIT':
            display(screen,'LIST  COMPOSER', 30,20)
            mouse_position = pygame.mouse.get_pos()
            if is_inside([355,100],[250,250],mouse_position):
                pygame.draw.rect(screen, SILVER1, [350,95,260,260],3)
            for i in range(3):
                if i + index > len(list_composers) - 1 or i + index < 0:
                    continue
                avatar = pygame.transform.scale(pygame.image.load(list_composers[i+index].avatar), (250,250))
                screen.blit(avatar,[55 + i*300, 100])
                name = Label(list_composers[i+index].name,position=[150 + i*300,380])
                name.display(screen)
            new_composer_button.showButton(screen,[300,400],mouse_position)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_inside([300,400],[360,100],mouse_position):
                    compose_name = c.ask(screen, 'Composer\'s Name', [400, 40])
                    if compose_name != None and compose_name != '':
                        status = 'NEW'
                        new_composer = Composer(compose_name, 'Avatar/Unknown.jpeg')
                        avatar = pygame.transform.scale(pygame.image.load(new_composer.avatar), (300, 300))
                        name_composer_label = Label(new_composer.name.upper(), 50, [200, 50])
                if is_inside([355,100],[250,250],mouse_position):
                    status = 'COMPOSE'
                    selected_composer = list_composers[index + 1]
                    avatar = pygame.transform.scale(pygame.image.load(selected_composer.avatar), (300, 300))
                    name_composer_label = Label(selected_composer.name.upper(), 50, [200, 50])
                    l = os.listdir('Musics/' + selected_composer.name)
                if len(list_composers) >= 3 + index and mouse_position[0] > 700:
                    index = index + 1
                if index >= 0 and mouse_position[0] < 260:
                    index = index - 1

        if status == 'COMPOSE':
            mouse_position = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))
            name_composer_label.display(screen)
            pygame.draw.rect(screen, SILVER1, [500, 40, 400, 50])
            display(screen,selected_composer.name.capitalize() + '\'s Music', 620, 50)

            pygame.draw.rect(screen, SILVER, [500, 100, 400, 360])
            pygame.draw.rect(screen, SILVER, [65, 115, 310, 310], 3)
            add_midi_button.showButton(screen, [500, 470], mouse_position)
            screen.blit(avatar, [70, 120])
            if is_inside([500, 100], [400, 360], mouse_position):
                id = int((mouse_position[1] - 100) / 30)
                if id < len(l):
                    pygame.draw.rect(screen,SILVER1,[500,100 + id*30,400,30])

            for i in range(len(l)):
                small_display(screen,l[i],520,108+30*i)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if is_inside([500,470],[400,50],mouse_position):
                    if asked == False:
                        name_of_song = c.ask(screen, 'Name', [400, 40])
                        selected_composer.compose(selected_composer.name + '/' + name_of_song)
                        l = os.listdir('Musics/' + selected_composer.name)
                if mouse_position[0] < 70 :
                    status = 'INIT'
                if is_inside([500,100],[400,360],mouse_position):
                    id = int((mouse_position[1] - 100)/30)
                    if id < len(l):
                        thread = create_thread_play('Musics/' + selected_composer.name + '/' + l[id])
                        thread.start()
                        thread.join()
                        print('PLAYING')
        if status == 'NEW':
            mouse_position = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))
            name_composer_label.display(screen)
            pygame.draw.rect(screen, SILVER1, [500, 40, 400 , 50])
            display(screen,'List SrcMidi',620,50)

            pygame.draw.rect(screen,SILVER,[500,100,400,360])
            pygame.draw.rect(screen,SILVER,[65,115,310,310],3)
            add_midi_button.showButton(screen,[500,470],mouse_position)
            screen.blit(avatar, [70, 120])
            ok_button.showButton(screen,[110,450],mouse_position)
            for i in range(len(new_composer.midi)):
                small_display(screen,new_composer.midi[i],500,100+30*i)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if is_inside([500,470],[400,50],mouse_position):
                    root = tkinter.Tk()
                    filename =  askopenfilename(title = "choose your file")
                    root.update()
                    root.destroy()
                    new_composer.midi.append(filename)

                if is_inside([70,120], [300,300], mouse_position):
                    root = tkinter.Tk()
                    avatar_ = askopenfilename(title = "choose your file")
                    root.update()
                    root.destroy()
                    new_composer.avatar = avatar_
                    avatar = pygame.transform.scale(pygame.image.load(new_composer.avatar), (300, 300))

                if is_inside([110,450], [200,70], mouse_position):
                    list_composers.append(new_composer)
                    pickle.dump(list_composers, open('composer.dat', 'wb'))
                    os.mkdir('Musics/' + new_composer.name)
                    generateModel(new_composer.model,len(new_composer.midi)*20)
                    generateTModel(new_composer.modelt,len(new_composer.modelt)*10)
                    os.mkdir('TempData/' + new_composer.name + 'Midi')
                    os.mkdir('TempData/' + new_composer.name + 'TrainingData')
                    nomalize('', 'TempData/' + new_composer.name + 'Midi', new_composer.midi)
                    generateTrainingData('TempData/' + new_composer.name + 'Midi', 100, 'TempData/' + new_composer.name + 'TrainingData' + '/X', 'TempData/' + new_composer.name + 'TrainingData' + '/Y')
                    generateTTrainingData('TempData/' + new_composer.name + 'Midi', 50, 'TempData/' + new_composer.name + 'TrainingData' + '/XT', 'TempData/' + new_composer.name + 'TrainingData' + '/YT')
                    trainModel(new_composer.model,'TempData/' + new_composer.name + 'TrainingData' + '/X', 'TempData/' + new_composer.name + 'TrainingData' + '/Y', 5, 20)
                    trainModel(new_composer.modelt, 'TempData/' + new_composer.name + 'TrainingData' + '/XT', 'TempData/' + new_composer.name + 'TrainingData' + '/YT', 5, 20)
                    status = 'INIT'

        pygame.display.update()



