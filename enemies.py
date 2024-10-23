import weapons
class Enemy:
    def __init__(self, name, ally=False, attack=0, defence=0, hitpoints=0, stamina=0, staminaRecovery=0, weapon="Poison-Tipped Dagger", experiencePoints=0, gold=0, defend=False, stunned=False, poisoned=0, bleeding=False):
        self.name = name
        self.ally = ally
        self.attack = attack
        self.hitpoints = hitpoints
        self.maxHitpoints = hitpoints
        self.weapon = weapons.weaponsList[weapon]
        self.stamina = stamina
        self.maxStamina = self.stamina
        self.staminaRecovery = staminaRecovery
        self.experiencePoints = experiencePoints
        self.gold = gold
        self.defend = defend
        self.stunned = stunned
        self.poisoned = poisoned
        self.bleeding = bleeding
        self.defence = defence

class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", attack=1, hitpoints=25, stamina=48, experiencePoints=5, gold=20)

class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Dragon", attack=15, hitpoints=100, stamina=20)

class Sephiroth(Enemy):
    def __init__(self):
        super().__init__(name="Sephiroth", attack=25, hitpoints=150, stamina=50, weapon="Katana", experiencePoints=100, gold=500)
        