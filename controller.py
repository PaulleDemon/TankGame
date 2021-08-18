from Tank import Bullet, Enemy


class Controller:

    bullets = set()
    enemies = set()
    player = None
    screen = None
    obstacles = set()

    def __init__(self, screen):
        self.screen = screen

    def setPlayer(self, tank):
        self.player = tank

    def addObstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def createBullet(self, tank_object, normal_pos, fire_pos, angle, radius, speed):
        bullet = Bullet(self.screen, tank_object, normal_pos, fire_pos, angle, radius, speed)
        self.bullets.add(bullet)

    def updateTanks(self):
        self.player.update()
        for tank in self.enemies:
            tank.update()

    def updateObstacles(self, pos):
        for obs, _ in self.obstacles:
            obs.update(pos)

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
        enemy = Enemy() # todo: from here
        self.enemies.add(enemy)