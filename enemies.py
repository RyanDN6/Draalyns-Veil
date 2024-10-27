import weapons
class Enemy:
    def __init__(self, type, name, power=1, areas=None, ally=False, boss=False, attack=0, defence=0, hitpoints=0, agility=10, sp=20, spRecovery=0, weapon="Fists", experiencePoints=0, gold=0, defend=False, stunned=False, poisoned=0, bleeding=False):
        self.type = type
        self.name = name
        if areas == None:
            self.areas = []
        else:
            self.areas = areas
        self.power = power
        self.ally = ally
        self.boss = boss
        self.attack = attack
        self.hitpoints = hitpoints
        self.maxHitpoints = hitpoints
        self.weapon = weapons.weaponsList[weapon]
        self.sp = sp
        self.maxSp = self.sp
        self.spRecovery = spRecovery
        self.agility = agility
        self.experiencePoints = experiencePoints
        self.gold = gold
        self.defend = defend
        self.stunned = stunned
        self.poisoned = poisoned
        self.bleeding = bleeding
        self.defence = defence

class Slime(Enemy):
    def __init__(self):
        super().__init__(type="Slime", name="Slime", areas=[".", "%", "^"], power=1, attack=0, defence=0, hitpoints=10, agility=10, experiencePoints=2, gold=3)

class Dragonfly(Enemy):
    def __init__(self):
        super().__init__(type="Dragonfly", name="Dragonfly",  areas=[".", "%"], power=1, attack=3, defence=0, hitpoints=8, agility=22, experiencePoints=3, gold=4)

class Rat(Enemy):
    def __init__(self):
        super().__init__(type="Rat", name="Rat",  areas=[".", "%"], power=1, attack=1, defence=0, hitpoints=10, agility=17, experiencePoints=2, gold=5)

class GrassGoblin(Enemy):
    def __init__(self):
        super().__init__(type="Goblin", name="Goblin", areas=[".", "%"], power=2, attack=2, defence=0, hitpoints=20, agility=15, experiencePoints=5, gold=8)



class Snake(Enemy):
    def __init__(self):
        super().__init__(type="Snake", name="Snake", areas=["%"], power=3, attack=3, defence=0, hitpoints=25, agility=19, weapon="Poison-Tipped Dagger", experiencePoints=8, gold=12)

class WildSlime(Enemy):
    def __init__(self):
        super().__init__(type="Wild Slime", name="Wild Slime", areas=["%", "^"], power=1, attack=2, defence=0, hitpoints=15, agility=10, experiencePoints=4, gold=9)

class MountainGoblin(Enemy):
    def __init__(self):
        super().__init__(type="Mountain Goblin", name="Mountain Goblin", areas=["^"], power=1, attack=2, defence=0, hitpoints=30, agility=15, experiencePoints=5, gold=12)

class JumpingSpider(Enemy):
     def __init__(self):
        super().__init__(type="Jumping Spider", name="Jumping Spider", power=5, attack=10, defence=0, hitpoints=30, agility=13, weapon="Poison-Tipped Dagger", experiencePoints=8, gold=12)

class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Dragon", attack=15, hitpoints=100, agility=25)

class PlainsGoldenDice(Enemy):
     def __init__(self):
        super().__init__(type="Golden Dice", name="Golden Dice", areas=[".", "%", "^"], power=2, attack=10, defence=1000, hitpoints=5, agility=50, weapon="Poison-Tipped Dagger", experiencePoints=0, gold=120)


enemyList = [Slime(), WildSlime(), Dragonfly(), GrassGoblin(), MountainGoblin(), Snake()]