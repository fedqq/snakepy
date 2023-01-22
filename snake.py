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
        inCoords = True
        while inCoords:
            x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 2) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 2) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                inCoords = False
        self.coordinates = (x, y)
        self.img = (Image.open("apple.png"))
        self.resized = self.img.resize((SPACE_SIZE, SPACE_SIZE), Image.ANTIALIAS)
        self.new_img = ImageTk.PhotoImage(self.resized)

        canvas.create_image(x,y, anchor=NW, image=self.new_img, tag = "food")
        
        #canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = "#ff2626", tag = "food")
        canvas.pack()
    pass

global snakeEnd
global endImg

global snakeStart
global startImg

def nextTurn(snake, food):
    if dead:
        return
    if paused:
        window.after(DELAY, nextTurn, snake, food)
        return

    (startOldX, startOldY) = snake.coordinates[0]
    x, y = snake.coordinates[0]
    if direction == 'down':
        y += SPACE_SIZE
    elif direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    else:
        x += SPACE_SIZE
    
    CheckCollisions(x, y)
    snake.coordinates.insert(0, (x, y))


    startFileName = ""
    if startOldX > x:
        startFileName = "startLeft.png"
    elif startOldX < x:
        startFileName = "startRight.png"
    elif startOldY < y:
        startFileName = "startDown.png"
    else:
        startFileName = "startUp.png"

    global startImg
    global snakeStart
    startImg = PhotoImage(file = startFileName)
    snakeStart = canvas.create_image(x, y, anchor = NW, image = startImg)

    snake.squares[0] = canvas.create_rectangle(startOldX, startOldY, startOldX + SPACE_SIZE, startOldY + SPACE_SIZE, fill = "#34a8eb", outline = "#33a6e8")
    snake.squares.insert(0, snakeStart)

    if food.coordinates[0] == x and food.coordinates[1] == y:
        global score
        score += 1
        label["text"] = "Score: {}".format(score)
        
        canvas.delete("food")
        food = Food()
    else:     
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        canvas.delete(snake.squares[-2])
        del snake.squares[-1]
        (oldX, oldY) = snake.coordinates[-1]
        global snakeEnd
        global endImg
        fileName = ""
        (nextX, nextY) = snake.coordinates[-2]
        if nextX > oldX:
            fileName = "endLeft.png"
        elif nextX < oldX:
            fileName = "endRight.png"
        elif nextY < oldY:
            fileName = "endDown.png"
        else:
            fileName = "endUp.png"

        endImg = PhotoImage(file = fileName)
        snakeEnd = canvas.create_image(oldX, oldY, anchor = NW, image = endImg, tag = "end")
        snake.squares[-1] = snakeEnd

    if not dead:
        window.after(DELAY, nextTurn, snake, food)


direction = 'down'

def changeDirection(newdirection):
    global direction
    if direction == 'left' and newdirection != 'right':
        direction = newdirection

    if direction == 'right' and newdirection != 'left':
        direction = newdirection

    if direction == 'up' and newdirection != 'down':
        direction = newdirection

    if direction == 'down' and newdirection != 'up':
        direction = newdirection

def CheckCollisions(x, y):
    if (x, y) in snake.coordinates or x > GAME_WIDTH or x < 0 or y > GAME_HEIGHT or y < 0:
        gameOver()

def createBG():
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

global endMenuImg
global restartImg

def gameOver():
    global direction
    global best
    global dead
    global snake

    direction = 'down'

    dead = True
    if score > best:
        best = score
    snake.coordinates.clear()
    snake.squares.clear()
    del snake
    canvas.delete("all")
    createBG()

    global restartImg
    global endMenuImg

    endMenuImg = ImageTk.PhotoImage(file = "endMenu.png")
    canvas.create_image(0, 0, image = endMenuImg, anchor = NW, tag = "rects")

    restartImg = PhotoImage(file = "restartBtn.png")
    canvas.create_image(0, 0, image = restartImg, anchor = NW, tag = "restartBtn")
    
    canvas.create_text(300, 150, text="Score: {}\nBest Score: {}".format(score, best), fill="white", font=('Helvetica 17 bold'), justify = CENTER)
    
def pauseGame():
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
    

def restartGame():
    canvas.delete("all")
    createBG()

    global snake
    global score
    global food
    global dead

    snake = 0
    snake = Snake()
    score = 0
    food = Food()
    dead = False
    nextTurn(snake, food)

def winGame():
    canvas.delete("all")
    global snake
    global food
    del snake
    del food
    canvas.create_text(300, 150, text="GG", fill="white", font=('Helvetica 75 bold'), justify = CENTER, tag = "winText")

global mx
global my

def mouseClick(event):
    global mx
    global my
    if dead:
        mx = event.x
        my = event.y
        if mx > 167 and mx < 429 and my > 447 and my < 507: 
            restartGame()

def posGet(e):
    global mx
    global my
    mx= e.x
    my= e.y

window = Tk()
window.title("Snake")
window.resizable(False, False)
window.configure(bg="#a8d44c")

label = Label(window, text="Score: {}".format(score), font = ("Arial", 30), bg = "#a8d44c", fg = "#ffffff")
label.pack()

canvas = Canvas(window, bg = "#a8d44c", width = GAME_WIDTH, height = GAME_WIDTH, bd = 0, relief=RAISED)

canvas.pack()

createBG()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)

window.bind("<Left>", lambda event: changeDirection('left'))
window.bind("<Right>", lambda event: changeDirection('right'))
window.bind("<Up>", lambda event: changeDirection('up'))
window.bind("<Down>", lambda event: changeDirection('down'))
window.bind("<Return>", lambda event: restartGame())
window.bind("<Escape>", lambda event: pauseGame())

frame = Frame(window, width=600, height=600)
frame.bind("<Button-1>", lambda event: mouseClick(event))
window.bind('<Motion>', lambda event: posGet(event))

snake = Snake()
food = Food()

nextTurn(snake, food)

window.mainloop()