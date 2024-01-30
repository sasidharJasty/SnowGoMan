#1. to run cd into the directory
#2. then python3 main.py
#fix sprites.py
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.player_image = pg.image.load(path.join(game_folder, PLAYER_IMG)).convert_alpha()
        self.sn_image = pg.image.load(path.join(game_folder,"blueSnow.png")).convert_alpha()
        self.bg = pg.image.load(path.join(game_folder,"map.png")).convert_alpha()
        self.fog = pg.image.load(path.join(game_folder,"fog.png")).convert_alpha()
        self.rock = pg.image.load(path.join(game_folder, "rock.png")).convert_alpha()
        self.bg_rect = self.bg.get_rect()
        self.fog_rect = self.fog.get_rect()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.rock = pg.sprite.Group()
        self.snow = pg.sprite.Group()
        self.snowflake = pg.sprite.Group()
        self.snowflakes = []
        self.blizzard = False
        self.strat = False 
        self.score = 0
        
        for i in range(SNOWFLAKES):
            x=random.randint(0,1024)
            y=random.randint(0,self.screen.get_height())
            self.snowflakes.append((x,y))
            
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Ground(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'S':
                    snow(self)
                if tile == 'R':
                    Rock(self)
        self.mob_timer = 0
        self.bliz = 0
        self.time = 0
        self.snow_rel = 0


        


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

        now = pg.time.get_ticks()
        now1 = pg.time.get_ticks()
        print(MOB_FREQ-round((self.score)/500))
        if now - self.mob_timer > MOB_FREQ-round((self.score)/2):
            self.mob_timer=now
            Rock(self)
            self.snow_rel+=1
        
        if self.snow_rel >= random.randint(13,16):
            snow(self)
            self.snow_rel = 0
        

        if now1 - self.bliz > FREQ:
            self.bliz=now1
            self.blizzard = True
        
        

        if self.player.scale <=13:
            self.playing = False

        
        


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):

        self.screen.blit(self.bg,self.bg_rect)
        self.all_sprites.draw(self.screen)
        for i in range(len(self.snowflakes)):
            snowflakes = self.snowflakes[i]
            draft = 1
            self.snowflakes[i]=(snowflakes[0]+draft,snowflakes[1]+draft)
            pg.draw.circle(self.screen,pg.Color("snow2"),(snowflakes[0],snowflakes[1]),5)
            if snowflakes[1]> self.screen.get_height():
                self.snowflakes[i] = (snowflakes[0],0)
            
            if snowflakes[0]> self.screen.get_width():
                self.snowflakes[i] = (0,snowflakes[1])

        
        if self.strat == False:
            self.mins = pg.time.get_ticks()
            self.strat =True

        if self.blizzard:
            now3 = pg.time.get_ticks()-self.mins
            self.screen.blit(self.fog,self.fog_rect)
            if now3-self.time>= 18000:
                self.blizzard = False
                self.time = now3
        else:
            now3 = pg.time.get_ticks()-self.mins
            self.time = now3
                
        self.draw_text(str("snowball scale: "+str(round(self.player.scale)-13)), 22, BLACK,WIDTH/2,15)
        self.draw_text("Score: "+str(self.score), 22, BLACK,WIDTH/2,40)
        self.draw_text(str(round(self.clock.get_fps())),20,BLACK,20,15)
        if pg.time.get_ticks()< 14000:
            self.draw_text("Your melting!", 22, BLACK,self.player.pos.x,550)
            self.draw_text("Collect falling snowballs and avoid falling rocks", 22, BLACK,WIDTH/2+200,330)
        
        self.score = round((pg.time.get_ticks()-self.mins)/1000)
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_start_screen(self):

        self.screen.blit(self.bg,self.bg_rect)
        self.screen.blit(self.player_image, (300,300))
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("arrow keys or A,D to move", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play",22, WHITE, WIDTH/2, HEIGHT*3/4)

        pg.display.flip()
        self.wfk()

        

    def wfk(self,keyp = None):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    self.quit()
                if keyp == None:
                    if event.type == pg.KEYUP:
                        waiting = False
                else:
                    if event.type == pg.KEYUP:
                        if event.key == keyp:
                            waiting = False


    def show_go_screen(self):
        self.screen.blit(self.bg,self.bg_rect)
        self.screen.blit(self.player_image, (300,300))
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text("You Melted!!", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Your socre was: "+str(self.score), 22, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Press [SPACE] to play again",22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.wfk(pg.K_SPACE)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()