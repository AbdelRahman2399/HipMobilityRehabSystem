import pygame
import random
import socket
pygame.font.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sharky!")

BG = pygame.transform.scale(pygame.image.load("underwater.jpg"), (WIDTH, HEIGHT))


SHARKY_WIDTH = 40
SHARKY_HEIGHT = 60

SHARKY = pygame.transform.scale(pygame.image.load("shark.png"), (SHARKY_WIDTH, SHARKY_HEIGHT))

SHARKY_VEL = 5

FISH_WIDTH = 30
FISH_HEIGHT = 20

FISH = pygame.transform.scale(pygame.image.load("fish.png"), (FISH_WIDTH, FISH_HEIGHT))


FONT = pygame.font.SysFont("comicsans", 30)

def draw(sharky, score, fish):
    WIN.blit(BG, (0, 0))
    
    score = FONT.render(f"Score: {round(score)}", 1, "white")
    WIN.blit(score, (10, 10))
    
    WIN.blit(SHARKY, (sharky.x, sharky.y))
    WIN.blit(FISH, (fish.x,fish.y))
    
    pygame.display.update()
    
def main():
    run = True

    clock = pygame.time.Clock()
    
    hit = False
    
    sharky = pygame.Rect(400, 400, SHARKY_WIDTH, SHARKY_HEIGHT)
    fish = pygame.Rect(200, 200, FISH_WIDTH, FISH_HEIGHT)
    score = 0
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))
    
    sharky.x = 400
    sharky.y = 400
    
    draw(sharky, score, fish)
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        msg = s.recv(1024)
        pos = msg.decode("utf-8")
        pos = pos.split(",")
        sharky.x = 400*-float(pos[1][1:-2]) + 400
        sharky.y = 400*-float(pos[0][1:-2]) + 400
        if sharky.x < 0:
            sharky.x = 0
        elif sharky.x + SHARKY_WIDTH > WIDTH:
            sharky.x = WIDTH - SHARKY_WIDTH
        
        if sharky.y < 0:
            sharky.y = 0
        elif sharky.y + SHARKY_HEIGHT > HEIGHT:
            sharky.y = HEIGHT - SHARKY_HEIGHT        
            
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT] and sharky.x - SHARKY_VEL >= 0:
        #    sharky.x -= SHARKY_VEL
        #if keys[pygame.K_RIGHT] and sharky.x + SHARKY_VEL + SHARKY_WIDTH <= WIDTH:
        #    sharky.x += SHARKY_VEL
        #if keys[pygame.K_UP] and sharky.y - SHARKY_VEL >= 0:
        #    sharky.y -= SHARKY_VEL
        #if keys[pygame.K_DOWN] and sharky.y + SHARKY_VEL + SHARKY_HEIGHT <= WIDTH:
        #    sharky.y += SHARKY_VEL
            
        if sharky.colliderect(fish):
            #fish.x = random.randint(0, WIDTH - FISH_WIDTH)
            #fish.y = random.randint(0, HEIGHT - FISH_HEIGHT)
            fish.x = random.randint(200, 600)
            fish.y = random.randint(200, 600)
            score += 10
        
        draw(sharky, score, fish)

    pygame.quit()        
    
if __name__ == "__main__":
    main()
            
        
        
    
    
    