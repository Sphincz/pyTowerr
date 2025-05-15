import random

import pygame as pg
import math
import settings


class Tower(pg.sprite.Sprite):
    def __init__(self, tower_id, tower_type, tower_spritesheets, tile_x, tile_y, angle):
        pg.sprite.Sprite.__init__(self)
        self.tower_id = tower_id
        self.tower_type = tower_type
        self.upgrade_level = 1
        self.range = settings.TOWER_TYPES[tower_type].get("range")
        self.last_shot = pg.time.get_ticks()
        self.last_shot_time = 0  # Time since the last shot
        self.target = None
        self.is_shooting = False

        # Initialize default tower stats with the 'worst' values from settings
        self.accuracy = 0.01  # Worst accuracy is the lowest value
        _, cooldown_max = settings.TOWER_TYPES[tower_type]['cooldown']
        self.cooldown = cooldown_max  # Worst cooldown is the highest value
        range_min, _ = settings.TOWER_TYPES[tower_type]['range']
        self.range = range_min  # Worst range is the smallest value
        damage_min, _ = settings.TOWER_TYPES[tower_type]['damage']
        self.damage = damage_min  # Worst damage is the smallest value
        self.crit_chance = 0.0  # Worst critical chance is 0.0

        # position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.angle = angle
        # calculate center coordinates
        self.x = (self.tile_x + 0.5) * settings.TILE_SIZE
        self.y = (self.tile_y + 0.5) * settings.TILE_SIZE
        # shot sound effect
        self.shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
        self.shot_fx.set_volume(0.5)

        # animation variables
        self.sprite_sheets = tower_spritesheets
        self.animation_list = self.load_images(self.sprite_sheets[int(self.tower_type[-1]) - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # update image
        self.angle = angle
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        # Params for Genetic Algorithm
        self.strategy_params = {
            "accuracy": self.accuracy,
            "cooldown": self.cooldown,
            "range": self.range,
            "damage": self.damage,
            "crit_chance": self.crit_chance
        }

    def update_strategy_params(self, best_solution):
        self.accuracy, self.cooldown, self.range, self.damage, self.crit_chance = best_solution
        self.strategy_params = {
            "accuracy": self.accuracy,
            "cooldown": self.cooldown,
            "range": self.range,
            "damage": self.damage,
            "crit_chance": self.crit_chance
        }

    @staticmethod
    def load_images(sprite_sheet):
        # extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(settings.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def pick_target(self, enemy_group):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemy_group:
            distance = self.calculate_distance(enemy)
            if distance < self.range:
                if distance < closest_distance:
                    closest_enemy = enemy
                    closest_distance = distance

        self.target = closest_enemy
        # if self.target:
        #    self.angle = self.calculate_angle(self.target)
        #    print(self.angle)

    def calculate_distance(self, enemy):
        x_dist = enemy.pos[0] - self.x
        y_dist = enemy.pos[1] - self.y
        return math.sqrt(x_dist ** 2 + y_dist ** 2)

    def calculate_angle(self, enemy):
        x_dist = enemy.pos[0] - self.x
        y_dist = enemy.pos[1] - self.y
        return math.degrees(math.atan2(-y_dist, x_dist))  # Convert to degrees

    def shoot(self, current_time):
        if self.target and current_time - self.last_shot_time >= self.strategy_params["cooldown"]:
            self.angle = self.calculate_angle(self.target)
            self.last_shot_time = current_time
            self.is_shooting = True

            # Check for hit success
            if self.is_hit_successful():
                damage = self.strategy_params['damage']
                critical_hit = random.random() <= self.strategy_params['crit_chance']
                if critical_hit:
                    damage *= 2  # Double damage
                self.target.health -= damage

                print(
                    f"Tower {self.tower_id} # Hit enemy at position {self.target.pos}. "
                    f"Accuracy: {round(self.strategy_params['accuracy'], 3)}, "
                    f"Damage: {damage}.",
                    f"Critical Chance: {round(self.strategy_params['crit_chance'], 2)}, "
                    f"Critical Hit: {critical_hit}." if critical_hit else "")
                self.shot_fx.play()
            else:
                print(f"Tower {self.tower_id} # Missed shot")

    def is_hit_successful(self):
        # Determine if the shot hits based on the accuracy parameter
        accuracy = self.strategy_params['accuracy']
        hit_chance = random.random()
        return hit_chance <= accuracy

    def update(self, enemy_group, current_time, world):
        self.pick_target(enemy_group)
        if self.target:
            self.shoot(current_time)
            self.play_animation(current_time)
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def play_animation(self, current_time):
        if self.is_shooting:
            if current_time - self.update_time > settings.ANIMATION_DELAY:
                self.update_time = current_time
                self.frame_index += 1
                # Check if all frames have been parsed
                if self.frame_index >= len(self.animation_list):
                    self.frame_index = 0  # Reset frame index
                    self.is_shooting = False  # Stop animation
                # Update image based on the current frame
                self.original_image = self.animation_list[self.frame_index]

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)

        # Draw the range circle
        pg.draw.circle(surface, pg.Color("blue"), (int(self.x), int(self.y)), self.range, 1)

        # Draw a line to the target if it exists and is within range
        if self.target and self.calculate_distance(self.target) <= self.range:
            pg.draw.line(surface, pg.Color("red"), (self.x, self.y), (self.target.pos[0], self.target.pos[1]), 1)
