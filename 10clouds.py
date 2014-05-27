#!/usr/bin/env python
# encoding: utf-8


# description
# 10 Clouds is a small game about climbing a pipe and collecting clouds.
# Player collects clouds by switching sides of the pipe.
# Each cloud represents 1 of 10 values I stand by.
# Game is very short and easy.
# The purpose is to showcase those values in an interesting and engaging way.
# Have fun.


# imports
import pygame, random, time, math
from pygame import display
from pygame import key
from pygame.locals import QUIT


# classes
class Player():
    '''
    Player class.

    switch_position - changes player's position
    draw - displays the player on the screen

    '''


    def __init__(self, position=0, position_x=123, position_y=360):
        '''
        Player class constructor.

        position - describes left/right position to the pipe
        position_x - stands for x position
        position_y - stands for y position

        '''

        # left/right position
        self.position = position

        # x position
        self.position_x = position_x

        # y position
        self.position_y = position_y


    def switch_position(self):
        '''
        Switches player's position on the screen.
        0 stands for left, 1 for right

        '''

        if self.position:
            self.position = 0
            self.position_x = 123

        else:
            self.position = 1
            self.position_x = 164


    def draw(self):
        '''
        Draws the player on the screen.

        '''


        # display player placed on the right side
        if self.position:
            screen.blit(player_right_img, (self.position_x, self.position_y))

        # display player placed on the left side
        else:
            screen.blit(player_left_img, (self.position_x, self.position_y))


class Pipe():
    '''
    Pipe class.

    draw - displays pipe on the screen

    '''


    def __init__(self, position_x=155, position_y=0):
        '''
        Pipe class constructor.

        position_x - x position
        position_y - y position
        current_time - gets the current time with time.time()

        '''

        # x position
        self.position_x = position_x

        # y position
        self.position_y = position_y

        # current time
        self.current_time = time.time()


    def draw(self, data_obj):
        '''
        Displays pipe on the screen.
        Updates position_y.

        '''

        if self.position_y >= HEIGHT:
            self.position_y = -HEIGHT


        self.position_y += data_obj.speed

        screen.blit(pipe_img, (self.position_x, self.position_y))


class Cloud():
    '''
    Cloud class.

    draw - displays the cloud on the screen
    spawn - spawns the cloud

    '''


    def __init__(self, position_x=0, position_y=0, collided=0):
        '''
        Cloud class constructor.

        '''

        # position x
        self.position_x = position_x

        # position y
        self.position_y = position_y

        # stands for collision status
        self.collided = collided

        # spawns a cloud
        self.spawn()


    def draw(self, data_obj):
        '''
        Display a cloud.

        '''

        if self.position_y >= HEIGHT:
            self.spawn()


        self.position_y += data_obj.speed


        if self.collided == 0:
            screen.blit(cloud_img, (self.position_x, self.position_y))


    def spawn(self):
        '''
        Spawn a cloud.

        '''


        self.position_y = -42

        self.collided = 0

        position = random.randint(0, 1)

        if position:
            self.position_x = 113

        else:
            self.position_x = 164


class Data():
    '''
    Data class stores all the data about currently played session.


    - __init__ - constructor,
    - collected_cloud -

    '''


    def __init__(self, screen_mode=0, gamestate=1, clouds=0, mute=0, bottom_pos=388, speed=1):
        '''
        Data class constructor.

        screen_mode - defines whether to display the game in windowed or fullscreen
        gamestate - current game state
        clouds - number of collected clouds

        '''


        # 2 modes, 0 - 'windowed', 1 - 'fullscreen'
        self.screen_mode = screen_mode

        # 3 game states, 1 - main menu, 2 - gameplay, 3 - summary
        self.gamestate = gamestate

        # number of collected clouds, gets increased upon collecting a cloud
        self.clouds = clouds

        # mute all sound effects
        self.mute = mute

        # y position of 'bottom' image in main menu
        self.bottom_pos = bottom_pos

        # speed of gameplay, how fast objects are moving
        self.speed = speed


        #
        self.current_time = time.time()


    def collected_cloud(self):
        '''
        Increases the number of collected clouds.
        Function gets called upon player colliding with a cloud.

        '''


        self.clouds += 1


# functions
def get_user_input(data_obj, player_obj):
    '''
    Collects all user input and decides what to do with it.
    Current game state is taken into consideration.

    Focuses on:
    - pressing 'space' button(game interaction)
    - pressing 'escape' button(switches screen modes)
    - clicking on window's 'X' button(handles quit event)

    '''


    # detecting player interaction, user input
    for event in pygame.event.get():
        # if keys are pressed
        if event.type == 2:
            # pressing 'space' defines all user interactions
            if pygame.key.name(event.key) == "space":
                # play this sound every time 'space' is pressed
                if data_obj.mute == 0:
                    press_space_sound.play(loops=0, maxtime=0, fade_ms=0)

                if data_obj.gamestate == 1:
                    print("GAMESTATE 1")
                    # when space is pressed go to game state 2
                    data_obj.gamestate = 2

                elif data_obj.gamestate == 2:
                    print("GAMESTATE 2")
                    # when space is pressed switch player's position
                    player_obj.switch_position()
                    #data_obj.gamestate = 3

                elif data_obj.gamestate == 3:
                    # when space is pressed go to game state 1
                    print("GAMESTATE 3")
                    data_obj.gamestate = 1

            # pressing 'escape' changes screen mode
            if  pygame.key.name(event.key) == "escape":
                if data_obj.screen_mode == 0:
                    canvas = display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

                    data_obj.screen_mode = 1

                else:
                    canvas = display.set_mode((WIDTH, HEIGHT), 0, 16)

                    data_obj.screen_mode = 0


            # pressing 'm' mutes all sounds
            if pygame.key.name(event.key) == "m":
                if data_obj.mute == 0:
                    pygame.mixer.Sound.stop(background_music)

                    data_obj.mute = 1

                else:
                    pygame.mixer.Sound.play(background_music)

                    data_obj.mute = 0


        # handling quit event when user clicks window's 'X' button
        if event.type is QUIT:
            pygame.quit()
            exit()


def collision(data_obj, player_obj, cloud_obj):
    '''
    Detect collision between a player_obj and cloud_obj.

    '''


    if cloud_obj.position_y >= player_obj.position_y and cloud_obj.position_y <= player_obj.position_y + 22:
        if cloud_obj.position_x <= player_obj.position_x and cloud_obj.collided != 1:
            cloud_obj.collided = 1

            data_obj.collected_cloud()


def update_game(data_obj, player_obj, cloud_obj):
    '''

    '''

    # main menu
    if data_obj.gamestate == 1:
        data_obj.bottom_pos = 388
        data_obj.speed = 0.5

    # gameplay
    elif data_obj.gamestate == 2:
        # make bottom go away
        if data_obj.bottom_pos < HEIGHT:
            data_obj.bottom_pos += 0.5

        # increase game's speed
        if data_obj.speed <= 1.5:
            data_obj.speed += 0.0001

        collision(data_obj, player_obj, cloud_obj)

        if data_obj.clouds == 10:
            data_obj.gamestate = 3

    # summary
    elif data_obj.gamestate == 3:
        data_obj.bottom_pos = 388


def display_content(data_obj, player_obj, pipe_obj1, pipe_obj2, cloud_obj):
    '''
    Displays all of the content

    '''

    # fill the screen with background color
    canvas.fill((123, 197, 205))


    # display bottom
    screen.blit(bottom_img, (0, data_obj.bottom_pos))


    # display content when in main menu game state
    if data_obj.gamestate == 1:
        # display menu info
        screen.blit(main_menu_img, (20, 20))

    # display content when in gameplay game state
    elif data_obj.gamestate == 2:
        # display the pipe
        pipe_obj1.draw(data_obj)
        pipe_obj2.draw(data_obj)

        player_obj.draw()

        cloud_obj.draw(data_obj)

    # display content when in summary game state
    elif data_obj.gamestate == 3:
        # display summary
        screen.blit(summary_img, (20, 20))


    # update display
    display.update()


def main():
    '''
    Main function of the game, contains the main gameplay loop.
    Takes care of everything: user input, logic, displaying content, etc.

    Runs 3 main functions that represent
    - get_user_input(data_obj, player_obj)
    - update_game(data_obj)
    - display_content(data_obj)

    Game states:
    - 1, main menu
    - 2, gameplay
    - 3, summary

    '''


    # create an object to store all information about currently played session
    data = Data()

    # create a player object
    player = Player()

    # create pipe objects
    pipe1 = Pipe(155, -HEIGHT)
    pipe2 = Pipe(155, 0)

    # create a cloud object
    cloud = Cloud()

    # start playing background music
    background_music.play(loops=-1, maxtime=0, fade_ms=0)


    # main loop
    while True:
        # run main menu function(data.gamestate = 1)
        get_user_input(data, player)

        # run main gameplay loop(data.gamestate = 2)
        update_game(data, player, cloud)

        # run summary function(data.gamestate = 3)
        display_content(data, player, pipe1, pipe2, cloud)


# GLOBALS
WIDTH = 320
HEIGHT = 480


# setup pygame
pygame.init()
canvas = display.set_mode((WIDTH, HEIGHT), 0, 16)
display.set_caption('10 Clouds')
screen = pygame.display.get_surface()


# load sound
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# space press sound
press_space_sound = pygame.mixer.Sound("press_space.wav")

# collect cloud sound
collect_cloud_sound = pygame.mixer.Sound("collect_cloud.wav")

# background music
background_music = pygame.mixer.Sound("background_music.wav")


# load images
# bottom for use in main menu
bottom_img = pygame.image.load("bottom.png")

# main menu info
main_menu_img = pygame.image.load("main_menu.png")

# summary
summary_img = pygame.image.load("summary.png")

# pipe
pipe_img = pygame.image.load("pipe.png")

# player
player_left_img = pygame.image.load("player_left.png")
player_right_img = pygame.image.load("player_right.png")

# cloud
cloud_img = pygame.image.load("cloud.png")


# run the main function
main()