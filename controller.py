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
    prev_bg_x, prev_bg_y = (0, 0) # previous background position

    def __init__(self, screen, spawn_pos: list):
        self.screen = screen
        self.spwan_lst = spawn_pos

    def setPlayer(self, tank):
        self.player = tank

    def setBgPos(self, bgpos, prev_pos):
        self.bg_x, self.bg_y = bgpos
        self.prev_bg_x, self.prev_bg_y = prev_pos

    def addObstacle(self, obstacle, collidObj):
        self.obstacles.add((obstacle, collidObj))

    def createBullet(self, tank_object, normal_pos, fire_pos, angle, radius, speed):
        bullet = Bullet(self.screen, tank_object, normal_pos, fire_pos, angle, radius, speed)
        self.bullets.add(bullet)

    def getPlayerPos(self):
        return self.player.pos()

    def setBgPosChanged(self, changed: bool):
        self.bg_pos_changed = changed

    def updateTanks(self):
        self.player.update()

        bg_x, bg_y = self.bg_x - self.prev_bg_x, self.bg_y - self.prev_bg_y

        for tank in self.enemies:

            tank.setBgPos((bg_x, bg_y))
            tank.update(self.player.center())

    def updateObstacles(self):
        for obs, _ in self.obstacles:
            obs.update((self.bg_x, self.bg_y))

    def update_bullets(self):

        bg_x, bg_y = self.bg_x - self.prev_bg_x, self.bg_y - self.prev_bg_y

        for bullet in self.bullets.copy():
            bullet.update((bg_x, bg_y))

            if bullet.destroyed():
                self.bullets.remove(bullet)

    def checkCollision(self):
        """ checks for collision between tank, bullets and obstacles """
        for bullet in self.bullets.copy():
            for _, collid in self.obstacles:
                if collid.rect_collide(bullet.getBbox())[0]:
                    self.bullets.remove(bullet)
                    break

        for enemy in self.enemies:
            for _, collid in self.obstacles:
                if collid.rect_collide(enemy.getBbox())[0]:
                    enemy.change_angle()

            if self.player.colliderect(enemy.getRectObject()):
                self.player.resetPreviousPos()
                enemy.resetPreviousPos()

        for bullet in self.bullets.copy():
            for tank in self.enemies.copy():
                if tank != bullet.tankObject() and tank.colliderect(bullet.getRect()):
                    self.enemies.remove(tank)
                    self.bullets.remove(bullet)
                    break

            if bullet.tankObject() != self.player and self.player.colliderect(bullet.getRect()):
                self.bullets.remove(bullet)
                print("HIT")

    def update(self):
        self.update_bullets()
        self.updateTanks()
        self.updateObstacles()
        self.checkCollision()

    def spawnEnemy(self):

        pos = choice(self.spwan_lst)
        print(pos)
        enemy = Enemy(follow_radius=550, pos=pos, screen=self.screen, img_path=assets.ENEMY_TANK,
                      controller=self, speed=self.player.speed/2, fire_speed=self.player.fire_speed) # todo: from here
        self.enemies.add(enemy)