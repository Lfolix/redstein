import pygame as pg
import objects as obj

import sys
sys.path.append("modules")
sys.path.append("modules/inventory")

import interface
import inventory
import current_inventory


pg.init()


player = obj.Player("characters/player_1.png", 0, 0, 3, attack_distance=500)
id = obj.ItemIDGenerator()


map_1_config = {
    "tiles" : [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],

    "tile_images" : {
        0 : pg.image.load("tiles/grass.png"),
        1 : pg.image.load("tiles/wood.png"),
        2 : pg.image.load("tiles/grass_wood.png"),
        3 : pg.image.load("tiles/water.png"),
    },
    
    "tile_size" : 64,

    "objects" : [
        player
    ],

    "hostiles" : [
        obj.Enemy("characters/player_1.png", 500, 500, player, 5, 20, 5)
    ],

    "items" : [
        obj.DroppedItem(pg.image.load("items/sword.png"), 600, 600, player, obj.ItemEntity(pg.image.load("items/sword.png"), "ва", type="weapon", id=1, damage=5,)),
        obj.DroppedItem(pg.image.load("items/bow.png"), 700, 600, player, obj.ItemEntity(pg.image.load("items/bow.png"), "ва", type="weapon", id=1, damage=3)),
        obj.DroppedItem(pg.image.load("items/musket.png"), 600, 600, player, obj.ItemEntity(pg.image.load("items/musket.png"), "ва", type="weapon", id=1, damage=15, attack_distance=1000))
    ],

    "mining" : [
        
    ]
}

map_2_config = {
    "tiles" : [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],

    "tile_images" : {
        0 : pg.image.load("tiles/grass.png"),
        1 : pg.image.load("tiles/wood.png"),
    },
    
    "tile_size" : 64,

    "objects" : [
        player,
    ],

    "hostiles" : [
        
    ],

    "items" : [
        
    ],
    
    "mining" : [
        
    ]
}


map_1 = obj.Map(map_1_config, player)
map_2 = obj.Map(map_2_config, player)
game = obj.Game(fps = 60, map = map_1)

play = True
while play:
    key = pg.key.get_pressed()

    game.if_exit(play)

    game.draw_map()

    interface.draw(game.screen, player)
    inventory.draw(game.screen, player, map_1_config)

    game.completion()