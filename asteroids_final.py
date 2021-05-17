"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 2
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 20

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 8

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 5

BIG_ASTEROID_IMG = "images/meteorGrey_big2.png"
MEDIUM_ASTEROID_IMG = "images/meteorGrey_med2.png"
SMALL_ASTEROID_IMG = "images/meteorGrey_small2.png"
SHIP_IMG = "images/playerShip1_orange.png"
BULLET_IMG = "images/laserBlue01.png"
EXPLOSION_IMG = "images/explosion.png"
BACKGROUND_IMG = "images/background.png"
GAME_OVER_IMG = "images/gameover.png"

SHIP_SHOOTING_SOUND = arcade.load_sound("images/shoot.wav")
GAME_OVER_SOUND = arcade.load_sound("images/game_over.wav")


class Point:
    def __init__(self):
        self._x = 0.0
        self._y = 0.0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Velocity:
    def __init__(self):
        self._dx = 0.0
        self._dy = 0.0

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, value):
        self._dx = value

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, value):
        self._dy = value

class Base():
    def __init__(self):
        self._center = Point()
        self._velocity = Velocity()
        self._radius = 0.0
        self._alive = True
        self._angle = 0.0
        self._hit = 0
        self._image = ""

    def advance(self):
        self._center.x += self._velocity.dx
        self._center.y += self._velocity.dy

    def is_off_screen(self, scn_width=SCREEN_WIDTH, scn_height=SCREEN_HEIGHT):
        if self._center.x < 0:
            self._center.x = scn_width
        if self._center.x > scn_width:
            self._center.x = 0
        if self._center.y > scn_height:
            self._center.y = 0
        if self._center.y < 0:
            self._center.y = scn_height

    def draw(self):
        texture = arcade.load_texture(self._image)

        width = texture.width
        height = texture.height
        alpha = 255  # For transparency, 1 means transparent

        x = self._center.x
        y = self._center.y
        angle = self._angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def check_hit(self):
        self._hit -= 1
        self._alive = False
        return 1

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, x, y):
        self._center.x = x
        self._center.y = y

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, x, y):
        self._velocity.dx = x
        self._velocity.dy = y

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

class Asteroid(Base):
    def __init__(self):
        super().__init__()
        self._center.x = random.uniform(0, SCREEN_WIDTH)
        self._center.y = random.uniform(0, SCREEN_HEIGHT)
        self._velocity.dx = random.random() * BIG_ROCK_SPEED - 1
        self._velocity.dy = random.random() * BIG_ROCK_SPEED - 1

class Big_Asteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self._image = BIG_ASTEROID_IMG
        self._radius = BIG_ROCK_RADIUS

    def advance(self):
        super().advance()
        self._angle += BIG_ROCK_SPIN

    def check_hit(self):
        super().check_hit()
    
class Medium_Asteroid(Asteroid):
    def __init__(self, x, y, dy):
        super().__init__()
        self._center.x = x
        self._center.y = y
        self._velocity.dy = dy
        self._radius = MEDIUM_ROCK_RADIUS
        self._image = MEDIUM_ASTEROID_IMG

    def advance(self):
        super().advance()
        self._angle += MEDIUM_ROCK_SPIN

class Small_Asteroid(Asteroid):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self._center.x = x
        self._center.y = y
        self._velocity.dx = dx
        self._velocity.dy = dy
        self._radius = SMALL_ROCK_RADIUS
        self._image = SMALL_ASTEROID_IMG

    def advance(self):
        super().advance()
        self._angle += SMALL_ROCK_SPIN

class Ship(Base):
    def __init__(self):
        super().__init__()
        self._center.x = SCREEN_WIDTH // 2
        self._center.y = SCREEN_HEIGHT // 2
        self._radius = SHIP_RADIUS
        self._image = SHIP_IMG
        self.explosion = EXPLOSION_IMG
        
    def ship_move(self, angle):
        self._velocity.dx = math.cos(math.radians(angle)) * SHIP_THRUST_AMOUNT
        self._velocity.dy = math.sin(math.radians(angle)) * SHIP_THRUST_AMOUNT
        
        if self.velocity.dx >= SCREEN_WIDTH:
            self.velocity.dx = SCREEN_WIDTH
        elif self.velocity.dy >= SCREEN_HEIGHT:
            self.velocity.dy = SCREEN_HEIGHT
    
    def advance(self):
        super().advance()
        
        if self.center.x >= SCREEN_WIDTH - 20:
            self.center.x = SCREEN_WIDTH - 20
        elif self.center.y >= SCREEN_HEIGHT - 20:
            self.center.y = SCREEN_HEIGHT - 20
        elif self.center.x <= 0 + 20:
            self.center.x = 0 + 20
        elif self.center.y <= 0 + 20:
            self.center.y = 0 + 20 
    
    def game_over(self):
        texture = arcade.load_texture(self.explosion)
        gameover = arcade.load_texture(GAME_OVER_IMG)

        width = texture.width
        height = texture.height
        alpha = 255 # For transparency, 1 means transparent 

        x = self.center.x
        y = self.center.y
        game_x = x
        game_y = y

        #Hip Explosion
        arcade.draw_texture_rectangle(x, y, width, height, texture, 0, alpha)
        
        #Game Over Image
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT //2, width, height, gameover, 0, alpha)

class Bullet(Base):
    def __init__(self, x, y, ship_angle):
        self._count = 0
        super().__init__()
        self._center.x = x
        self._center.y = y
        self._radius = BULLET_RADIUS
        self._velocity.dx = BULLET_SPEED
        self._velocity.dy = BULLET_SPEED
        self._angle = ship_angle
        self._image = BULLET_IMG

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def fire(self, angle):
        self._velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self._velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        self.background = arcade.load_texture(BACKGROUND_IMG)
              
        self.held_keys = set()
        self.asteroid_count = INITIAL_ROCK_COUNT

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()

        self.bullets_list = []
        self.asteroid_list = []

        for asteroid in range(INITIAL_ROCK_COUNT):
            asteroid = Big_Asteroid()
            self.asteroid_list.append(asteroid)
            
        # Sounds
        self.hit_sound = arcade.load_sound(":resources:sounds/explosion1.wav")  
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        
        # clear the screen to begin drawing
        arcade.start_render()
        
        arcade.draw_texture_rectangle(400, 300, SCREEN_WIDTH, SCREEN_HEIGHT, self.background, 0, 255)

        # TODO: draw each object
        for asteroid in self.asteroid_list:
            asteroid.draw()

        for bullet in self.bullets_list:
            bullet.draw()

        if self.ship.alive == True:
            self.ship.draw()
        else:
            self.ship.game_over()                         

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """         
        self.check_collisions()
        self.check_keys() 

        # TODO: Tell everything to advance or move forward one step in time
        for asteroid in self.asteroid_list:
            asteroid.advance()
            asteroid.is_off_screen()

        for bullet in self.bullets_list:
            bullet.advance()
            bullet.count += 1

            if bullet.count == 60:
                bullet.alive = False

        if self.ship.alive:
            self.ship.advance()
        
        """for asteroid in self.asteroid_list:
            if len(self.asteroid_list) == 3:          
                for asteroid in range(INITIAL_ROCK_COUNT + 2):
                    asteroid = Big_Asteroid()
                    self.asteroid_list.append(asteroid)"""            

    def create_asteroid(self, asteroid):
        medium_rock_speed = BIG_ROCK_SPEED
        small_rock_speed = BIG_ROCK_SPEED
        
        count = 0

        if isinstance(asteroid, Big_Asteroid):
            for i in range(2):
                if count == 0:
                    i = Medium_Asteroid(asteroid.center.x, asteroid.center.y, medium_rock_speed + 2 )
                    count += 1
                else:
                    i = Medium_Asteroid(asteroid.center.x, asteroid.center.y, (medium_rock_speed + 2) * -1)

                self.asteroid_list.append(i)

            new_asteroid = Small_Asteroid(
                asteroid.center.x, asteroid.center.y, small_rock_speed + 1.5  , asteroid.velocity.dy)
            self.asteroid_list.append(new_asteroid)

        elif isinstance(asteroid, Medium_Asteroid):
            for i in range(2):
                if count == 0:
                    i = Small_Asteroid(asteroid.center.x, asteroid.center.y,
                                                  small_rock_speed + 2, small_rock_speed + 2)
                    count += 1
                else:
                    i = Small_Asteroid(asteroid.center.x, asteroid.center.y,
                                                  (small_rock_speed + 2) * -1, (small_rock_speed + 2 ) * -1)

                self.asteroid_list.append(i)    

    def check_collisions(self):
        """
       Checks to see if bullets have hit targets.
       Updates scores and removes dead items.
       :return:
       """
       # NOTE: This assumes you named your targets list "targets"
        for asteroid in self.asteroid_list:
            if asteroid.alive and self.ship.alive:
                asteroid_too_close = asteroid.radius + self.ship.radius

                if (abs(asteroid.center.x - self.ship.center.x) < asteroid_too_close and abs(asteroid.center.y - self.ship.center.y) < asteroid_too_close):
                    self.ship.alive = False
                    arcade.play_sound(GAME_OVER_SOUND)

        for bullet in self.bullets_list:

            if bullet.alive and self.ship.alive:
                bullet_too_close = bullet.radius + self.ship.radius

                if (abs(bullet.center.x - self.ship.center.x) < bullet_too_close and
                        abs(bullet.center.y - self.ship.center.y) < bullet_too_close) and bullet.count > 30:
                    self.ship.alive = False

            for asteroid in self.asteroid_list:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                            abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        asteroid.check_hit()

                        self.create_asteroid(asteroid)
                        arcade.play_sound(self.hit_sound)

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

       # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

       
    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets_list:
            if not bullet.alive:
                self.bullets_list.remove(bullet)
                
        for asteroid in self.asteroid_list:
            if not asteroid.alive:
                self.asteroid_list.remove(asteroid)
                
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += SHIP_TURN_AMOUNT

        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= SHIP_TURN_AMOUNT

        if arcade.key.UP in self.held_keys:
            self.ship.ship_move(self.ship.angle + 90)

        if arcade.key.DOWN in self.held_keys:
            self.ship.ship_move(self.ship.angle - 90)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!

                bullet = Bullet(self.ship.center.x, self.ship.center.y, self.ship.angle + 90)
                bullet.fire(self.ship.angle + 90)

                self.bullets_list.append(bullet)
                arcade.play_sound(SHIP_SHOOTING_SOUND)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key) 

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
