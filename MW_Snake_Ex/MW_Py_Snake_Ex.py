from tkinter import *
import pygame
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"

#initializing pygame
pygame.init()
#initializing mixer (sound)
pygame.mixer.init()


eat_sound = pygame.mixer.Sound('OOT_Get_Rupee.wav')
game_over_sound = pygame.mixer.Sound('Batman 1 Life lost.mp3')
background_music = pygame.mixer.Sound('The Midnight Sunset Official Audio.mp3')

class Snake:

#constructor, with body size, coordinates, and squares
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
#list of coordinates, snake will appear top left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE

        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

        eat_sound.play()


def next_turn(snake, food):

    x, y = snake.coordinates[0]
#y deals with vertical, x for horizontal
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)


    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()



    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

#direction
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("Game Over")
        return True
    elif y < 0 or y >+ GAME_HEIGHT:
        print("Game Over")
        return True

    #checking to see if we have matching coordinates.
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game Over")
            return True

    return False







def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
        font=('consolas', 70), text="Game Over", fill="red", tag="gameover")
    game_over_sound.play()

window = Tk()
window.title("I'm a snakkkkkeee")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

#the x and y we pass below can't be floats
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#movement with player input

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))



snake = Snake()
food = Food()

next_turn(snake, food)

background_music.play()

window.mainloop()