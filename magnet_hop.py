from pygame import *
import random

interface_x = 400
interface_y = 450
#Initializes screen
init()
window = display.set_mode((interface_x, interface_y))
display.set_caption('Magnet Hop')
clock = time.Clock()

def imessage(msg,x,y): 
    '''Sends message to user at the beginning to tell them how the game works
'''
    f = font.Font(None, 20)
    text= f.render(msg,True,[0, 0, 0])
    window.blit(text,[x,y])
#This is the main
class Magnet_Man:

    def __init__(self):
        WHITE = (255, 255, 255)       
        self.exist = image.load('RBF.png')
        self.exist.set_colorkey(WHITE)
        self.reset()   

    def reset(self):
        '''Set initial/respawn conditions'''
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity_x = 4
        self.max_velocity_y = 13
        self.x_acceleration = 0.5
        self.jump_velocity = 13

        scale = 7
        self.width, self.height = 7 * scale, 12 * scale
        self.scale = scale

        self.x = (interface_x - self.width) / 2
        self.y = interface_y - self.height


    def update(self,p): 
        '''moves the image graphically'''
        self.side_control()
        self.physics(p)
        self.move()
        self.show()
        self.x += self.velocity_x
        self.y -= self.velocity_y

        return (self.img, (self.x, self.y, self.width, self.height))

    def physics(self, p):
        '''Defines the games physics and how it should interact with platform which is what on represent'''
        on = False
        
        for color, rect in p:
            x,y,w,h = rect

            #X range
            if self.x + self.width / 2 > x and self.x - self.width / 2 < x + w:
                #Y range
                if self.y + self.height >= y and self.y + self.height <= y + h:

                    if self.velocity_y < 0:
                        on = True
        if not on and not self.y >= interface_y - self.height: #makes it fall
            self.velocity_y -= 0.5
        elif on: #platform autojump
            self.velocity_y = self.jump_velocity
        else:
            self.y = interface_y - self.height
            self.velocity_x = 0
            self.velocity_y = 0
            if self.x != (interface_x - self.width) / 2:
                if self.x > (interface_x - self.width) / 2:
                    self.x = max((interface_x - self.width) / 2, self.x - 6)
                else:
                    self.x = min((interface_x - self.width) / 2, self.x + 6)
            
            else: #start of game/jump function
                keys = key.get_pressed()
                if keys[K_SPACE] or keys[K_w]:
                    self.velocity_y = self.jump_velocity
                    
    def side_control(self): 
        '''classic doodle jump side teleporting magic'''
        if self.x + self.width < 0:
            self.x = interface_x - self.scale
        if self.x > interface_x:
            self.x = -self.width
    def show(self): 
        '''Creates character image'''
        self.img = self.exist

        
    def slowdown(self): 
        '''slows character down'''
        if self.velocity_x < 0: self.velocity_x = min(0, self.velocity_x + self.x_acceleration / 6)
        if self.velocity_x > 0: self.velocity_x = max(0, self.velocity_x - self.x_acceleration / 6)

    def move(self):
        '''I feel like this one is self-explanitory, it moves the character'''
        keys = key.get_pressed()
        if not self.y >= interface_y - self.height:

            if keys[K_LEFT] and keys[K_RIGHT] or keys[K_a] and keys[K_d]: self.slowdown()
            elif keys[K_LEFT] or keys[K_a]: self.velocity_x -= self.x_acceleration
            elif keys[K_RIGHT] or keys[K_d]: self.velocity_x += self.x_acceleration
            else: self.slowdown()

            self.velocity_x = max(-self.max_velocity_x, min(self.max_velocity_x, self.velocity_x))
            self.velocity_y = max(-self.max_velocity_y, min(self.max_velocity_y, self.velocity_y))
platformspacing = 50
#Its really interesting to play with the varb to see how it affect the frequency of platforms and the difficulty of the game.
class Platform_Tracker:
    '''this sets the conditions for platform generation'''
    def __init__(self):
        '''sets initial conditions for platforms'''
        self.platforms = []
        self.generates = 0
        self.start_generate = interface_y+10

        scale = 2.5 #Size of platforms
        self.width, self.height = 24 * scale, 6 * scale

    def update(self):
        '''gens the platforms as you go up'''
        self.generator()
        return self.manage()

        
        
    def generator(self):
        '''sets conditions for platform generation'''
        if interface_y - info['screen_y'] > self.generates * platformspacing:
            self.generate()
        
    def generate(self):
        '''generates platforms if generator conditions are met'''
        y = self.start_generate - self.generates * platformspacing
        x = random.randint(-self.width, interface_x)
        
        self.platforms.append(Platform(x,y))
        self.generates += 1
        
    def manage(self):
        '''lists with all the platforms so they can all be displayed correctly'''
        a = []
        b = []
        for i in self.platforms:
            b.append(i.show())

            if i.on_screen():
                a.append(i)
            
        self.platforms = a
        return b

class Platform:
    #This monster actually creates the platforms and was by far one of the hardest portions to callibrate
    def __init__(self,x,y):
        '''mold platform'''
        self.x = x
        self.y = y
        self.color = (random.randint(0,300), random.randint(0,300), random.randint(0,300))
        scale = 3
        self.width, self.height = 24 * scale, 6 * scale

    def on_screen(self):
        if self.y > info['screen_y'] + interface_y:
            return False
        return True

    def show(self):
        return ((0,0,0), (self.x, self.y, self.width, self.height))

def random_color(l,h):
    return (random.randint(l,h),random.randint(l,h),random.randint(l,h))

def blit_images(x):
    '''makes platform'''
    for i in x:
        window.blit(transform.scale(i[0], (i[1][2],i[1][3])), (i[1][0], i[1][1] - info['screen_y']))

def event_loop():
    '''game exit'''
    for loop in event.get():
        if loop.type == KEYDOWN:
            if loop.key == K_ESCAPE:
                quit()
        if loop.type == QUIT:
            quit()

f = font.SysFont('', 50)
def show_score(score, pos):
    '''shows score and high score'''
    message = f.render(str(round(score)), True, (10,50,100))
    rect = message.get_rect()

    if pos == 0:
        x = interface_x - rect.width - 10
    else:
        x = 10
    y = rect.height + 10
        
    window.blit(message, (x, y))   
        
#Stores the scores and where they go
info = {
    'screen_y': 0,
    'score': 0,
    'high_score': 0
    }
Magnet_man, platform_tracker = Magnet_Man(), Platform_Tracker()
backgroundimg=image.load("background.png").convert()
intro=0
while True:
    #MAIN LOOP
    if info['score']<100:#Makes the game harder
        platformspacing = 50
    else:
        platformspacing = 53
    event_loop()
    platform_blit = platform_tracker.update()
    Magnet_blit = Magnet_man.update(platform_blit)
    info['screen_y'] = min(min(0,Magnet_blit[1][1] - interface_y*0.4),info['screen_y'])
    info['score'] = (-Magnet_blit[1][1] + 400)/50

    if Magnet_blit[1][1] - 470 > info['screen_y']:
        info['score'] = 0
        info['screen_y'] = 0
        Magnet_man = Magnet_Man()
        platform_tracker = Platform_Tracker()

    clock.tick(60)

    #DISPLAY FILL and GRAPHICS
    window.fill((255,255,255))
    window.blit(backgroundimg,[0,0])
    blit_images([Magnet_blit])
    for x in platform_blit:
        i = list(x)
        i[1] = list(i[1])
        i[1][1] -= info['screen_y']
        draw.rect(window, i[0], i[1])

    info['high_score'] = max(info['high_score'], info['score'])

    show_score(info['score'],1)
    show_score(info['high_score'],0)
    if info['score']<5:
        imessage("Welcome to Magnet Hop. Press Space or w to begin.", interface_x/2-150,interface_y-200)
    else:
        pass
    if info['score'] == 100 and info['score']<105:
         imessage("Congrats, you hit a score of 100!", interface_x/2-150,interface_y-200)
    display.flip()
