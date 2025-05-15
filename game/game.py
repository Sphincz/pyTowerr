import threading

import pygame as pg
import json

from enemies.enemy import Zombie, Warrior
from game.world import World
from game.button import Button
from algorithms.genetic_algorithm import GeneticAlgorithm

import settings


class Game:
    screen = None
    clock = None
    game_over = False
    game_outcome = 0  # -1 the user loses & 1 the user wins
    level_started = False
    last_enemy_spawn = pg.time.get_ticks()
    tower_spritesheets = []
    world = None
    world_data = None
    map_image = None

    def __init__(self, clock, screen):
        # game variables
        self.restart_button = None
        self.fast_forward_button = None
        self.enemy_group = None
        self.send_wave_button = None
        self.clock = clock
        self.screen = screen
        self.wave_number_text = 0
        # load images
        self.map_image = pg.image.load('levels/level.png').convert_alpha()
        # enemies
        self.enemy_images = {
            "zombie": pg.image.load('assets/images/enemies/zombie.png').convert_alpha(),
            "warrior": pg.image.load('assets/images/enemies/warrior.png').convert_alpha(),
        }
        # buttons
        self.start_train_image = pg.image.load('assets/images/buttons/start-train.png').convert_alpha()
        self.send_wave_image = pg.image.load('assets/images/buttons/send-wave.png').convert_alpha()
        self.restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
        self.fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
        self.exit_image = pg.image.load('assets/images/buttons/exit-game.png').convert_alpha()

        # load json data for wave_number
        with open('levels/level.tmj') as file:
            self.world_data = json.load(file)

        # load fonts for displaying text on the screen
        self.text_font = pg.font.SysFont("Consolas", 24, bold=True)
        self.large_font = pg.font.SysFont("Consolas", 36)

        # create world
        self.world = World(self.world_data, self.map_image)
        self.world.process_data()
        self.world.process_enemies()

        # create groups
        self.enemy_group = pg.sprite.Group()

        # create buttons
        self.start_train_button = Button(settings.SCREEN_WIDTH + 60, 250, self.start_train_image, True)
        self.send_wave_button = Button(settings.SCREEN_WIDTH + 60, 325, self.send_wave_image, True)
        self.restart_button = Button(310, 300, self.restart_image, True)
        self.fast_forward_button = Button(settings.SCREEN_WIDTH + 55, 400, self.fast_forward_image, False)
        self.restart_button_2 = Button(settings.SCREEN_WIDTH + 45, 475, self.restart_image, True)
        self.exit_button = Button(settings.SCREEN_WIDTH + 60, settings.SCREEN_HEIGHT - 100, self.exit_image, True)

        # GA hyperparameters
        # self.num_generations = None
        # self.num_genes = None
        # self.population_size = None

        # GA helper variables
        self.generation_number = None
        self.ga_instance = None
        self.ga_thread = None
        self.ga_running = None
        self.best_solution = None
        self.best_solution_fitness = 0.0
        self.ga_train_button_active = True

    # function for outputting text onto the screen
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def display_data(self):
        # draw panel
        pg.draw.rect(self.screen, "midnightblue",
                     (settings.SCREEN_WIDTH, 0, settings.SIDE_PANEL, settings.SCREEN_HEIGHT))
        pg.draw.rect(self.screen, "grey100", (settings.SCREEN_WIDTH, 0, settings.SIDE_PANEL, settings.SCREEN_HEIGHT), 2)
        # display data
        self.draw_text(("Generation: " + str(self.generation_number)), self.text_font, "grey100",
                       settings.SCREEN_WIDTH + 10, 10)
        self.draw_text("Fitness: " + str(round(self.best_solution_fitness, 3)), self.text_font, "grey100",
                       settings.SCREEN_WIDTH + 10, 40)
        self.draw_text("Wave: " + str(self.wave_number_text), self.text_font, "grey100", settings.SCREEN_WIDTH + 10,
                       70)
        self.draw_text("Enemies killed: " + str(self.world.killed_enemies), self.text_font, "grey100",
                       settings.SCREEN_WIDTH + 10, 100)
        self.draw_text("Enemies escaped: " + str(self.world.missed_enemies), self.text_font, "grey100",
                       settings.SCREEN_WIDTH + 10, 130)
        self.draw_text("Health: " + str(self.world.health), self.text_font, "grey100",
                       settings.SCREEN_WIDTH + 10, 160)

    def reset_game(self):
        self.game_over = False
        self.level_started = False
        self.ga_train_button_active = True
        self.wave_number_text = 0
        self.last_enemy_spawn = pg.time.get_ticks()
        self.world = World(self.world_data, self.map_image)
        self.world.process_data()
        self.world.process_enemies()
        self.enemy_group.empty()

    def run_ga_in_thread(self):
        if self.ga_thread and self.ga_thread.is_alive():
            return  # GA is already running
        self.ga_running = True
        self.ga_thread = threading.Thread(target=self.run_ga)
        self.ga_thread.start()

    def run_ga(self):
        # Assuming a way to determine the tower type (typically from world.towers)
        first_tower_type = self.world.towers[0].tower_type
        self.ga_instance = GeneticAlgorithm(first_tower_type)
        self.ga_instance.run()
        self.ga_running = False
        top_solutions, top_fitnesses = self.ga_instance.get_best_solution(6)  # Retrieve top 6 solutions
        # Update total fitness score for all towers
        self.best_solution_fitness = sum(top_fitnesses) / len(top_fitnesses)
        # Print the top solutions and their fitness scores
        for i, solution in enumerate(top_solutions):
            print(f"Tower #{i + 1}: Best Accuracy: {round(solution[0], 2)}, Best Cooldown: {solution[1]}, "
                  f"Best Range: {solution[2]}, Best Firepower: {solution[3]}, Critical Chance: {round(solution[4], 2)}",
                  f"Fitness score: {round(top_fitnesses[i], 2)}")
        # Update the tower strategies with the top solutions
        self.update_tower_strategies(top_solutions)

    def update_tower_strategies(self, top_solutions):
        self.generation_number = self.ga_instance.get_current_generation()
        # Update the strategy parameters for each tower
        for i, tower in enumerate(self.world.towers):
            best_solution = top_solutions[i % len(top_solutions)]
            tower.update_strategy_params(best_solution)

    def run(self):
        run = True
        while run:
            self.clock.tick(settings.FPS)

            if not self.game_over:
                # check if player has lost
                if self.world.health <= 0:
                    self.game_over = True
                    self.game_outcome = -1  # lose
                # check if player has won
                if self.world.wave_number > settings.TOTAL_WAVES:
                    self.game_over = True
                    self.game_outcome = 1  # win

                # update groups
                self.enemy_group.update(self.world)
                # self.world.tower_group.update(self.enemy_group, self.world)
                current_time = pg.time.get_ticks()
                for tower in self.world.tower_group:
                    tower.update(self.enemy_group, current_time, self.world)

                # draw world
                self.world.draw(self.screen)

                # draw groups
                self.enemy_group.draw(self.screen)
                for tower in self.world.tower_group:
                    tower.draw(self.screen)

                # display info
                self.display_data()

                # exit game
                if self.exit_button.draw(self.screen):
                    run = False

                if not self.game_over:
                    # Run GA in a separate thread
                    if not self.ga_running and self.ga_train_button_active:
                        if self.start_train_button.draw(self.screen):
                            self.run_ga_in_thread()

                # check if the wave_number has been started or not
                if not self.level_started:
                    if self.send_wave_button.draw(self.screen) or pg.key.get_pressed()[pg.K_SPACE]:
                        self.level_started = True
                        self.wave_number_text += 1
                        self.ga_train_button_active = False
                else:
                    # fast-forward option
                    self.world.game_speed = 1
                    if self.fast_forward_button.draw(self.screen):
                        self.world.game_speed = 5
                    if self.restart_button_2.draw(self.screen):
                        self.reset_game()
                    # spawn enemies
                    if pg.time.get_ticks() - self.last_enemy_spawn > settings.SPAWN_COOLDOWN:
                        if self.world.spawned_enemies < len(self.world.enemy_list):
                            enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                            if enemy_type == "zombie":
                                enemy = Zombie(self.world.waypoints, self.enemy_images)
                            elif enemy_type == "warrior":
                                enemy = Warrior(self.world.waypoints, self.enemy_images)
                            self.enemy_group.add(enemy)
                            self.world.spawned_enemies += 1
                            self.last_enemy_spawn = pg.time.get_ticks()

                # check if the wave is finished
                if self.world.check_level_complete():
                    self.world.wave_number += 1
                    self.level_started = False
                    self.last_enemy_spawn = pg.time.get_ticks()
                    self.world.reset_level()
                    if self.world.wave_number < settings.TOTAL_WAVES:
                        self.world.process_enemies()
                    else:
                        self.game_over = True
                        self.game_outcome = 1  # win
            else:
                pg.draw.rect(self.screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
                if self.game_outcome == -1:
                    self.draw_text("GAME OVER", self.large_font, "grey0", 310, 230)
                elif self.game_outcome == 1:
                    self.draw_text("YOU WIN!", self.large_font, "grey0", 315, 230)
                # restart game
                if self.restart_button.draw(self.screen):
                    self.reset_game()

            # event handler
            for event in pg.event.get():
                # quit program
                if event.type == pg.QUIT:
                    run = False
            # update display
            pg.display.flip()

        pg.quit()
