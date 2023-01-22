from tkinter import *
from PIL import ImageTk, Image
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
DELAY = 80
SPACE_SIZE = 20
BODY_PARTS = 5

score = 0
best = 0
dead = False
paused = False
direction = 'down'
end_image = 0
restart_image = 0
button = 0
snake_end = 0
end_image = 0
snake_start = 0
start_image = 0

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = "#b0d454", tag = "snake", outline = "#b0d454")
            self.squares.append(square)

class Food:
    def __init__(self):
        on_snake = True
        while on_snake:
            x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 2) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 2) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                on_snake = False
        self.coordinates = (x, y)

        self.img = (Image.open("apple.png"))
        self.resized = self.img.resize((SPACE_SIZE, SPACE_SIZE), Image.ANTIALIAS)
        self.new_img = ImageTk.PhotoImage(self.resized)
        canvas.create_image(x,y, anchor=NW, image=self.new_img, tag = "food")
        canvas.pack()

def next_turn(snake, food):
    global score
    global start_image
    global snake_start
    global snake_end
    global end_image

    if dead or paused:
        if paused:
            window.after(DELAY, next_turn, snake, food)
        return

    old_start = snake.coordinates[0]
    x, y = snake.coordinates[0]
    if direction == 'down':
        y += SPACE_SIZE
    elif direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    else:
        x += SPACE_SIZE
    
    check_collisions(x, y)
    snake.coordinates.insert(0, (x, y))

    start_file_name = ""
    if old_start[0] > x:
        start_file_name = "startLeft.png"
    elif old_start[0] < x:
        start_file_name = "startRight.png"
    elif old_start[1] < y:
        start_file_name = "startDown.png"
    else:
        start_file_name = "startUp.png"

    start_image = PhotoImage(file = start_file_name)
    snake_start = canvas.create_image(x, y, anchor = NW, image = start_image)

    snake.squares[0] = canvas.create_rectangle(old_start[0], old_start[1], old_start[0] + SPACE_SIZE, old_start[1] + SPACE_SIZE, fill = "#34a8eb", outline = "#33a6e8")
    snake.squares.insert(0, snake_start)

    if food.coordinates[0] == x and food.coordinates[1] == y:
        score += 1
        label["text"] = "Score: {}".format(score)
        
        canvas.delete("food")
        food = Food()
    else:     
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        canvas.delete(snake.squares[-2])
        del snake.squares[-1]
        old_end = snake.coordinates[-1]
        fileName = ""
        next_coords = snake.coordinates[-2]

        if next_coords[0] > old_end[0]:
            fileName = "endLeft.png"
        elif next_coords[0] < old_end[0]:
            fileName = "endRight.png"
        elif next_coords[1] < old_end[1]:
            fileName = "endDown.png"
        else:
            fileName = "endUp.png"

        end_image = PhotoImage(file = fileName)
        snake_end = canvas.create_image(old_end[0], old_end[1], anchor = NW, image = end_image, tag = "end")
        snake.squares[-1] = snake_end

    window.after(DELAY, next_turn, snake, food)

def change_direction(newdirection):
    global direction

    if direction == 'left' and newdirection != 'right':
        direction = newdirection

    if direction == 'right' and newdirection != 'left':
        direction = newdirection

    if direction == 'up' and newdirection != 'down':
        direction = newdirection

    if direction == 'down' and newdirection != 'up':
        direction = newdirection

def check_collisions(x, y):
    if (x, y) in snake.coordinates or x > GAME_WIDTH or x < 0 or y > GAME_HEIGHT or y < 0:
        end()

def check_win():
    if score == (GAME_WIDTH / SPACE_SIZE) * (GAME_HEIGHT / SPACE_SIZE):
        win()

def create_bg():
    fillType = 0
    for height in range(int(GAME_HEIGHT / SPACE_SIZE)):
        if fillType == 0:
                fillType = 1
        else:
            fillType = 0
        for width in range(int(GAME_WIDTH / SPACE_SIZE)):
            x = width * SPACE_SIZE
            y = height * SPACE_SIZE
            if fillType == 0:
                canvas.create_rectangle(x, y, x + SPACE_SIZE + 10, y + SPACE_SIZE + 10, fill = "#a8d44c", outline = "#b0d454")
                fillType = 1
            else:
                canvas.create_rectangle(x, y, x + SPACE_SIZE + 10, y + SPACE_SIZE + 10, fill = "#b0d454", outline = "#b0d454")
                fillType = 0

def end():
    global direction
    global best
    global dead
    global snake
    global button
    global restart_image
    global end_image

    direction = 'down'
    dead = True

    if score > best:
        best = score
    snake.coordinates.clear()
    snake.squares.clear()
    del snake
    canvas.delete("all")
    create_bg()

    end_image = ImageTk.PhotoImage(file = "endMenu.png")
    canvas.create_image(0, 0, image = end_image, anchor = NW, tag = "rects")

    restart_image = PhotoImage(file = "restartBtn.png")
    button = Button(canvas, image = restart_image, bd = 0, padx = 0, pady = 0, borderwidth = 0, command = lambda: restart())
    button.place(x = GAME_WIDTH / 2 - 137, y = 460)
    
    canvas.create_text(300, 150, text="Score: {}\nBest Score: {}".format(score, best), fill="white", font=('Helvetica 17 bold'), justify = CENTER)
    
def pause():
    global dead
    global paused

    if dead:
        return
    if paused:
        paused = False
        canvas.delete("pausedText")
    else:
        paused = True
        canvas.create_text(300, 150, text="Press Esc To Unpause", fill="white", font=('Helvetica 17 bold'), justify = CENTER, tag = "pausedText")
    
def restart():
    global snake
    global score
    global food
    global dead
    global button

    button.destroy()
    del button

    canvas.delete("all")
    create_bg()

    snake = 0
    snake = Snake()
    score = 0
    food = Food()
    dead = False

    next_turn(snake, food)

def win():
    global snake
    global food

    canvas.delete("all")
    del snake
    del food
    canvas.create_text(300, 150, text="GG", fill="white", font=('Helvetica 75 bold'), justify = CENTER, tag = "winText")

window = Tk()
window.title("Snake")
window.resizable(False, False)
window.configure(bg="#a8d44c")

label = Label(window, text="Score: {}".format(score), font = ("Arial", 30), bg = "#a8d44c", fg = "#ffffff")
label.pack()

canvas = Canvas(window, bg = "#a8d44c", width = GAME_WIDTH, height = GAME_WIDTH, bd = 0, relief=RAISED)
canvas.pack()

create_bg()

window.update()

window.bind("<Left>", lambda event: change_direction('left'))
window.bind("<Right>", lambda event: change_direction('right'))
window.bind("<Up>", lambda event: change_direction('up'))
window.bind("<Down>", lambda event: change_direction('down'))
window.bind("<Return>", lambda event: restart())
window.bind("<Escape>", lambda event: pause())

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()