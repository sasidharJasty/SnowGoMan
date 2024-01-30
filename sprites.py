import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.scale = 40
        self.rot=0

    def get_keys(self):
        self.rot_speed=0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.pos.x>=0 or keys[pg.K_a] and self.pos.x>=0:
            self.vel.x = -PLAYER_SPEED
            self.rot_speed = PLAYER_ROTSPD

            


        if keys[pg.K_RIGHT] and self.pos.x<=1024 or keys[pg.K_d] and self.pos.x<=1024:
            self.vel.x = PLAYER_SPEED
            self.rot_speed = -PLAYER_ROTSPD

        #keys2 = pg.key.get_released() 0
        #if keys[pg.K_DOWN] or keys[pg.K_s]:
        #    self.vel.y = PLAYER_SPEED


    def collide_with_ground(self, dir):
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.ground, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.rect.centery = self.pos.y

    def update(self):
        self.get_keys()
        self.rot=(self.rot+self.rot_speed*self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_image,self.rot)
        self.image = pg.transform.scale(self.image, (self.scale*1.5,self.scale*1.5))
        if self.scale>=12: 
            self.scale-=0.01
        else:
            pass
        self.vel.y=+50
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.rect.centerx = self.pos.x

        self.rect.centery = self.pos.y
        self.collide_with_ground('y')
        #print(self.scale)
        self.mask = pg.mask.from_surface(self.image)

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ground
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * (TILESIZE/2)
        self.rect.y = y * (TILESIZE/2)


#Fix this first
class Rock(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.rock
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mobimg
        self.cx = random.randint(45,70)
        self.image = pg.transform.scale(self.image, (self.cx,self.cx))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(10,WIDTH-25)
        self.vx = 0
        self.rect.y = -50
        self.vy = 0
        self.dy = 0.03
        


    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect.y += self.vy
        if self.rect.bottom > 650:
            self.kill()
        
        if self.rect.bottom > 334:
            self.dy = 0.002


        rock_hits = pg.sprite.spritecollide(self.game.player, self.game.rock, False,pg.sprite.collide_circle)
        if rock_hits:
            self.game.player.scale -= random.randrange(5,15)
            self.kill()

        

class snow(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.snow
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.adder = 0
        if self.game.score >= 160 :
            self.image = self.game.sn_image
            self.adder = -3
        else:
            self.image = game.player_image
        self.cx = random.randint(25,65)
        self.image = pg.transform.scale(self.image, (self.cx,self.cx))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(10,WIDTH-25)
        self.vx = 0
        self.rect.y = -50
        self.vy = 0
        self.dy = 0.03
        


    def update(self):
        
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect.y += self.vy
        if self.rect.bottom > 650:
            self.kill()
        if self.rect.bottom > 334:
            self.dy = 0.002
        self.rand = random.randint(6,16)

        rock_hits = pg.sprite.spritecollide(self.game.player, self.game.snow, False,pg.sprite.collide_circle)
        if rock_hits:
            self.game.player.scale += self.rand+ self.adder
            self.kill()