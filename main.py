# Libraries Used
import operator
import tkinter as tk
from tkinter import *
from random import randint
import pickle

# Screen Resolution - 1920*1080
window1=''
MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND
run = True
pause_text = ''
e1=''
FILENAME = "save.pickle"

# Main Class
class Snake(tk.Canvas):
    def __init__(self, name, num):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )

        self.name = name
        self.num = num
        self.previous_values={}
        self.previous_values['name'] = self.name

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]

        self.previous_values['snake_pos']=self.snake_positions

        self.food_position = self.set_new_food_position()
        self.previous_values['direction'] = "Right"
        self.direction = "Right"

        self.previous_values['score'] = 0
        self.score = 0

        if self.num==1:
            self.score = self.name['score']
            self.snake_positions = self.name['snake_pos']
            self.direction = self.name['direction']
            self.name = self.name['name']
        self.load_assets()
        self.create_objects()

        self.bind_all("<Key>", self.on_key_press)

        self.pack()

        self.after(GAME_SPEED, self.perform_actions)

    # Function to load images
    def load_assets(self):
        try:
            self.snake_body = tk.PhotoImage(file="./assets/snake.png")

            self.food = tk.PhotoImage(file="./assets/food.png")
        except IOError as error:
            # root.destroy()
            raise

    # Function to save the state
    def save_state(self):
        try:

            data = {
                "previous": self.previous_values,
            }
            with open(FILENAME, "wb") as f:
                pickle.dump(data, f)
            self.end_game()
        except Exception as e:

            print
            "error saving state:", str(e)

        # root.destroy()

    # Function to create widgets
    def create_objects(self):

        self.create_text(
            35, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    # Function to check the collision
    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    # Function to check collision between snake and food
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            self.previous_values['snake_pos'] = self.snake_positions
            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), *self.food_position)
            self.previous_values['score'] = self.score
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    # Function for decreasing snake length
    def min(self):
        self.delete('snake')
        self.snake_positions = self.snake_positions[:3]
        for x_position, y_position in self.snake_positions:
            self.create_image(
                x_position, y_position, image=self.snake_body, tag="snake"
            )
        self.previous_values['snake_pos'] = self.snake_positions

    # Function for boss key
    def info(self):
        self.pause()
        pad=3
        window = Toplevel()
        window.geometry("{0}x{1}+0+0".format(
            window.winfo_screenwidth()-pad, window.winfo_screenheight()-pad))
        canvas = Canvas(window, width=window.winfo_screenwidth()-pad, height=window.winfo_screenheight()-pad)
        canvas.pack(expand=YES, fill=BOTH)
        window.title("Amazon Web Services")
        self.image = tk.PhotoImage(file="./assets/work.png")
        canvas.create_image( 10, 100, image=self.image)

        window.mainloop()

    # Function to end game
    def end_game(self):
        self.delete(tk.ALL)
        self.previous_values['end']='end'
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14
        )


        file = open("score.txt")
        temp = file.read().splitlines()
        data = {}
        for i in temp:
            d = i.split(',')
            data[d[0]] = int(d[1])
        if self.name in data.keys():
            if self.score>data[self.name]:
                data[self.name]= self.score
                file.close()
                file = open("score.txt", 'w')
                for i in data:
                    file.write(f"{i},{data[i]}\n")
                file.close()

        else:
            file.close()
            file = open("score.txt", 'a')
            file.write(f"{self.name},{self.score}\n")
            file.close()

    # Function for moving snake
    def move_snake(self):
        global run
        if run == True:
            head_x_position, head_y_position = self.snake_positions[0]

            if self.direction == "Left":
                new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
            elif self.direction == "Right":
                new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
            elif self.direction == "Down":
                new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
            elif self.direction == "Up":
                new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

            self.snake_positions = [new_head_position] + self.snake_positions[:-1]
            self.previous_values['snake_pos'] = self.snake_positions

            for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
                self.coords(segment, position)

    # Function for key pressing events
    def on_key_press(self, e):
        new_direction = e.keysym


        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

        if( new_direction == 'd'):
            self.pause()

        if (new_direction == 'a'):
            self.min()

        if (new_direction == 'i'):
            self.info()

        if (new_direction == 's'):
            self.save_state()

    # Function for executing functions
    def perform_actions(self):

        if self.check_collisions():
            self.end_game()

        self.check_food_collision()
        self.move_snake()

        self.after(GAME_SPEED, self.perform_actions)

    # Function to se food positions randomly
    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    # Function to pause game
    def pause(self):
        global run, pause_text
        if run == False:
            run = True
            self.delete(pause_text)
            self.after(GAME_SPEED * 3 + 70, self.move_snake)
        else:
            run = False
            pause_text = self.create_text(302, 250, font='Arial 5', text="Press d to resume", fill='white')


# Function to call snake class
def call_snake(name):
    root = tk.Tk()
    root.title("Snake")
    root.resizable(False, False)
    num=0
    root.after(1, lambda: root.focus_force())
    board = Snake(name, num)
    board.pack()
    root.mainloop()

def call_snake_prev(prev):
    root = tk.Tk()
    root.title("Snake")
    root.resizable(False, False)
    num=1
    root.after(1, lambda: root.focus_force())
    board = Snake(prev,num)
    board.pack()
    root.mainloop()

def start1():
    global e1
    name = e1.get()
    window1.destroy()
    call_snake(name)

def start():
    name = e1.get()
    window.destroy()
    call_snake(name)

def load():
    window.destroy()
    try:
        with open(FILENAME, "rb") as f:
            data = pickle.load(f)
        previous_values = data["previous"]
        call_snake_prev(previous_values)
    except Exception as e:
        print
        "error loading saved state:", str(e)

def load1():
    window1.destroy()
    try:
        with open(FILENAME, "rb") as f:
            data = pickle.load(f)
        previous_values = data["previous"]
        call_snake_prev(previous_values)
    except Exception as e:
        print
        "error loading saved state:", str(e)



# Function for building main screen
window=tk.Tk()
window.geometry("600x620")
window.title("Snake Game")
l1=Label(window,text="Enter Name",font="times 12", width=15, padx=10, pady=10)
l1.grid(row=1,column=2,columnspan=2)
name_text=StringVar()
e1=Entry(window,textvariable=name_text, width=40)
e1.grid(row=1,column=4)

def show(n):
    file = open("score.txt", 'a')
    file.close()
    file = open("score.txt")
    temp = file.read().splitlines()
    if temp != []:
        rows = len(temp) + 1
        cols = len(temp[0].split(','))

        data = {}

        for i in temp:
            d = i.split(',')
            data[d[0]] = int(d[1])

        data = dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))

        count = 0
        e = Entry(window, width=20, fg='Black',
                  font=('Arial', 16))
        e.grid(row=count + 20, column=3)
        e.insert(END, 'Name')
        e = Entry(window, width=20, fg='Black',
                  font=('Arial', 16))
        e.grid(row=count + 20, column=4)
        e.insert(END, 'Score')
        count = count + 1

        for j in data:
            e = Entry(window, width=20, fg='Black',
                      font=('Arial', 16))
            e.grid(row=count + 20, column=3)
            e.insert(END, j)
            e = Entry(window, width=20, fg='Black',
                      font=('Arial', 16))
            e.grid(row=count + 20, column=4)
            e.insert(END, data[j])
            count = count + 1


def clear():
    file = open("score.txt", 'w')
    file.write('')
    file.close()
    window.destroy()
    create()


def create():
    global window1
    window1 = tk.Tk()
    window1.geometry("600x620")
    window1.title("Snake Game")
    l1 = Label(window1, text="Enter Name", font="times 12", width=15, padx=10, pady=10)
    l1.grid(row=1, column=2, columnspan=2)
    name_text = StringVar()
    global e1
    e1 = Entry(window1, textvariable=name_text, width=40)
    e1.grid(row=1, column=4)

    b1 = Button(window1, text="Start Game", width=10, command=start1)
    b1.grid(row=30, column=3)

    b2 = Button(window1, text="Load Game", width=10, command=load1)
    b2.grid(row=30, column=4)

    e = Entry(window1, width=22, fg='Black',
              font=('Arial', 12))
    e.grid(row=40, column=3)
    e.insert(END, 'Pause')
    e = Entry(window1, width=20, fg='Black',
              font=('Arial', 12))
    e.grid(row=40, column=4)
    e.insert(END, 'Press d')

    e = Entry(window1, width=22, fg='Black',
              font=('Arial', 12))
    e.grid(row=41, column=3)
    e.insert(END, 'Decrease Length of snake')
    e = Entry(window1, width=20, fg='Black',
              font=('Arial', 12))
    e.grid(row=41, column=4)
    e.insert(END, 'Press a')

    e = Entry(window1, width=22, fg='Black',
              font=('Arial', 12))
    e.grid(row=42, column=3)
    e.insert(END, 'Save State')
    e = Entry(window1, width=20, fg='Black',
              font=('Arial', 12))
    e.grid(row=42, column=4)
    e.insert(END, 'Press s')

    e = Entry(window1, width=22, fg='Black',
              font=('Arial', 12))
    e.grid(row=43, column=3)
    e.insert(END, 'Big Boss Key')
    e = Entry(window1, width=20, fg='Black',
              font=('Arial', 12))
    e.grid(row=43, column=4)
    e.insert(END, 'Press i')

    window1.mainloop()


show(0)



b1=Button(window,text= "Start Game" ,width=10, command=start)
b1.grid(row=30,column=3)

b2=Button(window,text= "Load Game" ,width=10, command=load)
b2.grid(row=30,column=4)

b2=Button(window,text= "Clear Scores" ,width=10, command=clear)
b2.grid(row=31,column=4)


e = Entry(window, width=22, fg='Black',
          font=('Arial', 12))
e.grid(row=40, column=3)
e.insert(END, 'Pause')
e = Entry(window, width=20, fg='Black',
          font=('Arial', 12))
e.grid(row=40, column=4)
e.insert(END, 'Press d')

e = Entry(window, width=22, fg='Black',
          font=('Arial', 12))
e.grid(row=41, column=3)
e.insert(END, 'Decrease Length of snake')
e = Entry(window, width=20, fg='Black',
          font=('Arial', 12))
e.grid(row=41, column=4)
e.insert(END, 'Press a')

e = Entry(window, width=22, fg='Black',
          font=('Arial', 12))
e.grid(row=42, column=3)
e.insert(END, 'Save State')
e = Entry(window, width=20, fg='Black',
          font=('Arial', 12))
e.grid(row=42, column=4)
e.insert(END, 'Press s')


e = Entry(window, width=22, fg='Black',
          font=('Arial', 12))
e.grid(row=43, column=3)
e.insert(END, 'Big Boss Key')
e = Entry(window, width=20, fg='Black',
          font=('Arial', 12))
e.grid(row=43, column=4)
e.insert(END, 'Press i')



window.mainloop()

