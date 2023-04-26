# game based on Christian Thompson tutorial

from asyncio.windows_events import NULL
import turtle
import winsound

class Scoreboard(turtle.Turtle):
    score_Left = 0    #score of player 1
    score_Right = 0    #score of player 2
    
    def __init__(self):
        super().__init__()

    #sets the scores back to zero
    def zero_Score(self):
        self.score_Left = 0
        self.score_Right = 0
    
    #updates the score and writes it again
    def score_Up(self, player):
        if player == "left":
            self.score_Left = self.score_Left + 1
        else:
            self.score_Right = self.score_Right + 1
        self.clear()
        self.write("Player 1: {}    Player 2: {}".format(self.score_Left, self.score_Right), align = "center", font = ("Courier", 24, "normal"))
    

class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        
    #moving methods
    def move_Paddle_Up(self):
        y = self.ycor()
        if y > (290 - 50):
            return 
        y = y + 20
        self.sety(y)

    def move_Paddle_Down(self):
        y = self.ycor()
        if y < (-290 + 50):
            return 
        y = y - 20
        self.sety(y)


class Ball(turtle.Turtle):
    default_Ball_Speed = 0.2

    def __init__(self):
        super().__init__()

    #moving the ball
    def move_Ball(self, in_Menu):
        if in_Menu == True:    #if its in menu, it does not move the ball
            return
        self.setx(self.xcor() + self.dx)    #ball moves +2px every game loop        
        self.sety(self.ycor() + self.dy)    #ball moves +2px every game loop

    #adjust ball movement speed
    def increase_Ball_Speed(self):
        if (float(self.dx) + 0.05 < 0) or (float(self.dx) + 0.05 > 5):
            return
        self.dx = float(self.dx) + 0.05
        self.dy = self.dx
        print("DX {}".format(self.dx))
        print("DY {}".format(self.dy))

    def decrease_Ball_Speed(self):
        if (float(self.dx) - 0.05 < 0) or (float(self.dx) - 0.05 > 5):
            return
        self.dx = float(self.dx) - 0.05
        self.dy = self.dx
        print("DX {}".format(self.dx))
        print("DY {}".format(self.dy))

    def reset_Ball_Speed(self):
        self.dx = self.default_Ball_Speed
        self.dy = self.default_Ball_Speed


class Menu(turtle.Turtle):
    def __init__(self):
        super().__init__()

    #show the game menu
    def show(self):
        self.write("          PONG\n\n1   -> New Game\n2   -> Continue Game\n+   -> Increase ball speed\n-   -> Decrease ball speed\nr   -> Reset ball speed\nEsc -> Open menu\nq   -> Quit", align = "center", font = ("Courier", 24, "bold"))

class Game_Controller():
    #creates all atributes
    window = NULL
    scoreboard = NULL
    menu = NULL
    paddle_Left = NULL
    paddle_Right = NULL
    ball = NULL
    quit = False
    in_Menu = True
    
    def __init__(self):
        pass

    #creates the window for the game
    def create_Window(self):
        self.window = turtle.Screen()
        self.window.title("Pong")
        self.window.bgcolor("black")
        self.window.setup(width = 800, height = 600)
        self.window.tracer(0)        

    #creates the score board
    def create_Scoreboard(self):
        self.scoreboard = Scoreboard()
        self.scoreboard.color("white")
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(0, 260)
        self.scoreboard.write("Player 1: {}    Player 2: {}".format(self.scoreboard.score_Left, self.scoreboard.score_Right), align = "center", font = ("Courier", 24, "normal"))
    
    #creates the menu
    def create_Menu(self):
        self.menu = Menu()
        self.menu.speed(0)
        self.menu.color("white")
        self.menu.penup()
        self.menu.hideturtle()
        self.menu.goto(0, -50)

    #creates the paddles and the ball
    def create_Game_Objects(self):
        #left paddle
        self.paddle_Left = Paddle()
        self.paddle_Left.speed(0)    #animation speed
        self.paddle_Left.shape("square")
        self.paddle_Left.shapesize(stretch_wid = 5, stretch_len = 1)
        self.paddle_Left.color("white")
        self.paddle_Left.penup()
        self.paddle_Left.goto(-350, 0)

        #right paddle
        self.paddle_Right = Paddle()
        self.paddle_Right.speed(0)    #animation speed
        self.paddle_Right.shape("square")
        self.paddle_Right.shapesize(stretch_wid = 5, stretch_len = 1)
        self.paddle_Right.color("white")
        self.paddle_Right.penup()
        self.paddle_Right.goto(350, 0)

        #ball
        self.ball = Ball()
        self.ball.speed(0)    #animation speed
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, 0)
        self.ball.dx = self.ball.default_Ball_Speed    #ball moves by 0.2px in x axis
        self.ball.dy = self.ball.default_Ball_Speed    #ball moves by 0.2px in y axis

    #checks if ball hits borders
    def check_Border(self):
        if self.in_Menu == True:    #if its in menu, skips the checking
            return
        if self.ball.ycor() > 290:    #hits the top border
            self.ball.sety(290)
            self.ball.dy = self.ball.dy * (-1)
            winsound.PlaySound("bounce_border.wav", winsound.SND_ASYNC)
        if self.ball.ycor() < -290:    #hits the bottom border
            self.ball.sety(-290)
            self.ball.dy = self.ball.dy * (-1)
            winsound.PlaySound("bounce_border.wav", winsound.SND_ASYNC)
        if self.ball.xcor() > 390:    #player 1 scores
            self.ball.goto(0, 0)
            self.ball.dx = self.ball.dx * (-1)
            self.scoreboard.score_Up("left")
            winsound.PlaySound("score_up.wav", winsound.SND_ASYNC)
        if self.ball.xcor() < -390:    #player 2 scores
            self.ball.goto(0, 0)
            self.ball.dx = self.ball.dx * (-1)
            self.scoreboard.score_Up("right")
            winsound.PlaySound("score_up.wav", winsound.SND_ASYNC)
    
    #paddle collision checking
    def check_Paddle_Collision(self):
        if self.in_Menu == True:    #if its in menu, skips the checking
            return
        #paddle_Left colision checking
        if self.ball.xcor() <= self.paddle_Left.xcor() and (self.ball.ycor() <= self.paddle_Left.ycor() + 60 and self.ball.ycor() >= self.paddle_Left.ycor() - 60):
            self.ball.setx(-340)
            self.ball.dx = self.ball.dx * (-1)
            winsound.PlaySound("bounce_paddle.wav", winsound.SND_ASYNC)
            return
        #paddle_Right colision checking
        if self.ball.xcor() >= self.paddle_Right.xcor() and (self.ball.ycor() <= self.paddle_Right.ycor() + 60 and self.ball.ycor() >= self.paddle_Right.ycor() - 60):
            self.ball.setx(340)
            self.ball.dx = self.ball.dx * (-1)
            winsound.PlaySound("bounce_paddle.wav", winsound.SND_ASYNC)
    
    def quit_Game(self):
        self.quit = True

    def show_Menu(self):
        self.in_Menu = True
        self.paddle_Left.hideturtle()
        self.paddle_Right.hideturtle()
        self.ball.hideturtle()
        self.scoreboard.clear()
        self.menu.clear()
        self.menu.show()
        winsound.PlaySound("menu_open.wav", winsound.SND_ASYNC)

    def new_Game(self):
        self.in_Menu = False
        self.ball.goto(0, 0)
        self.paddle_Left.goto(-350, 0)
        self.paddle_Right.goto(350, 0)
        self.scoreboard.zero_Score()
        self.ball.dx = self.ball.default_Ball_Speed
        self.ball.dy = self.ball.default_Ball_Speed
        self.menu.clear()
        self.scoreboard.clear()
        self.scoreboard.write("Player 1: {}    Player 2: {}".format(self.scoreboard.score_Left, self.scoreboard.score_Right), align = "center", font = ("Courier", 24, "normal"))
        self.paddle_Left.showturtle()
        self.paddle_Right.showturtle()
        self.ball.showturtle()
        winsound.PlaySound("menu_close.wav", winsound.SND_ASYNC)
        
    def continue_Game(self):
        self.in_Menu = False
        self.menu.clear()
        self.scoreboard.clear()
        self.scoreboard.write("Player 1: {}    Player 2: {}".format(self.scoreboard.score_Left, self.scoreboard.score_Right), align = "center", font = ("Courier", 24, "normal"))
        self.paddle_Left.showturtle()
        self.paddle_Right.showturtle()
        self.ball.showturtle()
        winsound.PlaySound("menu_close.wav", winsound.SND_ASYNC)

    def read_Keyboard(self):
        self.window.listen()
        self.window.onkeypress(self.paddle_Left.move_Paddle_Up, "w")    #moves paddle_Left up when "w" is pressed
        self.window.onkeypress(self.paddle_Left.move_Paddle_Down, "s")    #moves paddle_Left up when "s" is pressed
        self.window.onkeypress(self.paddle_Right.move_Paddle_Up, "Up")    #moves paddle_Right up when up arrow is pressed
        self.window.onkeypress(self.paddle_Right.move_Paddle_Down, "Down")    #moves paddle_Right up when down arrow is pressed
        self.window.onkeypress(self.new_Game, "1")    #starts a new game when "1" is pressed
        self.window.onkeypress(self.continue_Game, "2")    #continues game when "2" is pressed
        self.window.onkeypress(self.ball.increase_Ball_Speed, "+")    #increases the speed of the ball
        self.window.onkeypress(self.ball.decrease_Ball_Speed, "-")    #decreases the speed of the ball
        self.window.onkeypress(self.ball.reset_Ball_Speed, "r")    #reset the speed of the ball
        self.window.onkeypress(self.quit_Game, "q")    #closes game when "q" is pressed
        self.window.onkeypress(self.show_Menu, "Escape")    #opens menu when "esc" is pressed

    def game_Loop(self):
        while self.quit == False:
            self.window.update()
            self.ball.move_Ball(self.in_Menu)
            self.check_Border()
            self.check_Paddle_Collision()

    def play_Game(self):
        self.create_Window()
        self.create_Menu()
        self.create_Scoreboard()
        self.create_Game_Objects()
        self.show_Menu()
        self.read_Keyboard()
        self.game_Loop()


game = Game_Controller()
game.play_Game()