import pygame as pg
import objects as obj
import time


slots = [
    (280, 260),
    (64, 64)
]

current_slots = [
    (60, 290),
    (60, 410)
]

slots_interface = [
    (0, 0),
    (64, 64)
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

    if key[pg.K_i]:
        if not open:  # Если инвентарь закрыт, открываем его
            open = True
            time.sleep(0.2)  # Задержка для предотвращения многократных нажатий
        else:  # Если инвентарь открыт, закрываем его
            open = False
            time.sleep(0.2)

    if open:
        # Очистка экрана (или рисование фона)
        screen.fill((0, 0, 0))  # Заполните экран черным цветом или используйте другой фон

        print("slot:", sur_slot)

        # Отрисовка фона инвентаря
        screen.blit(image, (0, 0))

        sur_slot = -1
        sur_slot_cur = -1

        if len(player.inventory) >= 1:
            for i in player.inventory:
                sur_slot += 1
                i.draw(screen, slots[sur_slot])  # Передаем screen, а не image

                # Проверка, находится ли мышь над предметом
                if i.rect.collidepoint(pg.mouse.get_pos()):
                    screen.blit(properties, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
                    if pg.mouse.get_pressed()[2]:  # Если нажата левая кнопка мыши
                        deleted_item = i
                        player.inventory.remove(deleted_item)
                        map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 125, player, i))

                    if pg.mouse.get_pressed()[0]:  # Если нажата левая кнопка мыши
                        removed_item = i
                        player.inventory.remove(removed_item)
                        player.current_inventory.append(i)

        if len(player.current_inventory) >= 1:
            for i in player.current_inventory:
                sur_slot_cur += 1
                i.draw(screen, current_slots[sur_slot_cur])  # Передаем screen, а не image

                # Проверка, находится ли мышь над предметом
                if i.rect.collidepoint(pg.mouse.get_pos()):
                    screen.blit(properties, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
                    if pg.mouse.get_pressed()[2]:  # Если нажата левая кнопка мыши
                        deleted_item = i
                        player.current_inventory.remove(deleted_item)
                        map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 125, player, i))

                    if pg.mouse.get_pressed()[0]:  # Если нажата левая кнопка мыши
                        removed_item = i
                        player.current_inventory.remove(removed_item)
                        player.inventory.append(removed_item)

        # Проверка на выход за пределы слотов
        if sur_slot >= len(slots):
            sur_slot = -1

        if sur_slot_cur >= len(current_slots):
            sur_slot = -1

                # Отрисовка фона инвентаря

    if not open:
        screen.blit(image_interface, (0, 0))

        sur_slot = -1

        if len(player.current_inventory) >= 1:
            for i in player.current_inventory:
                sur_slot += 1
                i.draw(screen, slots_interface[sur_slot])  # Передаем screen, а не image

                # Проверка, находится ли мышь над предметом
                if i.rect.collidepoint(pg.mouse.get_pos()):
                    screen.blit(properties, (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
                    if pg.mouse.get_pressed()[2]:  # Если нажата левая кнопка мыши
                        deleted_item = i
                        player.current_inventory.remove(deleted_item)
                        map["items"].append(obj.DroppedItem(i.image, player.x, player.y + 125, player, i))

        # Проверка на выход за пределы слотов
        if sur_slot >= len(slots_interface):
            sur_slot = -1

