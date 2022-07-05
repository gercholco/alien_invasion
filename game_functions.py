import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def check_events (ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type ==pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type ==pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):     
    if event.key == pygame.K_RIGHT:
    #Move the ship to the right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

"""Respond to keypresses"""
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
    #Move the ship to the right
        ship.rect.centerx += 1
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """fire a bullet if limit not reached yet"""
    #create a new bullet and add it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """update position of bullets and get rid of old bullets"""
    #update bullet position
    bullets.update()

        #get rid of bullets that have disappeared
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """respond to alien-bullet collisions"""
    #remove any bullets and aliens that have colided
    #check for any bullets that have hit aliens
    #if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        #destroy existing bullets and create new fleet.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
    

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen"""
    #Redraw the screen during each pass throught the loop
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    pygame.display.flip()

def get_number_aliens_x(ai_settings, alien_width):
    """determinate the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of aliens that fit on the screen"""
    avaiable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaiable_space_y / (2 * alien_height))
    return number_rows

def create_alien (ai_settings, screen, aliens, alien_number, row_number):
    """create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """create a full fleet of aliens"""
    #create an alien and find the number of aleins in a row
    alien=Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #spacing between each alien is equal to one alien width
    #create the fleet of aleins
    for row_number in range(number_rows):
        #create trhe first row of aliens
        for alien_number in range(number_aliens_x):
        #create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """respond properly if any alienshave reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """respond to ship being hit by alien"""
    #decrement ships_left
    stats.ships_left -= 1

    #empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    #create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    #pause.
    sleep(0.5)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """check if the fleet is at an edge, and then update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    #Make the most recently drawn screen visible
    pygame.display.flip()