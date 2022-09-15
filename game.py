from distutils import extension
import pygame
import random
import os

# Constants 常量
W, H = 288, 512
FPS = 30

# Setup 设置
pygame.init()
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()

# Materials 素材
IMAGES = {}
for image in os.listdir('assets/sprites/'):
    name, extension = os.path.splitext(image)
    path = os.path.join('assets/sprites', image)
    IMAGES[name] = pygame.image.load(path)

print(IMAGES)

FLOOR_Y = H - IMAGES['floor'].get_height()
FLOOR_GAP = IMAGES['floor'].get_width() -W
#sound resoures
AUDIO = {}
for audio in os.listdir('assets/audio/'):
    name, extension = os.path.splitext(audio)
    path = os.path.join('assets/audio', audio)
    AUDIO[name] = pygame.mixer.Sound(path)

def main():
    while True:
        AUDIO['start'].play()
        IMAGES['bgpic'] = IMAGES[random.choice(['day','night'])]
        color = random.choice(['red', 'yellow', 'blue'])
        IMAGES['birds'] = [IMAGES[color+'-up'], IMAGES[color+'-mid'], IMAGES[color+'-down']] 
        pipe = IMAGES[random.choice(['green-pipe','red-pipe'])]
        IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe, False, True)]
        menu_window()
        game_window()
        end_window()
        
def menu_window():
    floor_x = 0

    guide_x = (W - IMAGES['guide'].get_width())/2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height())/2
    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height())/2
    bird_y_vel = 1
    bird_y_range = [bird_y - 8, bird_y + 8]

    idx = 0
    repeat = 5
    frames = [0]*repeat + [1]*repeat + [2]*repeat + [1]*repeat
    while True:      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        
        floor_x -= 4
        if floor_x <= -FLOOR_GAP:
            floor_x = 0

        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1

        idx += 1
        idx %= len(frames)

        SCREEN.blit(IMAGES['day'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x, bird_y))
        pygame.display.update()
        CLOCK.tick(FPS)
    

def game_window():
    floor_x = 0
    bird = Bird(W*0.2, H*0.4)
    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap = True
                    AUDIO['flap'].play()
                    
        floor_x -= 4
        if floor_x <= -FLOOR_GAP:
            floor_x = 0

        bird.update(flap)

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['pipes'][0], (W/2, H/2))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)

def end_window():
    gameover_x = (W - IMAGES['gameover'].get_width())/2
    gameover_y = (FLOOR_Y - IMAGES['gameover'].get_height())/2
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (0, FLOOR_Y))  
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        SCREEN.blit(IMAGES['birds'][0], (W/2, H*0.3))
        pygame.display.update()
        CLOCK.tick(FPS)

class Bird:
    def __init__(self, x, y):
        repeat = 5
        self.frames = [0]*repeat + [1]*repeat + [2]*repeat + [1]*repeat
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = IMAGES['birds'][self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = -10
        self.max_y_vel = 10
        self.gravity = 1
        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3
        self.y_ve_after_flap = -10
        self.rotate_after_flap = 45

    def update(self, flap=False):
        if flap:
            self.y_vel = self.y_ve_after_flap
            self.rotate = self.rotate_after_flap

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate+self.rotate_vel, self.max_rotate)
        
        self.idx += 1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image, self.rotate)

main()