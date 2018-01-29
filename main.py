import pygame, sys, copy

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
done = False

#color shit
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

def collisionCheck(x1, x2, y1, y2, w1, w2, h1, h2):
    return ((x1+w1>x2 and x1+w1<x2+w2) or (x2+w2>x1 and x2+w2 < x1+w1)) and ((y1+h1>y2 and y1+h1<y2+h2) or (y2+h2>y1 and y2+h2 < y1+h1))

#player shit
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, moveset):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.vel = 2
        self.moveset = moveset
        self.isLeft = False
        self.isRight = False
        self.isUp = False
        self.isDown = False

    def onKeyDown(self, event):
        if event.key == self.moveset[0]: self.isLeft = True
        if event.key == self.moveset[1]: self.isRight  = True
        if event.key == self.moveset[2]: self.isUp    = True
        if event.key == self.moveset[3]: self.isDown  = True

    def onKeyUp(self, event):
        if event.key == self.moveset[0]: self.isLeft  = False
        if event.key == self.moveset[1]: self.isRight = False
        if event.key == self.moveset[2]: self.isUp    = False
        if event.key == self.moveset[3]: self.isDown  = False

    def update(self):
        self.vx = (-self.vel if self.isLeft else 0) + (self.vel if self.isRight else 0)
        self.vy = (-self.vel if self.isUp   else 0) + (self.vel if self.isDown  else 0)
        projection = Player(self.x, self.y, self.w, self.h, self.color, self.moveset)
        projection.x += self.vx
        projection.y += self.vy

        if self.vx > 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx + self.w > obj.x and self.x + self.vx < obj.x + obj.w and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        self.vx = obj.x - (self.x + self.w)
                        break;
        if self.vx < 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx < obj.x + obj.w and self.x + self.vx + self.w > obj.x and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        self.vx = self.x - (obj.x + obj.w)
                        break;
        if self.vy > 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy + self.h > obj.y and self.y + self.vy < obj.y + obj.h and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        self.vy = obj.y - (self.y + self.h)
                        break;
        if self.vy < 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy < obj.y + obj.h and self.y + self.vy + self.h > obj.y and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        self.vy = self.y - (obj.y + obj.h)
                        break;

        self.x += self.vx
        self.y += self.vy

#wall shit
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

#define shit
player = Player(1920/2-30, 1080/2-30, 60, 60, blue, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
player2 = Player(1920/2-30, 1080/2+100, 60, 60, yellow, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
wallList = [
    Wall(0, -10, 1920, 20), #top
    Wall(0, 1070, 1920, 20), #bottom
    Wall(-10, 0, 20, 1080), #left
    Wall(1910, 0, 20, 1080), #right
    Wall(100, 100, 100, 100)
]
objList = []
objList.append(player)
objList.append(player2)
objList.extend(wallList)


allsprites = pygame.sprite.Group()
allsprites.add(player)
allsprites.add(player2)
allsprites.add(wallList)

#loop shit
while True:

    #input shit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            player.onKeyDown(event)
            player2.onKeyDown(event)
        if event.type == pygame.KEYUP:
            player.onKeyUp(event)
            player2.onKeyUp(event)

    player.update()
    player2.update()

    #draw shit
    screen.fill(black)
    for wall in wallList:
        screen.blit(wall.image, (wall.x, wall.y))
    screen.blit(player.image, (player.x, player.y))
    screen.blit(player2.image, (player2.x, player2.y))

    #update shit
    allsprites.update()
    pygame.display.flip()
    clock.tick(60)