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
    
    def __init__(self, x, y, color, moveset):
        pygame.sprite.Sprite.__init__(self)
        self.w = self.h = 60
        self.image = pygame.Surface((self.w, self.h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx = self.vy = 0
        self.vel = 2
        self.moveset = moveset
        self.isLeft = self.isRight = self.isUp = self.isDown = False
        self.isAlive = True

    def onKeyDown(self, event):
        if event.key == self.moveset[0]: self.isLeft  = True
        if event.key == self.moveset[1]: self.isRight = True
        if event.key == self.moveset[2]: self.isUp    = True
        if event.key == self.moveset[3]: self.isDown  = True

    def onKeyUp(self, event):
        if event.key == self.moveset[0]: self.isLeft  = False
        if event.key == self.moveset[1]: self.isRight = False
        if event.key == self.moveset[2]: self.isUp    = False
        if event.key == self.moveset[3]: self.isDown  = False

    def death(self):
        self.isAlive = False

    def update(self):
        self.vx = (-self.vel if self.isLeft else 0) + (self.vel if self.isRight else 0)
        self.vy = (-self.vel if self.isUp   else 0) + (self.vel if self.isDown  else 0)

        #right
        if self.vx > 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx + self.w > obj.x and self.x + self.vx < obj.x + obj.w and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        if isinstance(obj, Wall) or isinstance(obj, Player): self.vx = obj.x - (self.x + self.w)
                        break
        #left
        if self.vx < 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx < obj.x + obj.w and self.x + self.vx + self.w > obj.x and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        if isinstance(obj, Wall) or isinstance(obj, Player): self.vx = self.x - (obj.x + obj.w)
                        break
        #down
        if self.vy > 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy + self.h > obj.y and self.y + self.vy < obj.y + obj.h and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        if isinstance(obj, Wall) or isinstance(obj, Player): self.vy = obj.y - (self.y + self.h)
                        break
        #up
        if self.vy < 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy < obj.y + obj.h and self.y + self.vy + self.h > obj.y and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        if isinstance(obj, Wall) or isinstance(obj, Player): self.vy = self.y - (obj.y + obj.h)
                        break

        self.x += self.vx
        self.y += self.vy

#enemy shit
class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, player1, player2):
        pygame.sprite.Sprite.__init__(self)
        self.w = self.h = 40
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx = self.vy = 0
        self.vel = 1
        self.target1 = player1
        self.target2 = player2

    def update(self):
        centerSelfx = self.x + self.w/2
        centerSelfy = self.y + self.h/2
        center1x = self.target1.x + self.target1.w/2
        center1y = self.target1.y + self.target1.h/2
        center2x = self.target2.x + self.target2.w/2
        center2y = self.target2.y + self.target2.h/2

        dist1 = ((centerSelfx - center1x)**(2) + (centerSelfy - center1y)**(2))**(1/2)
        dist2 = ((centerSelfx - center2x)**(2) + (centerSelfy - center2y)**(2))**(1/2)

        if   not self.target1.isAlive: target = self.target2
        elif not self.target2.isAlive: target = self.target1
        else: target = self.target1 if dist1 < dist2 else self.target2
        centerx = target.x + target.w / 2
        centery = target.y + target.h / 2

        if centerx - centerSelfx < 0: self.vx = -self.vel
        if centerx - centerSelfx > 0: self.vx = self.vel
        if centery - centerSelfy < 0: self.vy = -self.vel
        if centery - centerSelfy > 0: self.vy = self.vel
        if centerx - centerSelfx == 0: self.vx = 0
        if centery - centerSelfy == 0: self.vy = 0

        # right
        if self.vx > 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx + self.w > obj.x and self.x + self.vx < obj.x + obj.w and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        if isinstance(obj, Wall) or isinstance(obj, Enemy): self.vx = obj.x - (self.x + self.w)
                        if isinstance(obj, Player): obj.death()
                        break
        # left
        if self.vx < 0:
            for obj in objList:
                if not obj == self:
                    if self.x + self.vx < obj.x + obj.w and self.x + self.vx + self.w > obj.x and self.y < obj.y + obj.h and self.y + self.h > obj.y:
                        if isinstance(obj, Wall) or isinstance(obj, Enemy): self.vx = self.x - (obj.x + obj.w)
                        if isinstance(obj, Player): obj.death()
                        break
        # down
        if self.vy > 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy + self.h > obj.y and self.y + self.vy < obj.y + obj.h and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        if isinstance(obj, Wall) or isinstance(obj, Enemy): self.vy = obj.y - (self.y + self.h)
                        if isinstance(obj, Player): obj.death()
                        break
        # up
        if self.vy < 0:
            for obj in objList:
                if not obj == self:
                    if self.y + self.vy < obj.y + obj.h and self.y + self.vy + self.h > obj.y and self.x < obj.x + obj.w and self.x + self.w > obj.x:
                        if isinstance(obj, Wall) or isinstance(obj, Enemy): self.vy = self.y - (obj.y + obj.h)
                        if isinstance(obj, Player): obj.death()
                        break

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
player1 = Player(30, 1080/2-25, blue, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
player2 = Player(1830, 1080/2-25, yellow, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
wallList = [
    Wall(0, -10, 1920, 20), Wall(0, 1070, 1920, 20), Wall(-10, 0, 20, 1080), Wall(1910, 0, 20, 1080) #top, bottom, left, right
]
enemyList = []
for i in range(0, 3):
    enemyList.append(Enemy(1920/2-20, 1080/2-20, player1, player2))

objList = []
objList.append(player1)
objList.append(player2)
objList.extend(wallList)
objList.extend(enemyList)

allsprites = pygame.sprite.Group()
allsprites.add(player1)
allsprites.add(player2)
allsprites.add(wallList)
allsprites.add(enemyList)

#loop shit
while True:

    #input shit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if player1.isAlive: player1.onKeyDown(event)
            if player2.isAlive: player2.onKeyDown(event)
        if event.type == pygame.KEYUP:
            if player1.isAlive: player1.onKeyUp(event)
            if player2.isAlive: player2.onKeyUp(event)

    if player1.isAlive: player1.update()
    if player2.isAlive: player2.update()

    #draw shit
    screen.fill(black)
    for wall in wallList:
        screen.blit(wall.image, (wall.x, wall.y))
    for enemy in enemyList:
        enemy.update()
        screen.blit(enemy.image, (enemy.x, enemy.y))
    if player1.isAlive: screen.blit(player1.image, (player1.x, player1.y))
    if player2.isAlive: screen.blit(player2.image, (player2.x, player2.y))

    #update shit
    allsprites.update()
    pygame.display.flip()
    clock.tick(60)