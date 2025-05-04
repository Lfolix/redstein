import pygame as pg
import objects as obj
import time

pg.init()

slots = [
    (280, 260),
    (400, 260),
    (280, 400),
    (400, 400),
]

current_slots = [
    (60, 290),
    (60, 410)
]

slots_interface = [
    (0, 0),
    (64, 0)
]

open = False

sur_slot = -1
sur_slot_cur = -1

image = pg.image.load("modules/inventory/inventory_image.png")
image_interface = pg.image.load("modules/inventory/current_slots.png")

properties = pg.image.load("modules/inventory/properties.png")

def draw(screen, player, map):
    global open
    global sur_slot

    key = pg.key.get_pressed()
    mouse_key = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    if key[pg.K_i]:
        if not open:
            open = True
            time.sleep(0.2)
        else:
            open = False
            time.sleep(0.2)

    if open:
        screen.fill((0, 0, 0))

        sur_slot = -1
        screen.blit(image, (0, 0))

        for i in player.inventory:
            sur_slot += 1

            if sur_slot >= len(slots):
                sur_slot = -1

            i.draw(screen, slots[sur_slot])


            if i.rect.collidepoint(mouse_pos):
                if key[pg.K_e]:
                    if len(player.current_inventory) - 1 < len(current_slots) - 1:
                        if i.type != "eat":
                            time.sleep(0.3)
                            player.current_inventory.append(i)
                            player.inventory.remove(i)

                if key[pg.K_r]:
                    time.sleep(0.3)
                    map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 100, player, i))
                    player.inventory.remove(i)

                if key[pg.K_t]:
                    if i.type == "eat":
                        if player.hunger < 50:
                            time.sleep(0.3)
                            player.hunger += i.hunger
                            player.inventory.remove(i)


        for i in player.current_inventory:
            sur_slot += 1

            if sur_slot >= len(current_slots) - 1:
                sur_slot = -1

            print(sur_slot)

            i.draw(screen, current_slots[sur_slot])


            if i.rect.collidepoint(mouse_pos):
                if key[pg.K_e]:
                    if len(player.inventory) - 1 < len(slots) - 1:
                        if i.type != "eat":
                            time.sleep(0.3)
                            player.inventory.append(i)
                            player.current_inventory.remove(i)

                if key[pg.K_r]:
                    time.sleep(0.3)
                    map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 100, player, i))
                    player.current_inventory.remove(i)