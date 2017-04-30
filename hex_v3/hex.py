__author__ = "adam_mcdaniel"

import pygame,sys,os,random,time,glob,math
import Tkinter as tk
from pygame.locals import *

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
grey = (90,90,90)
slate = (47,89,89)
silver = (200,200,200)
bblue = (0, 109, 160)

with open(os.path.join(os.path.dirname(sys.argv[0]),'library/data/conf/res.dat')) as f:
    content = f.readlines()
    f.close()

width = content[1]
height = content[2]
width = int(width)
height = int(height)
WIN_WIDTH = width
WIN_HEIGHT = height
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 1000

pygame.init()

entities = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
view_object = []
bkg = []

soundtrack_check = ""
soundtracks = []
bglist = []

levels = []
Viewers = []
tiles = []
borders = []
messages = []

selectors = []

dios = []
dios2 = []
dios3 = []

projectiles = []

pygame.font.init()
global font

pygame.mixer.init()
#pygame.mixer.music.set_volume(0.3)

screen = pygame.display.set_mode(DISPLAY,FLAGS, DEPTH)
font = pygame.font.Font(str(os.path.join(str(sys.argv[0]).replace(os.path.basename(sys.argv[0]),''),'library/resources/font/dio.ttf')), 35)
class Text():
    def __init__(self,x,y):
        self.message = None
        self.x = x
        self.y = y
        try:
            messages.append(self)
        except Exception as e:
            pass

    def set_message(self,text,color):
        self.message = font.render(text,True,color)

    def update(self,screen):
        screen.blit(self.message,(self.x,self.y))


def build(level = 0,soundtrack = 0,backg = 0):
    global soundtrack_check
    x = y = 0
    for row in level:
        for col in row:

            if col == "D":
                f = Factory(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileBlueFlag.png"),1)
                tiles.append(f)

            if col == "F":
                f = Factory(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRedFlag.png"),2)
                tiles.append(f)

            if col == "Q":
                f = Factory(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileGreenFlag.png"),3)
                tiles.append(f)

            if col == "G":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileGrass_full.png"))
                #p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRock_full.png"))
                tiles.append(p)

            if col == "1":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/viewer/viewer.png"))
                tiles.append(p)
                borders.append(p)

            if col == "M":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileAutumn_full.png"))
                #p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRock_full.png"))
                tiles.append(p)
            if col == "m":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRedFlag_full.png"))
                tiles.append(p)

            if col == "S":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRock_full.png"))
                tiles.append(p)


            if col == "W":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileWater_shadow.png"))
                tiles.append(p)
            if col == "w":
                p = Tile(x,y,os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileBlueFlag.png"))
                tiles.append(p)
                borders.append(p)

            if col == "H":
                p = Wall(x,y)#,"#000000")#os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileWater_shadow.png"))
                tiles.append(p)

            if col == "q":
                v = Viewer(x,y)
                Viewers.append(v)

            x += 32
        y += 48
        x = 0

    if backg == "B":
        bg = pygame.Surface((32,32))
        bg.fill(pygame.Color("#000000"))
        bkg.append(bg)

    elif backg == "W":
        bg = pygame.Surface((32,32))
        bg.fill(pygame.Color("#EEEEEE"))
        bkg.append(bg)

    try:
        if soundtrack_check != soundtrack:
            pygame.mixer.music.load(soundtrack)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
            soundtrack_check = soundtrack
    except:
        pass

def clearall(l = 0):
    global camera
    entities.empty()
    backgrounds.empty()
    del bkg[:]
    del dios[:]
    del dios2[:]
    del dios3[:]
    del Viewers[:]
    del projectiles[:]
    del tiles[:]
    del messages[:]
    if len(soundtracks) > 0:
        build(levels[l],soundtracks[l],str(bglist[l]))
    else:
        build(levels[l],0,str(bglist[l]))
    total_level_width  = len(levels[l][0])*32
    total_level_height = len(levels[l])*48
    camera = Camera(complex_camera, total_level_width, total_level_height)
    time.sleep(0.25)

def main():
    global cameraX, cameraY

    pygame.display.set_caption("Hex")

    timer = pygame.time.Clock()

    #pygame.mouse.set_visible(False)
    pygame.mouse.set_visible(True)

    Game = True
    l = 0
    firstround = True

    playing = True

    for name in glob.glob(os.path.join(os.path.dirname(sys.argv[0]),'library/data/lib/*/map/*')):
        try:
            with open(name) as f:
                level = f.readlines()
                levels.append(level)
                f.close()
        except Exception as e:
            pass
    for name in glob.glob(os.path.join(os.path.dirname(sys.argv[0]),'library/data/lib/*/soundtrack/*')):
        try:
            with open(name) as f:
                soundtracks.append(str(name))
                f.close()
        except Exception as e:
            pass
    for name in glob.glob(os.path.join(os.path.dirname(sys.argv[0]),'library/data/lib/*/background/*')):
        try:
            with open(name) as f:
                content = f.readlines
                backg = content(0)
                backg = backg[0]
                backg.replace('\n','')
                bglist.append(str(backg[0]))
                f.close()
        except Exception as e:
            pass

    up = down = left = right = False

    #bg = pygame.image.load('block.png')

    clearall(0)
    # build the level

    try:
        bg = bkg[0]
    except Exception as e:
        pass

    Running = True
    pause = False


    selector = Selector()
    selectors.append(selector)
    with open(os.path.join(os.path.dirname(sys.argv[0]),'library/data/conf/fps.dat')) as f:
        fpscontent = f.readlines()
        f.close()

    fps = fpscontent[0]


    # Code to add widgets will go here...

    blit_timer = 0

    slow_speed = 0

    rate = 1
    while Running:
        blit_timer += rate
        timer.tick(float(fps))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Game = False
                Running = False
                pygame.quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                selector.selecting = False

            if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
                clearall(0)

            if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                pass
                """
                try:
                    if playing:
                        playing = False
                        pygame.mixer.music.pause()
                    elif not playing:
                        playing = True
                        pygame.mixer.music.unpause()
                except:
                    pass
                """
            if e.type == pygame.MOUSEBUTTONDOWN:

                if selector.selecting == "place":
                    if len(selector.children) > 0:
                        selector.place()
                        selector.selecting = False
                    else:
                        selector.selecting = False

                if selector.selecting == False:
                    selector.selecting = True
                    selector.set_anchor((pygame.mouse.get_pos()[0]+Viewers[0].rect.left-WIN_WIDTH/2,pygame.mouse.get_pos()[1]+Viewers[0].rect.top-WIN_HEIGHT/2))

            if e.type == pygame.MOUSEBUTTONUP:
                selector.children = []
                if selector.selecting == True:
                    for dio in dios:
                        if pygame.Rect.colliderect(selector.rect,dio.rect):
                            selector.children.append(dio)
                    selector.selecting = "place"



            if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                down = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                right = True

            if e.type == pygame.KEYUP and e.key == pygame.K_w:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_s:
                down = False
            if e.type == pygame.KEYUP and e.key == pygame.K_a:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_d:
                right = False

        # draw background
        """
        for y in range(40):
            for x in range(40):
                screen.blit(bkg[0], (x * 32, y * 32))
        """

        if blit_timer >= slow_speed:
            screen.fill(white)

        # update player, draw everything else

        Viewers[0].update(up, down, left, right)

        camera.update(Viewers[0])

        for tile in tiles:
            if not isinstance(tile,Wall):
                tile.update()
                if pygame.sprite.collide_rect(view_object[0],tile):
                    if blit_timer >= slow_speed:
                        screen.blit(tile.image, camera.apply(tile))

        for dio in dios:
            dio.update()
            if pygame.sprite.collide_rect(view_object[0],dio):
                if blit_timer >= slow_speed:
                    screen.blit(dio.image,camera.apply(dio))

        for dio in dios2:
            dio.update()
            if pygame.sprite.collide_rect(view_object[0],dio):
                if blit_timer >= slow_speed:
                    screen.blit(dio.image,camera.apply(dio))

        for dio in dios3:
            dio.update()
            if pygame.sprite.collide_rect(view_object[0],dio):
                if blit_timer >= slow_speed:
                    screen.blit(dio.image,camera.apply(dio))

        for projectile in projectiles:
            projectile.update()
            if pygame.sprite.collide_rect(view_object[0],projectile):
                if blit_timer >= slow_speed:
                    screen.blit(projectile.image,camera.apply(projectile))

        for s in selectors:
            if pygame.sprite.collide_rect(view_object[0],s):
                if blit_timer >= slow_speed:
                    screen.blit(s.image,camera.apply(s))
            selector.update((pygame.mouse.get_pos()[0]+Viewers[0].rect.left-WIN_WIDTH/2,pygame.mouse.get_pos()[1]+Viewers[0].rect.top-WIN_HEIGHT/2))
        """
        if len(dios) == 0:
            time.sleep(1)
            clearall(0)
        """
        if blit_timer >= slow_speed:
            blit_timer = 0

        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class view(Entity):
    def __init__(self,image = "#0000C5"):
        Entity.__init__(self)
        self.color = image
        self.image = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
        self.image.fill(pygame.Color(self.color))

        try:
            self.image = pygame.image.load(image)
        except:
            pass

        self.rect = pygame.Rect(0, 0,WIN_WIDTH,WIN_HEIGHT)
        view_object.append(self)

View = view()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)
def complex_camera(camera, target_rect):
    with open(os.path.join(os.path.dirname(sys.argv[0]),'library/data/conf/os.dat')) as f:
        content = f.readlines()
        f.close()
        ostype = content[0]

    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h
    """
    if 'win' in ostype:
        l = min(0, l)                      # stop scrolling at the left edge
        l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                      # stop scrolling at the top
    """
    view_object[0].rect.left, view_object[0].rect.top, _, _ = pygame.Rect(l, t, w, h)
    view_object[0].rect.left = -view_object[0].rect.left
    view_object[0].rect.top = -view_object[0].rect.top
    return pygame.Rect(l, t, w+32, h)

class Selector(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.lastdir = 'right'
        self.xvel = 0
        self.yvel = 0
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.image = pygame.Surface((72, 72),pygame.SRCALPHA)
        self.image.fill((0,0,255,80))
        self.selecting = False

        self.store_coords = (0,0)

        self.anchor = pygame.mouse.get_pos()

        self.children = []

    def set_anchor(self,coords):
        self.anchor = coords
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        self.children = []

    def change_size(self,coords):
        self.image = pygame.Surface((abs(coords[0] - self.anchor[0]), abs(coords[1] - self.anchor[1])),pygame.SRCALPHA)
        self.image.fill((0,0,255,80))
        self.rect = pygame.Rect(self.rect.left,self.rect.top,abs(coords[0] - self.anchor[0]), abs(coords[1] - self.anchor[1]))

    """
    def kill(self):
        self.selecting = "place"
        self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),'library/resources/viewer/viewer.png'))
        for dio in dios:
            if pygame.sprite.collide_rect(self,dio):
                self.children.append(dio)
            else:
                try:
                    self.children.remove(dio)
                except Exception as e:
                    pass

    """
    def place(self):
        for child in self.children:
            child.change_dir((pygame.mouse.get_pos()[0]+Viewers[0].rect.left-WIN_WIDTH/2+36,pygame.mouse.get_pos()[1]+Viewers[0].rect.top-WIN_HEIGHT/2+36))
            self.children = []

    def update(self,coords):
        if self.selecting == True:
            for dio in dios:
                if pygame.sprite.collide_rect(self,dio):
                    self.children.append(dio)
                else:
                    try:
                        self.children.remove(dio)
                    except Exception as e:
                        pass
            self.change_size(coords)
            if (coords[0] - self.anchor[0] < 0):
                self.rect.left = coords[0]
            if (coords[1] - self.anchor[1] < 0):
                self.rect.top = coords[1]
        else:
            self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),'library/resources/viewer/viewer.png'))



class Viewer(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.lastdir = 'right'
        self.xvel = 0
        self.yvel = 0
        self.max_speed = 12
        self.rect = pygame.Rect(x, y, 72, 72)
        #self.image = pygame.Surface((72, 72),pygame.SRCALPHA)
        #self.image.fill((255,0,0,100))
        self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),'library/resources/viewer/viewer.png'))

    def update(self, up, down, left, right):

        if up:
            if self.yvel > -self.max_speed:
                self.yvel += -1
            else:
                self.yvel = -self.max_speed

        if down:
            if self.yvel < self.max_speed:
                self.yvel += 1
            else:
                self.yvel = self.max_speed

        if left:
            if self.xvel > -self.max_speed:
                self.xvel += -1
            else:
                self.xvel = -self.max_speed

        if right:
            if self.xvel < self.max_speed:
                self.xvel += 1
            else:
                self.xvel = self.max_speed

        if not(left or right):
            if self.xvel > 0:
                self.xvel -= 0.25
            if self.xvel < 0:
                self.xvel += 0.25
            self.walkcycle = 0
        if not(up or down):
            if self.yvel > 0:
                self.yvel -= 0.25
            if self.yvel < 0:
                self.yvel += 0.25

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, borders)
        # increment in y direction
        self.rect.top += self.yvel
        # do y-axis collisions
        self.collide(0, self.yvel, borders)

    def collide(self, xvel, yvel, borders):
        for border in borders:
            if pygame.sprite.collide_rect(self, border):
                if xvel > 0:
                    self.rect.right = border.rect.left
                if xvel < 0:
                    self.rect.left = border.rect.right
                if yvel > 0:
                    self.rect.bottom = border.rect.top
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = border.rect.bottom
                    self.yvel = 0

class Tile(Entity):
    def __init__(self, x, y,color = "#0000C5"):
        Entity.__init__(self)
        self.timer = 0
        self.color = color
        self.image = pygame.Surface((32, 32))
        self.type = 1

        try:
            self.image.fill(pygame.Color(self.color))
        except:
            pass

        try:
            self.image = pygame.image.load(self.color)
        except:
            pass


        self.image.convert()
        self.rect = pygame.Rect(x, y, 64, 64)

    def update(self):
        try:
            pass
        except:
            pass


class Factory(Entity):
    def __init__(self, x, y,color = "#0000C5",faction = 1):
        Entity.__init__(self)
        self.timer = 0
        self.color = color
        self.image = pygame.Surface((32, 32))
        self.type = faction

        try:
            self.image.fill(pygame.Color(self.color))
        except:
            pass

        try:
            self.image = pygame.image.load(self.color)
        except:
            pass


        self.image.convert()
        self.rect = pygame.Rect(x, y, 64, 64)

    def check_dios(self,type_check):
        number_of_dios = 0
        if type_check == 1:
            for dio in dios:
                if pygame.sprite.collide_rect(self,dio):
                    number_of_dios += 1
        if type_check == 2:
            for dio in dios2:
                if pygame.sprite.collide_rect(self,dio):
                    number_of_dios += 1
        if type_check == 3:
            for dio in dios3:
                if pygame.sprite.collide_rect(self,dio):
                    number_of_dios += 1
        return number_of_dios

    def change_type(self):
        if self.check_dios(1) > 2:
            self.type = 1
            self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileBlueFlag.png"))
        if self.check_dios(2) > 2:
            self.type = 2
            self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileRedFlag.png"))
        if self.check_dios(3) > 2:
            self.type = 3
            self.image = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]),"library/resources/plats/tileGreenFlag.png"))

    def update(self):
        try:
            self.change_type()
            self.timer += 1
            if self.timer > 200:
                if self.check_dios(self.type) < 3:
                    number_of_factories = 0
                    if self.type == 1:
                        for factory in tiles:
                            if isinstance(factory,Factory):
                                if factory.type == 1:
                                    number_of_factories += 1
                        if len(dios) < (number_of_factories**0.5)*4:
                            d = PlayerDio(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios.append(d)
                            d.collide(1,1)
                            print((number_of_factories**0.5)*4)
                    if self.type == 2:
                        for factory in tiles:
                            if isinstance(factory,Factory):
                                if factory.type == 2:
                                    number_of_factories += 1
                        if len(dios2) < (number_of_factories**0.5)*4:
                            d = AiDio(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios2.append(d)
                            d.collide(1,1)
                    if self.type == 3:
                        for factory in tiles:
                            if isinstance(factory,Factory):
                                if factory.type == 1:
                                    number_of_factories += 1
                        if len(dios3) < (number_of_factories**0.5)*4:
                            d = AiDio2(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios3.append(d)
                            d.collide(1,1)
                    """
                    if self.type == 1:
                        if len(dios) < 16:
                            d = PlayerDio(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios.append(d)
                            d.collide(1,1)
                    if self.type == 2:
                        if len(dios2) < 16:
                            d = AiDio(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios2.append(d)
                            d.collide(1,1)
                    if self.type == 3:
                        if len(dios3) < 16:
                            d = AiDio2(self.rect.left+32+random.randint(-10,10),self.rect.top+32+random.randint(-10,10))
                            dios3.append(d)
                            d.collide(1,1)
                    """
                    self.timer = 0
        except Exception as e:
            print(e)

class Wall(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.rect = pygame.Rect(x, y, 66, 66)


class Projectile(Entity):
    def __init__(self, x, y, angle, color, parent):
        Entity.__init__(self)
        self.angle = angle
        self.parent = parent
        self.forward = random.randint(10,15)
        self.xvel = 0
        self.yvel = 0
        self.image = pygame.Surface((3,3))
        self.image.fill(pygame.Color(color))
        self.rect = pygame.Rect(x, y, 3, 3)
        projectiles.append(self)
        self.time = 0

    def update(self):
        self.time += 1
        if self.time > 1000:
            self.kill()

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # do y-axis collisions
        self.collide(0, self.yvel)

    def kill(self):
        if self in projectiles:
            projectiles.remove(self)

    def collide(self, xvel, yvel):
        if self.parent == "2":
            for dio in dios:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
            for dio in dios2:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
        if self.parent == "1":
            for dio in dios:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
            for dio in dios3:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
        if self.parent == "player":
            for dio in dios2:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
            for dio in dios3:
                if pygame.sprite.collide_rect(self, dio):
                    dio.kill()
                    self.kill()
        for tile in tiles:
            if isinstance(tile,Wall):
                if pygame.sprite.collide_rect(self, tile):
                    self.kill()




class PlayerDio(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.lives = 5
        self.turn = 0
        self.angle = 3
        self.shoot_timer = 10
        self.forward = random.randint(4,9)
        self.check_distance_num = random.randint(10,30)
        self.xvel = 0
        self.yvel = 0
        self.random_height = random.randint(16,32)
        self.rect = pygame.Rect(x, y, 8, self.random_height)
        self.image = pygame.Surface((8,self.random_height))
        self.image.fill(pygame.Color("#"+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+"FF"))
        self.moving = False
        self.coords = (self.rect.left,self.rect.top)

    def begin_move(self):
        self.moving = True

    def end_move(self):
        self.moving = False

    def change_dir(self,coords):
        self.coords = coords
        if ((self.coords[0]-self.rect.left > 0) and (self.coords[1]-self.rect.top < 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.coords[1]),(self.rect.left-self.coords[0])))
        if ((self.coords[0]-self.rect.left < 0) and (self.coords[1]-self.rect.top > 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.coords[1]),(self.rect.left-self.coords[0])))))
        if ((self.coords[0]-self.rect.left > 0) and (self.coords[1]-self.rect.top > 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.coords[1]),(self.rect.left-self.coords[0])))
        if ((self.coords[0]-self.rect.left < 0) and (self.coords[1]-self.rect.top < 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.coords[1]),(self.rect.left-self.coords[0])))))
        self.angle += self.turn

    def target_shoot(self):
        for dio in dios2:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 150:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#2222FF","player")
                    self.shoot_timer = 10
        for dio in dios3:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 150:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#2222FF","player")
                    self.shoot_timer = 10

    def update(self):
        self.target_shoot()

        if (((((self.coords[0]-self.rect.left)**2)+((self.coords[1]-self.rect.top)**2))**0.5)) < 24:
            self.end_move()
        else:
            self.moving = True
            self.change_dir(self.coords)


        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

        if not self.moving:
            self.xvel = 0
            self.yvel = 0

        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # do y-axis collisions
        self.collide(0, self.yvel)
        """
        try:
            for dio in dios:
                if dio != self:
                    if pygame.Rect.colliderect(self.rect,dio.rect):
                        if self.moving:
                            self.rect.left += random.randint(-8,8)
                            self.rect.top += random.randint(-8,8)
                        else:
                            self.rect.left += random.randint(-2,2)
                            self.rect.top += random.randint(-2,2)
        except:
            pass
        """
    def kill(self):
        self.lives -= 1
        if self.lives <= 0:
            dios.remove(self)

    def collide(self, xvel, yvel):
        for tile in tiles:
            if isinstance(tile,Wall):
                if pygame.sprite.collide_rect(self, tile):
                    if xvel > 0:
                        self.rect.right = tile.rect.left
                        self.xvel = 0
                    if xvel < 0:
                        self.rect.left = tile.rect.right
                        self.xvel = 0
                    if yvel > 0:
                        self.rect.bottom = tile.rect.top
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = tile.rect.bottom
                        self.yvel = 0
        for dio in dios:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5
        for dio in dios2:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5
        for dio in dios3:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5

class AiDio(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.lives = 10
        self.stop_time = 0
        self.shoot_timer = 10
        self.turn = 1
        self.angle = 3
        self.forward = random.randint(3,6)
        self.check_distance_num = random.randint(10,30)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.random_height = random.randint(16,32)
        self.rect = pygame.Rect(x, y, 8, self.random_height)
        self.image = pygame.Surface((8,self.random_height))
        self.image.fill(pygame.Color("#FF"+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))))
        self.moving = False
        self.coords = (self.rect.left,self.rect.top)
        self.target_dio = None

    def kill(self):
        dios2.remove(self)

    def change_dir(self,coords):
        if ((coords[0]-self.rect.left > 0) and (coords[1]-self.rect.top < 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))
        if ((coords[0]-self.rect.left < 0) and (coords[1]-self.rect.top > 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))))
        if ((coords[0]-self.rect.left > 0) and (coords[1]-self.rect.top > 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))
        if ((coords[0]-self.rect.left < 0) and (coords[1]-self.rect.top < 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))))
        self.angle += self.turn

    def target_shoot(self):
        for dio in dios:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 100:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#FF2222","1")
                    self.shoot_timer = 0

        for dio in dios3:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 100:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#FF2222","1")
                    self.shoot_timer = 0


    def find_dio(self):
        try:
            list_of_distances = []
            list_of_dios = []
            for dio in dios:
                list_of_distances.append((((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)+80))
                list_of_dios.append(dio)
            for dio in dios3:
                list_of_distances.append((((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)+80))
                list_of_dios.append(dio)
            for fact in tiles:
                if isinstance(fact,Factory):
                    if fact.type != 2:
                        if fact.check_dios(2) == 0:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)))
                            list_of_dios.append(fact)
                        elif fact.check_dios(2) > 0:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)-20))
                            list_of_dios.append(fact)
                        elif fact.check_dios(2) > 1:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)-40))
                            list_of_dios.append(fact)

            dio_num = -1
            x = 1000000
            for i in list_of_distances:
                dio_num+=1
                if i < x:
                    x = i
                    self.target_dio = list_of_dios[dio_num]
        except Exception as e:
            print(e)

    def move_to_target(self):
        try:
            self.coords[0] = self.target_dio.rect.left
            self.coords[1] = self.target_dio.rect.top
        except Exception as e:
            pass

    def stop_move(self):
        self.stop_time = 10

    def update(self):
        if random.randint(0,50) == 1:
            self.stop_move()
        if self.stop_time > 0:
            self.stop_time += -1
        else:
            self.find_dio()
            self.move_to_target()
            self.target_shoot()

            if (((((self.coords[0]-self.rect.left)**2)+((self.coords[1]-self.rect.top)**2))**0.5)) < 24:
                pass
            else:
                if isinstance(self.target_dio,Factory):
                    self.change_dir((self.target_dio.rect.left+32,self.target_dio.rect.top+32))
                else:
                    self.change_dir((self.target_dio.rect.left,self.target_dio.rect.top))
            if self.angle > 360:
                self.angle += -360
            if self.angle < 0:
                self.angle += 360

            self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
            self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0)
            # increment in y direction
            self.rect.top += self.yvel
            # do y-axis collisions
            self.collide(0, self.yvel)

    def collide(self, xvel, yvel):
        for tile in tiles:
            if isinstance(tile,Wall):
                if pygame.sprite.collide_rect(self, tile):
                    if xvel > 0:
                        self.rect.right = tile.rect.left
                        self.xvel = 0
                    if xvel < 0:
                        self.rect.left = tile.rect.right
                        self.xvel = 0
                    if yvel > 0:
                        self.rect.bottom = tile.rect.top
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = tile.rect.bottom
                        self.yvel = 0
        for dio in dios:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5

        for dio in dios2:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5
        for dio in dios3:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5

class AiDio2(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.lives = 10
        self.stop_time = 0
        self.shoot_timer = 10
        self.turn = 1
        self.angle = 3
        self.forward = random.randint(6,12)
        self.check_distance_num = random.randint(10,30)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.random_height = random.randint(16,32)
        self.rect = pygame.Rect(x, y, 8, self.random_height)
        self.image = pygame.Surface((8,self.random_height))
        self.image.fill(pygame.Color("#"+str(random.randint(0,9))+str(random.randint(0,9))+"cc"+str(random.randint(0,9))+str(random.randint(0,9))))
        #self.image.fill(pygame.Color("#ccee"+str(random.randint(0,9))+str(random.randint(0,9))))
        self.moving = False
        self.coords = (self.rect.left,self.rect.top)
        self.target_dio = None

    def kill(self):
        dios3.remove(self)

    def change_dir(self,coords):
        if ((coords[0]-self.rect.left > 0) and (coords[1]-self.rect.top < 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))
        if ((coords[0]-self.rect.left < 0) and (coords[1]-self.rect.top > 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))))
        if ((coords[0]-self.rect.left > 0) and (coords[1]-self.rect.top > 0)):
            self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))
        if ((coords[0]-self.rect.left < 0) and (coords[1]-self.rect.top < 0)):
            self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-coords[1]),(self.rect.left-coords[0])))))
        self.angle += self.turn

    def target_shoot(self):
        for dio in dios:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 256:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#22FF22","2")
                    self.shoot_timer = 22
        for dio in dios2:
            if (((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)) < 256:
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))
                if ((dio.rect.left-self.rect.left > 0) and (dio.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))
                if ((dio.rect.left-self.rect.left < 0) and (dio.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-dio.rect.top),(self.rect.left-dio.rect.left)))))

                if self.shoot_timer > 0:
                    self.shoot_timer += -1
                else:
                    projectile = Projectile(self.rect.left,self.rect.top,self.angle+self.turn,"#22FF22","2")
                    self.shoot_timer = 22


    def find_dio(self):
        try:
            list_of_distances = []
            list_of_dios = []
            for dio in dios:
                list_of_distances.append((((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)+50))
                list_of_dios.append(dio)
            for dio in dios2:
                list_of_distances.append((((((dio.rect.left-self.rect.left)**2)+((dio.rect.top-self.rect.top)**2))**0.5)+50))
                list_of_dios.append(dio)
            for fact in tiles:
                if isinstance(fact,Factory):
                    if fact.type != 3:
                        if fact.check_dios(3) == 0:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)))
                            list_of_dios.append(fact)
                        elif fact.check_dios(3) > 0:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)-20))
                            list_of_dios.append(fact)
                        elif fact.check_dios(3) > 1:
                            list_of_distances.append((((((fact.rect.left+32-self.rect.left)**2)+((fact.rect.top+32-self.rect.top)**2))**0.5)-40))
                            list_of_dios.append(fact)
            dio_num = -1
            x = 1000000
            for i in list_of_distances:
                dio_num+=1
                if i < x:
                    x = i
                    self.target_dio = list_of_dios[dio_num]
        except Exception as e:
            print(e)

    def move_to_target(self):
        try:
            self.coords[0] = self.target_dio.rect.left
            self.coords[1] = self.target_dio.rect.top
        except Exception as e:
            pass

    def stop_move(self):
        self.stop_time = 10

    def update(self):
        if random.randint(0,40) == 1:
            self.stop_move()
        if self.stop_time > 0:
            self.stop_time += -1
        else:
            self.find_dio()
            self.move_to_target()
            self.target_shoot()

            if (((((self.coords[0]-self.rect.left)**2)+((self.coords[1]-self.rect.top)**2))**0.5)) < 24:
                pass
            else:
                self.change_dir((self.target_dio.rect.left,self.target_dio.rect.top))

            if self.angle > 360:
                self.angle += -360
            if self.angle < 0:
                self.angle += 360

            self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
            self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

            self.rect.left += self.xvel
            # do x-axis collisions
            self.collide(self.xvel, 0)
            # increment in y direction
            self.rect.top += self.yvel
            # do y-axis collisions
            self.collide(0, self.yvel)

    def collide(self, xvel, yvel):
        for tile in tiles:
            if isinstance(tile,Wall):
                if pygame.sprite.collide_rect(self, tile):
                    if xvel > 0:
                        self.rect.right = tile.rect.left
                        self.xvel = 0
                    if xvel < 0:
                        self.rect.left = tile.rect.right
                        self.xvel = 0
                    if yvel > 0:
                        self.rect.bottom = tile.rect.top
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = tile.rect.bottom
                        self.yvel = 0
        for dio in dios:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5

        for dio in dios2:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5

        for dio in dios3:
            if dio != self:
                if pygame.sprite.collide_rect(self, dio):
                    if xvel > 0:
                        self.rect.right = dio.rect.left
                        self.xvel += -5
                    if xvel < 0:
                        self.rect.left = dio.rect.right
                        self.xvel += 5
                    if yvel > 0:
                        self.rect.bottom = dio.rect.top
                        self.yvel += -5
                    if yvel < 0:
                        self.rect.top = dio.rect.bottom
                        self.yvel += 5


if __name__ == "__main__":
    while True:
        main()
