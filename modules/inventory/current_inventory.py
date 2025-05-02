import pygame as pg
import objects as obj
import time
import inventory


slots = [
    (0, 0),
    (64, 64)
]

open = False

sur_slot = -1
sur_slot_cur = -1

image = pg.image.load("modules/inventory/current_slots.png")

properties = pg.image.load("modules/inventory/properties.png")

def draw(screen, player, map):
    global open
    global sur_slot

        # Отрисовка фона инвентаря
    screen.blit(image, (0, 0))

    sur_slot = -1

    if len(player.current_inventory) >= 1:
        for i in player.current_inventory:
            sur_slot += 1
            i.draw(screen, slots[sur_slot])  # Передаем screen, а не image

            # Проверка, находится ли мышь над предметом
            if i.rect.collidepoint(pg.mouse.get_pos()):
                screen.blit(properties, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
                if pg.mouse.get_pressed()[2]:  # Если нажата левая кнопка мыши
                    deleted_item = i
                    player.current_inventory.remove(deleted_item)
                    map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 125, player, i))

    # Проверка на выход за пределы слотов
    if sur_slot >= len(slots):
        sur_slot = -1
