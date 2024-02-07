import pygame
from sys import exit
import config
import componente
import populatie

pygame.init()
clk = pygame.time.Clock()
populatie = populatie.Population(100)

def generate_pipes():
    config.pipes.append(componente.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10

    while True:
        quit_game()

        config.window.fill((173, 216, 230))

        config.ground.draw(config.window)

        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200

        pipes_spawn_time -= 1

        for pipe in config.pipes:
            pipe.draw (config.window)
            pipe.update ()
            if pipe.off_screen:
                config.pipes.remove(pipe)
                for player in populatie.players:
                    if not player.coliziune_conducte() and not player.coliziune_cer() and player.alive:
                        player.score += 1
                        # Actualizare highscore
                        if player.score > config.highscore:
                            config.highscore = player.score

        if not populatie.extinct():
            populatie.update_live_players()
        else:
            config.pipes.clear()
            populatie.selectie_naturala()

        clk.tick (60)
        pygame.display.flip()

if __name__ == "__main__":
    main()