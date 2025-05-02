import pygame as pg


pg.init()


# Main objects

class Game:
    def __init__(self, width = 1360, height = 768, fps = 60, title = "My game", icon = None, map = None):
        self.width, self.height, self.fps, self.title, self.icon = width, height, fps, title, icon
        self.screen = pg.display.set_mode((width, height))
        self.map = map

    def draw_object(self, object):
        object.draw(self.screen)

    def if_exit(self, value):
        for i in pg.event.get():
            if i.type == pg.QUIT:
                value = False
                pg.quit()

    def completion(self):
        pg.display.update()
        pg.time.Clock().tick(self.fps)

    def draw_map(self):
        self.map.draw(self.screen)

    def set_map(self, map):
        self.map = map

class Map:
    def __init__(self, config, player):
        self.tiles = config["tiles"]
        self.tile_images = config["tile_images"]
        self.tile_size = config["tile_size"]
        self.objects = config["objects"]
        self.hostiles = config["hostiles"]
        self.all_items = config["items"]
        self.player = player

    def draw(self, screen):
        for row_index, row in enumerate(self.tiles):
            for col_index, col in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                
                screen.blit(self.tile_images[col], (x, y))

        for i in self.objects:
            i.draw(screen)
            i.walk()

        for i in self.all_items:
            i.draw(screen)

        for i in self.hostiles:
            i.draw(screen)
            i.following()


# Characters

class Entity:
    def __init__(self, image, x, y, speed = 0, health = 50, damage = 10):
        self.image, self.x, self.y, self.speed, self.health = pg.image.load(image), x, y, speed, health
        self.alive = True
        self.damage = damage
        self.health = health
        self.rect = pg.Rect(self.x, self.y, 100, 100)
        self.inventory = []
        self.current_inventory = []

    def draw(self, screen):
        if self.alive:
            self.rect.topleft = self.x, self.y
            screen.blit(self.image, (self.x, self.y))

        if self.health < 0:
            self.alive = False

class Player(Entity):
    def __init__(self, image, x, y, speed = 0, health = 50, damage = 10):
        super().__init__(image, x, y, speed, health, damage)

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))
            self.rect.topleft = (self.x, self.y)
            self.walk()

        if self.health <= 0:
            self.alive = False

    def walk(self):
        key = pg.key.get_pressed()

        if self.alive:
            if key[pg.K_w]:
                self.y -= self.speed

            if key[pg.K_s]:
                self.y += self.speed
                
            if key[pg.K_a]:
                self.x -= self.speed

            if key[pg.K_d]:
                self.x += self.speed           

class Enemy(Entity):
    def __init__(self, image, x, y, player, speed, health = 50, damage = 5):
        super().__init__(image, x, y, speed, health, damage)
        self.player = player
        self.detect_rect = pg.Rect(self.x + 32, self.y + 32, 512, 512)
        self.text_health = pg.font.Font(None, 20).render(str(self.health), True, ("red"))
        self.timer = 0

    def following(self):
        if self.player.rect.colliderect(self.detect_rect):
            print(self.player.x)
            if self.x > self.player.x:
                self.x -= self.speed

            if self.x < self.player.x:
                self.x += self.speed

            if self.y > self.player.y:
                self.y -= self.speed
            
            if self.y < self.player.y:
                self.y += self.speed

            if self.timer != 60:
                self.timer += 1
            else:
                self.attack()
                self.timer = 0

    def attack(self):
        if self.alive:
            if self.rect.colliderect(self.player.rect):
                if self.player.alive:
                    mouse = pg.mouse.get_pos()
                    key = pg.mouse.get_pressed()

                    self.player.health -= self.damage
                    self.player.x -= 20
                    self.x += 20

                    if self.rect.collidepoint(mouse[0], mouse[1]): 
                        print(mouse[0], mouse[1])
                        if key[0]:
                            self.health -= self.player.damage

    def draw(self, screen):
        if self.alive:
            self.detect_rect = pg.Rect(self.x - 256, self.y - 256, 512, 512)
            self.rect = pg.Rect(self.x, self.y, 100, 100)
            screen.blit(self.text_health, (self.x + 25, self.y - 15))
            screen.blit(self.image, (self.x, self.y))
            self.following()

class ItemEntity:
    def __init__(self, image, name, type, speed = 0, health = 50, damage = 10):
        self.image, self.speed, self.health = image, speed, health
        self.alive = True
        self.damage = damage
        self.health = health
        self.inventory = []
        self.name = name
        self.type = type

    def draw(self, screen, slot):
        mouse_pos = pg.mouse.get_pos()

        if self.alive:
            self.rect = pg.Rect(slot[0], slot[1], 100, 100)
            screen.blit(self.image, (slot[0], slot[1]))

        if self.health < 0:
            self.alive = False

class DroppedItem:
    def __init__(self, image, x, y, player, item, speed=0, health=50, damage=10):
        self.item = item
        self.image = image
        self.x, self.y, self.speed, self.health, self.damage = x, y, speed, health, damage
        self.player = player
        self.rect = pg.Rect(self.x, self.y, 64, 64)
        self.alive = True
    
    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))
            self.rect.topleft = self.x, self.y

            if self.rect.colliderect(self.player.rect):
                if self.item.type == "weapon":
                    if len(self.player.current_inventory) < 1: 
                        self.player.current_inventory.append(self.item)

                else:
                    self.player.inventory.append(self.item)

                self.alive = False
                self.player.damage += self.item.damage

class MineObject(Entity):
    def __init__(self, image, x, y, speed=0, health=50, damage=10, item=None):
        super().__init__(image, x, y, speed, health, damage)
        self.item = item
        self.alive = True
        self.rect = pg.Rect(self.x, self.y, 64, 64)

    def draw(self, screen, player, map):
        key = pg.mouse.get_pressed()
        if self.alive:
            self.rect.topleft = self.x, self.y
            screen.blit(self.image, (self.x, self.y))
            if self.rect.colliderect(player.rect):
                if key[0]:
                    self.health -= self.player.damage

        if self.health < 0:
            self.alive = False
            map["items"].append(DroppedItem(self.item.image, self.x, self.y + 100, player, self.item))

        


        

