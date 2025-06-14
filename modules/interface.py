import pygame as pg


pg.init()

font = pg.font.Font(None, 45)
font2 = pg.font.Font(None, 70)

timer_death = 0

def draw(screen, player):
    global timer_death
    screen.blit(font.render(f"Health : {player.health}",  True, ("Red")), (0, 0))
    screen.blit(font.render(f"Hunger : {player.hunger}",  True, ("Red")), (0, 50))
    screen.blit(font.render(f"Damage : {player.damage}",  True, ("Red")), (0, 100))
    screen.blit(font.render(f"inventory : {player.current_inventory}",  True, ("Red")), (0, 150))

    if player.health <= 0:
        timer_death += 1
        screen.blit(font.render(str("YOU ARE DEAD"),  True, ("Red")), (570, 0))

        if timer_death >= 10:
            screen.blit(font.render(str("Press enter to restart"),  True, ("Red")), (540, 80))
        if timer_death == 20:
            timer_death = 0