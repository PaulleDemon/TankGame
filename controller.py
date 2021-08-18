import assets
from Tank import Bullet, Enemy
from random import choice


class Controller:

    bullets = set()
    enemies = set()
    player = None
    screen = None
    obstacles = set()
    bg_x, bg_y = (0, 0) # background position

    def __init__(self, screen, spawn_pos: list):
        self.screen = screen
        self.spwan_lst = spawn_pos

    def setPlayer(self, tank):
        self.player = tank

    def setBgPos(self, bgpos):
        self.bg_x, self.bg_y = bgpos

    def addObstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def createBullet(self, tank_object, normal_pos, fire_pos, angle, radius, speed):
        bullet = Bullet(self.screen, tank_object, normal_pos, fire_pos, angle, radius, speed)
        self.bullets.add(bullet)

    def getPlayerPos(self):
        return self.player.pos()

    def updateTanks(self):
        self.player.update()
        for tank in self.enemies:
            tank.setBgPos((self.bg_x, self.bg_y))
            tank.update()

    def updateObstacles(self):
        for obs, _ in self.obstacles:
            obs.update((self.bg_x, self.bg_y))

    def checkCollision(self):
        """ checks for collision between tank, bullets and obstacles """
        for bullet in self.bullets.copy():
            for _, collid in self.obstacles:
                if collid.rect_collide(bullet.getBbox())[0]:
                    self.bullets.remove(bullet)
                    break

        if any(bullet.colliderect(self.player.getRectObject()) for bullet in self.bullets if bullet.tankObject()
                                                                                             != self.player):
            print("HIT")

        for tank in self.enemies.copy():
            for bullet in self.bullets.copy():
                if tank != bullet.tankObject() and tank.colliderect(bullet.getRect()):
                    self.enemies.remove(tank)
                    self.bullets.remove(bullet)
                    break

    def update_bullets(self):

        for bullet in self.bullets.copy():
            bullet.update()

            if bullet.destroyed():
                self.bullets.remove(bullet)

    def updatePlayers(self):

        self.checkCollision()
        self.update_bullets()
        self.updateTanks()

    def spawnEnemy(self):

        pos = choice(self.spwan_lst)
        print(pos)
        enemy = Enemy(follow_radius=250, fire_radius=100, pos=pos,
                      screen=self.screen, img_path=assets.ENEMY_TANK, controller=self) # todo: from here
        self.enemies.add(enemy)