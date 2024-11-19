import pygame
from random import randint
from tkinter import messagebox
from time import sleep
pygame.init()
screen_width=1550
screen_height=800 
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Jumping Game")
cloud_surf=pygame.image.load(r"C:\Users\Computer Makah\Pictures\images\cloud.jpg")
player_s_surf=pygame.image.load(r"C:\Users\Computer Makah\Pictures\images\standing.png")
player_r_surf=pygame.image.load(r"C:\Users\Computer Makah\Pictures\images\R1.png")
player_l_surf=pygame.image.load(r"C:\Users\Computer Makah\Pictures\images\L1.png")
score_font=pygame.font.SysFont("Algerian",25,True)
game_over_font=pygame.font.SysFont("Algerian",40,True)
clock=pygame.time.Clock()
# *********************************

class Player():
    def __init__(self,x,y,x_step,max_speed,surf,down_step):
        self.x=x
        self.y=y
        self.x_step=x_step
        self.max_speed=max_speed
        self.speed=self.max_speed
        self.score=0
        self.surf=surf
        self.down_step=down_step
        self.rect=self.surf.get_rect(topleft=(self.x,self.y))
        self.rect_color="black"
        self.height=self.rect.bottom-self.rect.top
        self.is_jumping=False
        self.keep_running=True

    def update_rect(self):
        self.rect=self.surf.get_rect(topleft=(self.x,self.y))

    def check_move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right<screen_width:
            self.x += self.x_step
            self.surf=player_r_surf
        if keys[pygame.K_LEFT] and self.rect.left>0:
            self.x -= self.x_step
            self.surf=player_l_surf
        self.update_rect()

    def move_down(self):
        if not self.is_jumping:
            self.y+=self.down_step
    
    def check_jump(self):
        keys=pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping :
            self.is_jumping=True
        if self.is_jumping:
            self.speed-=1
            if self.speed>-1*self.max_speed:
                if self.speed>0:
                    sign=1
                else:
                    sign=-1
                self.y-=sign*pow(self.speed,2)
            else:
                self.speed=self.max_speed
                self.is_jumping=False
    def check_crash_bottom(self):
        if self.rect.bottom > screen_height:
            global lines_list
            text=game_over_font.render("Game Over",True,"red")
            screen.blit(text,(screen_width//2-100,screen_height//2-20))
            self.keep_running=False
            pygame.display.update()
            sleep(1)
            msg=messagebox.askyesno("Restart","Do you want to restart the game")
            if msg == True:
                initialize_vars()
            else:
                messagebox.showinfo("Eng Game","We hope you enjoyed the game")
                quit()

    def draw_rect(self):
        pygame.draw.rect(screen,self.rect_color,self.rect,2)


    def draw_score(self):
        score_surf=score_font.render(f"Score: {int(self.score)}",True,"magenta")
        screen.blit(score_surf,(screen_width-200,20))
        self.score+=1/60
    
    def check_on_line(self):
        global lines_list
        for line in lines_list:
            if line.color != "red":
                if (self.rect.left >= line.x ) and (self.rect.right <= line.x+line.length):
                    # print("case 1 happened")
                    if self.rect.bottom - line.y < 3:
                        line.color="red"
                        self.speed = self.max_speed
                        self.y=line.y-self.height+55
                        self.rect_color="magenta"
                        self.down_step=line_y_step
        
        



# ***********************************************
class Line():
    def __init__(self,x,y,y_step,length,width,color) :
        self.x=x
        self.y=y    
        self.y_step=y_step
        self.length=length
        self.width=width
        self.color=color
    
    def move(self):
        self.y+=self.y_step
    

# ***********************************************
def check_events():
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                quit()

# *****************************************
def draw_lines():
    global lines_list,max_lines,lines_counter,line_y_step,add_counter
    if len(lines_list)<max_lines:
        if lines_counter == add_counter:
            lines_list.append(Line(randint(100,screen_width-200),0,line_y_step,120,3,"black"))
            lines_counter=0
        else:
            lines_counter+=1

    for line in lines_list:
        pygame.draw.line(screen,line.color,(line.x,line.y),(line.x+line.length,line.y),line.width)
        line.move()
        if line.y > screen_height:
            lines_list.remove(line)
      

# *****************************************************
lines_list=[]
line_y_step=3
max_lines=50
lines_counter=50
add_counter=50
my_player=Player(screen_width//3,screen_height//2,5,10,player_s_surf,line_y_step*1.5)
# ***********************************
def initialize_vars():
    global my_player,lines_list,line_y_step,max_lines,lines_counter,add_counter
    my_player=Player(screen_width//3,screen_height//2,5,10,player_s_surf,line_y_step)
    lines_list=[]
    line_y_step=3
    max_lines=50
    lines_counter=50
    add_counter=50

# *****************************************************
def start_game():
    while True:
        check_events()
        screen.fill((0,150,200))
        if my_player.keep_running:
            draw_lines()
            my_player.draw_rect()
            my_player.move_down()
            my_player.check_move()
            my_player.check_jump()
            screen.blit(my_player.surf,(my_player.x,my_player.y))
            my_player.check_crash_bottom()
            my_player.draw_score()
            my_player.check_on_line()
            pygame.display.update()
            clock.tick(60)
start_game()