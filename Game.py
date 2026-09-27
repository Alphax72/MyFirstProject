import pygame
import time
import random
import gif_pygame
pygame.init()
pygame.font.init() #intializes fonts

pygame.mixer.init() #intilizes music
pygame.mixer.music.load("Space.mp3")
pygame.mixer.music.play()

width, height = 1000, 700
window = pygame.display.set_mode((width,height)) 
pygame.display.set_caption("Space Dodge") #Creates window named "Space Dodge"

gif = gif_pygame.load("Jumpscare.gif")
BG = pygame.transform.scale(pygame.image.load("space.jpg"),(width,height))

Player_width = 40
Player_height = 60
Player_velocity = 5

Star_width = 10
Star_height = 20
Star_velocity = 3

Font = pygame.font.SysFont("Arial", 30)

pygame.mixer.music.set_volume(0.3)


def draw(player, elapsed_time, stars): #adds the image to the window
    window.blit(BG,(0,0)) #0,0 is the top left of pygame windows
    time_text = Font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    window.blit(time_text,(10,10))
    pygame.draw.rect(window, "red", player)
    for star in stars:
        pygame.draw.rect(window, "white", star)

    pygame.display.update() #will update the game for everything

def jumpscare():
    for _ in range(9):
        current_frame_surface = gif.blit_ready()
        scaled_frame = pygame.transform.scale(current_frame_surface, (width, height))
        window.blit(scaled_frame, (0, 0))
        pygame.display.update() 
        pygame.time.delay(100)   

def main():
    run = True
    clock = pygame.time.Clock() #creates clock
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000 #miliseconds
    star_count = 0
    stars = []
    hit = False

    player = pygame.Rect(200, height-Player_height, Player_width, Player_height)
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment:
            for _ in range (3):
                star_x = random.randint(0,width-Star_width)
                star = pygame.Rect(star_x,-Star_height, Star_width, Star_height)
                stars.append(star)

            star_add_increment = max(200,star_add_increment- 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-Player_velocity>=0:
            player.x -= Player_velocity
        if keys[pygame.K_RIGHT] and player.x+Player_velocity + player.width <= width:
            player.x += Player_velocity

        for star in stars[:]:
            star.y += Star_velocity
            if star.y > height:
                stars.remove(star)
            elif star.y + Star_height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        if hit:
            lost_text = Font.render("You Lost!", 1, "white")
            score_text = Font.render("Your score was: "+str(round(elapsed_time,1))+"!",1,"white")
            window.blit(lost_text,(width/2-lost_text.get_width()/2, height/2-lost_text.get_height()/2-25))
            window.blit(score_text,(width/2-score_text.get_width()/2, height/2-score_text.get_height()/2+25))
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Lose.mp3")
            pygame.mixer.music.play()
            pygame.time.delay(1500)
            pygame.display.update()
            pygame.time.delay(1500)
            pygame.mixer.music.load("FNAFScream.mp3")
            pygame.mixer.music.play()
            jumpscare()

            break
        draw(player, elapsed_time, stars)
    pygame.quit()

if __name__ == "__main__":
    main()

