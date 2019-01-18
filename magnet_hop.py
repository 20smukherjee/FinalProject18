from pygame import *
import random

interface_x = 400
interface_y = 450

init()
window = display.set_mode((interface_x, interface_y))
display.set_caption('Magnet Hop')
clock = time.Clock()

def message(msg,x,y):
    f = font.Font(None, 20)
    text= f.render(msg,True,[0, 0, 0])
    window.blit(text,[x,y])
    display.update()
    time.delay(1000)
    f = font.Font(None, 20)
    text= f.render(msg,True,[100, 100, 100])
    window.blit(text,[x,y])

class Magnet_Man:
    def __init__(self):       
        self.exist = image.load('RBF.png')
        self.reset()   
    def drawGrid(self):
        for x in range(80):
            draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12)) 
    def reset(self): #Sets initial conditions
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity_x = 5
        self.max_velocity_y = 13
        self.x_acceleration = 0.5
        self.jump_velocity = 13

        scale = 7
        self.width, self.height = 7 * scale, 12 * scale
        self.scale = scale

        self.x = (interface_x - self.width) / 2
        self.y = interface_y - self.height


    def update(self,p):
        self.side_control()
        self.physics(p)
        #self.drawGrid()
        self.move()
        self.show()
        self.x += self.velocity_x
        self.y -= self.velocity_y

        return (self.img, (self.x, self.y, self.width, self.height))

    def physics(self, p):

        on = False
        
        for color, rect in p:
            x,y,w,h = rect

            #X range
            if self.x + self.width / 2 > x and self.x - self.width / 2 < x + w:
                #Y range
                if self.y + self.height >= y and self.y + self.height <= y + h:

                    if self.velocity_y < 0:
                        on = True

        if not on and not self.y >= interface_y - self.height:
            self.velocity_y -= 0.5
        elif on:
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
            
            else:
                keys = key.get_pressed()
                if keys[K_SPACE]:
                    self.velocity_y = self.jump_velocity
                    
    def side_control(self):
        if self.x + self.width < 0:
            self.x = interface_x - self.scale
        if self.x > interface_x:
            self.x = -self.width
    def show(self): #Creates image
        self.img = self.exist

        
    def slowdown(self): 
        if self.velocity_x < 0: self.velocity_x = min(0, self.velocity_x + self.x_acceleration / 6)
        if self.velocity_x > 0: self.velocity_x = max(0, self.velocity_x - self.x_acceleration / 6)

    def move(self):
        keys = key.get_pressed()
        if not self.y >= interface_y - self.height:

            if keys[K_LEFT] and keys[K_RIGHT]: self.slowdown()
            elif keys[K_LEFT]: self.velocity_x -= self.x_acceleration
            elif keys[K_RIGHT]: self.velocity_x += self.x_acceleration
            else: self.slowdown()

            self.velocity_x = max(-self.max_velocity_x, min(self.max_velocity_x, self.velocity_x))
            self.velocity_y = max(-self.max_velocity_y, min(self.max_velocity_y, self.velocity_y))


platform_spacing = 60

class Platform_Manager:
    def __init__(self):
        self.platforms = []
        self.spawns = 0
        self.start_spawn = interface_y+10

        scale = 2.5
        self.width, self.height = 24 * scale, 6 * scale

    def update(self):
        self.spawner()
        return self.manage()

        
        
    def spawner(self):
        if interface_y - info['screen_y'] > self.spawns * platform_spacing:
            self.spawn()
        
    def spawn(self):
        y = self.start_spawn - self.spawns * platform_spacing
        x = random.randint(-self.width, interface_x)
        
        self.platforms.append(Platform(x,y))
        self.spawns += 1
        
    def manage(self):
        u = []
        b = []
        for i in self.platforms:
            b.append(i.show())

            if i.on_screen():
                u.append(i)
            
        self.platforms = u
        return b

class Platform:
    def __init__(self,x,y):
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

def random_colour(l,h):
    return (random.randint(l,h),random.randint(l,h),random.randint(l,h))

def blit_images(x):
    for i in x:
        window.blit(transform.scale(i[0], (i[1][2],i[1][3])), (i[1][0], i[1][1] - info['screen_y']))

def event_loop():
    for loop in event.get():
        if loop.type == KEYDOWN:
            if loop.key == K_ESCAPE:
                quit()
        if loop.type == QUIT:
            quit()

f = font.SysFont('', 50)
def show_score(score, pos):
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
Magnet_man, platform_manager = Magnet_Man(), Platform_Manager()
while True:
    #MAIN LOOP

    event_loop()
    #drawGrid()
    message("Welcome to Magnet Hop. Press space to begin.", interface_x/2-100,interface_y-200)
    platform_blit = platform_manager.update()
    Magnet_blit = Magnet_man.update(platform_blit)
    info['screen_y'] = min(min(0,Magnet_blit[1][1] - interface_y*0.4),info['screen_y'])
    info['score'] = (-Magnet_blit[1][1] + 400)/50

    if Magnet_blit[1][1] - 470 > info['screen_y']:
        info['score'] = 0
        info['screen_y'] = 0
        Magnet_man = Magnet_Man()
        platform_manager = Platform_Manager()

    clock.tick(60)

    #DISPLAY FILL and GRAPHICS
    window.fill((255,255,255))

    blit_images([Magnet_blit])
    
    for x in platform_blit:
        i = list(x)
        i[1] = list(i[1])
        i[1][1] -= info['screen_y']
        draw.rect(window, i[0], i[1])

    info['high_score'] = max(info['high_score'], info['score'])

    show_score(info['score'],1)
    show_score(info['high_score'],0)

    display.update()
