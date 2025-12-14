import pygame
import random
import sys
import os
import json

# ---------- Config ----------
WIDTH, HEIGHT = 800, 600
FPS = 60

SCORE_RATE_PER_SEC = 50

PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_START_HEALTH = 3
PLAYER_MAX_HEALTH = 5

DOG_SIZE = 50
DOG_SPEED_MIN = 3
DOG_SPEED_MAX = 6

POWER_SIZE = 35
POWER_SPEED = 3

HIGHSCORE_FILE = "highscore.json"
# ----------------------------

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NYAWNYAWNYAW - Cat Run")
clock = pygame.time.Clock()

# ---------- Asset Loader ----------
def safe_image_load(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((200,200,200,255))
        pygame.draw.rect(surf,(100,100,100),surf.get_rect(),2)
        return surf

def safe_sound_load(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

cat_img   = safe_image_load("cat.png",   (PLAYER_SIZE, PLAYER_SIZE))
dog_img   = safe_image_load("dog.png",   (DOG_SIZE, DOG_SIZE))
power_img = safe_image_load("power.png", (POWER_SIZE, POWER_SIZE))
heart_img = safe_image_load("heart.png", (25,25))

hit_sound   = safe_sound_load("hit.wav")
power_sound = safe_sound_load("power.wav")

try:
    pygame.mixer.music.load("bgm.wav")
    pygame.mixer.music.play(-1)
except:
    pass

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)

# ---------- Utils ----------
def clamp(v,a,b): return max(a,min(b,v))

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE,"r") as f:
                return json.load(f)
        except:
            return {"highscore":0}
    return {"highscore":0}

def save_highscore(data):
    try:
        with open(HIGHSCORE_FILE,"w") as f:
            json.dump(data,f)
    except:
        pass

# ---------- Entity ----------
class Entity:
    def __init__(self,x,y,speed,size,img):
        self.x=x; self.y=y; self.speed=speed
        self.size=size; self.img=img

    def draw(self): screen.blit(self.img,(int(self.x),int(self.y)))
    def update(self,dt): pass
    def rect(self):
        return pygame.Rect(int(self.x),int(self.y),self.size,self.size)


# ---------- Player ----------
class Player(Entity):
    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_SPEED,PLAYER_SIZE,cat_img)
        self.__health = PLAYER_START_HEALTH
        self.max_health = PLAYER_MAX_HEALTH

        self.score_float = 0.0
        self.score = 0

    def move(self,keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.y += self.speed

        self.x = clamp(self.x,0,WIDTH-self.size)
        self.y = clamp(self.y,0,HEIGHT-self.size)

    def take_damage(self):
        if self.__health>0:
            self.__health-=1
            if hit_sound: hit_sound.play()

    def heal(self):
        if self.__health < self.max_health:
            self.__health+=1
            if power_sound: power_sound.play()

    @property
    def health(self): return self.__health
    def is_alive(self): return self.__health>0


# ---------- Dog ----------
class Dog(Entity):
    def __init__(self):
        speed = random.randint(DOG_SPEED_MIN, DOG_SPEED_MAX)
        x = random.randint(0, WIDTH - DOG_SIZE)
        y = random.randint(-400, -40)
        super().__init__(x,y,speed,DOG_SIZE,dog_img)

    def update(self,dt):
        self.y += self.speed
        if self.y > HEIGHT: self.respawn()

    def respawn(self):
        self.y = random.randint(-400,-40)
        self.x = random.randint(0,WIDTH-self.size)
        self.speed = random.randint(DOG_SPEED_MIN, DOG_SPEED_MAX)


# ---------- Powerup ----------
class PowerUp(Entity):
    def __init__(self):
        x = random.randint(0,WIDTH-POWER_SIZE)
        y = random.randint(-800,-40)
        super().__init__(x,y,POWER_SPEED,POWER_SIZE,power_img)

    def update(self,dt):
        self.y += self.speed
        if self.y > HEIGHT: self.respawn()

    def respawn(self):
        self.y = random.randint(-800,-40)
        self.x = random.randint(0,WIDTH-self.size)


# ---------- Game ----------
class Game:
    def __init__(self):
        self.player = Player(WIDTH//2, HEIGHT - 100)
        self.dogs = [Dog() for _ in range(4)]  # FIXED amount (infinite mode)
        self.powerup = PowerUp()

        self.entities = []
        self.refresh_entities()

        self.running=True
        self.paused=False

        self.highscore = load_highscore()

    def refresh_entities(self):
        self.entities = self.dogs[:] + [self.powerup, self.player]

    def show_center(self,text,y,font_obj=None,color=RED):
        f = font_obj if font_obj else big_font
        surf = f.render(text,True,color)
        screen.blit(surf,(WIDTH//2 - surf.get_width()//2,y))

    def menu(self):
        while True:
            screen.fill(WHITE)
            self.show_center("NYAWNYAWNYAW",100)
            play = font.render("Press ENTER to Play",True,BLACK)
            quitx = font.render("Press ESC to Quit",True,BLACK)
            hs = font.render(f"Highscore: {self.highscore.get('highscore',0)}",True,BLACK)

            screen.blit(play,(WIDTH//2 - play.get_width()//2,260))
            screen.blit(quitx,(WIDTH//2 - quitx.get_width()//2,300))
            screen.blit(hs,(WIDTH//2 - hs.get_width()//2,360))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: return
                    if event.key == pygame.K_ESCAPE: sys.exit()

            pygame.display.update()
            clock.tick(FPS)

    def run(self):
        self.menu()

        while self.running:
            dt_ms = clock.tick(FPS)
            dt = dt_ms / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

            if self.paused:
                screen.fill(WHITE)
                self.show_center("PAUSED",HEIGHT//2 - 20)
                pygame.display.update()
                continue

            keys = pygame.key.get_pressed()
            self.player.move(keys)

            # ---------- FIXED SCORING ----------
            self.player.score_float += SCORE_RATE_PER_SEC * dt
            self.player.score = int(self.player.score_float)
            # -----------------------------------

            for e in self.entities:
                e.update(dt)

            p_rect = self.player.rect()

            for d in self.dogs:
                if d.rect().colliderect(p_rect):
                    self.player.take_damage()
                    d.respawn()

            if self.powerup.rect().colliderect(p_rect):
                self.player.heal()
                self.powerup.respawn()

            # Draw
            screen.fill(WHITE)

            for e in self.entities:
                e.draw()

            score_surf = font.render(f"Score: {self.player.score}",True,BLACK)
            screen.blit(score_surf,(10,10))

            # Health
            for i in range(self.player.health):
                screen.blit(heart_img,(WIDTH - (i+1)*30,10))

            if not self.player.is_alive():
                self.show_center("GAME OVER",HEIGHT//2-20)
                pygame.display.update()
                pygame.time.wait(1000)
                self.running=False

            pygame.display.update()

        self.end_screen()

    def end_screen(self):
        if self.player.score > self.highscore.get("highscore",0):
            self.highscore["highscore"] = self.player.score
            save_highscore(self.highscore)

        while True:
            screen.fill(WHITE)
            self.show_center("GAME OVER",100)
            s = font.render(f"Your Score: {self.player.score}",True,BLACK)
            hs = font.render(f"Highscore: {self.highscore['highscore']}",True,BLACK)
            retry = font.render("Press ENTER to Play Again",True,BLACK)
            quitx = font.render("Press ESC to Quit",True,BLACK)

            screen.blit(s,(WIDTH//2 - s.get_width()//2,240))
            screen.blit(hs,(WIDTH//2 - hs.get_width()//2,280))
            screen.blit(retry,(WIDTH//2 - retry.get_width()//2,330))
            screen.blit(quitx,(WIDTH//2 - quitx.get_width()//2,360))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__init__()
                        self.run()
                        return
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            pygame.display.update()
            clock.tick(FPS)


# ---------- Run ----------
if __name__ == "__main__":
    Game().run()
