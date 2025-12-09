from constants import *
from obstacle import Platform, ShadowZone, Hazard, FormBarrier, MovingPlatform
from collectibles import LightOrb, Portal
from enemies import Bug, Ant, Firefly_Enemy


class Level:
    def __init__(self, level_id, level_type="side_scroll"):
        self.level_id = level_id
        self.level_type = level_type
        self.width = 3000
        self.platforms = []
        self.moving_platforms = []
        self.shadow_zones = []
        self.hazards = []
        self.light_orbs = []
        self.form_barriers = []
        self.enemies = []
        self.finish_x = self.width - 200
        self.portal = Portal(self.finish_x)

    def get_finish_rect(self):
        return pygame.Rect(self.finish_x, 0, 100, GROUND_LEVEL)


class LevelManager:
    def __init__(self):
        self.current_level_id = 1
        self.current_level = None
        self.load_level(1)

    def load_level(self, level_id):
        self.current_level_id = level_id

        if level_id == 1:
            self.current_level = self.create_level_1()
        elif level_id == 2:
            self.current_level = self.create_level_2()
        elif level_id == 3:
            self.current_level = self.create_level_3()
        elif level_id == 4:
            self.current_level = self.create_level_4()
        else:
            self.current_level = self.create_level_1()

        return self.current_level

    def create_level_1(self):
        # level 1
        level = Level(1, "side_scroll")

        # platforms
        level.platforms = [
            Platform(300, 550, 200, 20, "light"),
            Platform(600, 480, 150, 20, "normal"),
            Platform(900, 420, 180, 20, "light"),
            Platform(1200, 350, 150, 20, "shadow"),
            Platform(1500, 450, 200, 20, "normal"),
            Platform(1800, 380, 150, 20, "light"),
            Platform(2100, 300, 180, 20, "shadow"),
            Platform(2400, 400, 150, 20, "normal"),
        ]

        # shadow zones - forces shadow form
        level.shadow_zones = [
            ShadowZone(1150, 200, 200, 450),
            ShadowZone(2050, 150, 250, 500),
        ]

        # form barriers
        level.form_barriers = [
            FormBarrier(750, 350, 30, 250, "light"),
            FormBarrier(1050, 250, 30, 400, "shadow"),
            FormBarrier(1700, 280, 30, 370, "light"),
            FormBarrier(2300, 300, 30, 350, "shadow"),
        ]

        # light orbs
        level.light_orbs = [
            LightOrb(400, 500),
            LightOrb(700, 430),
            LightOrb(1000, 370),
            LightOrb(1300, 300),
            LightOrb(1600, 400),
            LightOrb(1900, 330),
            LightOrb(2200, 250),
            LightOrb(2500, 350),
        ]

        # hazards
        level.hazards = [
            Hazard(550, GROUND_LEVEL - 30),
            Hazard(580, GROUND_LEVEL - 30),
            Hazard(1450, GROUND_LEVEL - 30),
            Hazard(1480, GROUND_LEVEL - 30),
            Hazard(2250, GROUND_LEVEL - 30),
        ]

        return level

    def create_level_2(self):
        # level 2
        level = Level(2, "side_scroll")
        level.width = 3500  # mai lung!
        level.finish_x = level.width - 200
        level.portal = Portal(level.finish_x)

        # platforms
        level.platforms = [
            Platform(250, 580, 150, 20, "light"),
            Platform(500, 500, 120, 20, "shadow"),
            Platform(750, 420, 140, 20, "light"),
            Platform(1000, 360, 120, 20, "shadow"),
            Platform(1300, 450, 150, 20, "normal"),
            Platform(1600, 350, 130, 20, "light"),
            Platform(1900, 280, 140, 20, "shadow"),
            Platform(2200, 380, 150, 20, "light"),
            Platform(2500, 300, 120, 20, "shadow"),
            Platform(2800, 420, 150, 20, "normal"),
            Platform(3100, 340, 150, 20, "light"),
        ]

        # shadow zones
        level.shadow_zones = [
            ShadowZone(500, 350, 200, 300),
            ShadowZone(1250, 200, 300, 450),
            ShadowZone(2000, 150, 300, 500),
            ShadowZone(2850, 250, 350, 400),
        ]

        # form barriers
        level.form_barriers = [
            FormBarrier(380, 480, 30, 170, "light"),  # before shadow zone
            FormBarrier(800, 320, 30, 330, "shadow"),  # between platforms
            FormBarrier(1150, 260, 30, 390, "light"),
            FormBarrier(1750, 180, 30, 470, "shadow"),
            FormBarrier(2350, 280, 30, 370, "light"),
            FormBarrier(3050, 240, 30, 410, "shadow"),
        ]

        # light orbs
        level.light_orbs = [
            LightOrb(350, 530),
            LightOrb(600, 450),
            LightOrb(850, 370),
            LightOrb(1100, 310),
            LightOrb(1400, 400),
            LightOrb(1700, 300),
            LightOrb(2000, 230),
            LightOrb(2300, 330),
            LightOrb(2600, 250),
            LightOrb(2900, 370),
            LightOrb(3200, 290),
        ]

        # hazards
        level.hazards = [
            Hazard(450, GROUND_LEVEL - 30),
            Hazard(480, GROUND_LEVEL - 30),
            Hazard(510, GROUND_LEVEL - 30),
            Hazard(1200, GROUND_LEVEL - 30),
            Hazard(1230, GROUND_LEVEL - 30),
            Hazard(2000, GROUND_LEVEL - 30),
            Hazard(2030, GROUND_LEVEL - 30),
            Hazard(2650, GROUND_LEVEL - 30),
            Hazard(2680, GROUND_LEVEL - 30),
            Hazard(2710, GROUND_LEVEL - 30),
        ]

        return level

    def create_level_3(self):
        # level 3
        level = Level(3, "forward")
        level.width = 2800
        level.finish_x = level.width - 200
        level.portal = Portal(level.finish_x)

        # platforms
        level.platforms = [
            Platform(400, 520, 220, 25, "light"),
            Platform(750, 470, 200, 25, "shadow"),
            Platform(1100, 420, 220, 25, "light"),
            Platform(1450, 370, 200, 25, "shadow"),
            Platform(1800, 320, 220, 25, "light"),
            Platform(2150, 270, 200, 25, "shadow"),
        ]

        # shadow zones
        level.shadow_zones = [
            ShadowZone(650, 320, 500, 330),
            ShadowZone(1350, 220, 550, 430),
            ShadowZone(2050, 170, 500, 480),
        ]

        # form barriers
        level.form_barriers = [
            FormBarrier(620, 420, 30, 230, "light"),
            FormBarrier(950, 370, 30, 280, "shadow"),
            FormBarrier(1320, 320, 30, 330, "light"),
            FormBarrier(1650, 270, 30, 380, "shadow"),
            FormBarrier(2000, 220, 30, 430, "light"),
        ]

        # light orbs
        level.light_orbs = [
            LightOrb(500, 470),
            LightOrb(850, 420),
            LightOrb(1200, 370),
            LightOrb(1550, 320),
            LightOrb(1900, 270),
            LightOrb(2250, 220),
        ]

        # hazards
        level.hazards = [
            Hazard(700, GROUND_LEVEL - 30),
            Hazard(730, GROUND_LEVEL - 30),
            Hazard(1400, GROUND_LEVEL - 30),
            Hazard(1430, GROUND_LEVEL - 30),
            Hazard(2100, GROUND_LEVEL - 30),
            Hazard(2130, GROUND_LEVEL - 30),
        ]

        # enemies
        level.enemies = [
            Bug(1000, GROUND_LEVEL - 30, 150, 2),
            Ant(1500, GROUND_LEVEL - 20, 180, 2.5),
            Firefly_Enemy(1200, 250, 100, 1.5),
            Bug(2300, GROUND_LEVEL - 30, 200, 1.8),
            Ant(2800, GROUND_LEVEL - 20, 150, 3),
        ]

        return level

    def create_level_4(self):
        # level 4
        level = Level(4, "forward")
        level.width = 4000
        level.finish_x = level.width - 150
        level.portal = Portal(level.finish_x)

        # platforms
        level.platforms = [
            Platform(400, 580, 250, 25, "light"),
            Platform(900, 520, 200, 25, "shadow"),
            Platform(1400, 470, 220, 25, "light"),
            Platform(1900, 420, 180, 25, "shadow"),
            Platform(2400, 380, 200, 25, "light"),
            Platform(2900, 340, 180, 25, "shadow"),
            Platform(3400, 300, 200, 25, "light"),
        ]

        # moving platforms - up-down
        level.moving_platforms = [
            MovingPlatform(700, 450, 150, 20, "normal", "vertical", 120, 3),
            MovingPlatform(1200, 380, 140, 20, "light", "vertical", 100, 2),
            MovingPlatform(1700, 320, 130, 20, "shadow", "vertical", 140, 4),
            MovingPlatform(2200, 280, 150, 20, "normal", "vertical", 110, 3),
            MovingPlatform(2700, 240, 140, 20, "light", "vertical", 130, 2),
            MovingPlatform(3200, 200, 150, 20, "shadow", "vertical", 100, 3),
        ]

        # shadow zones
        level.shadow_zones = [
            ShadowZone(850, 300, 400, 350),
            ShadowZone(1850, 250, 450, 400),
            ShadowZone(2850, 200, 500, 450),
        ]

        # form barriers
        level.form_barriers = [
            FormBarrier(650, 480, 30, 170, "light"),
            FormBarrier(1150, 370, 30, 280, "shadow"),
            FormBarrier(1650, 320, 30, 330, "light"),
            FormBarrier(2150, 280, 30, 370, "shadow"),
            FormBarrier(2650, 240, 30, 410, "light"),
            FormBarrier(3150, 200, 30, 450, "shadow"),
        ]

        # light orbs
        level.light_orbs = [
            LightOrb(500, 530),
            LightOrb(800, 400),
            LightOrb(1000, 470),
            LightOrb(1300, 420),
            LightOrb(1500, 420),
            LightOrb(1800, 370),
            LightOrb(2000, 370),
            LightOrb(2300, 330),
            LightOrb(2500, 330),
            LightOrb(2800, 290),
            LightOrb(3000, 290),
            LightOrb(3300, 250),
            LightOrb(3500, 250),
        ]

        # hazards
        level.hazards = [
            Hazard(600, GROUND_LEVEL - 30),
            Hazard(630, GROUND_LEVEL - 30),
            Hazard(1350, GROUND_LEVEL - 30),
            Hazard(1380, GROUND_LEVEL - 30),
            Hazard(1850, GROUND_LEVEL - 30),
            Hazard(1880, GROUND_LEVEL - 30),
            Hazard(2350, GROUND_LEVEL - 30),
            Hazard(2380, GROUND_LEVEL - 30),
            Hazard(2850, GROUND_LEVEL - 30),
            Hazard(2880, GROUND_LEVEL - 30),
            Hazard(3350, GROUND_LEVEL - 30),
            Hazard(3380, GROUND_LEVEL - 30),
        ]

        # enemies
        level.enemies = [
            Bug(800, GROUND_LEVEL - 30, 180, 2),
            Ant(1300, GROUND_LEVEL - 20, 200, 2.5),
            Firefly_Enemy(1100, 300, 120, 1.5),
            Bug(1900, GROUND_LEVEL - 30, 150, 2),
            Firefly_Enemy(2200, 250, 100, 1.8),
            Ant(2700, GROUND_LEVEL - 20, 180, 2.5),
            Bug(3200, GROUND_LEVEL - 30, 200, 2),
        ]

        return level

    def next_level(self):
        # go to the next level
        next_id = self.current_level_id + 1
        if next_id <= 4:
            return self.load_level(next_id)
        return None