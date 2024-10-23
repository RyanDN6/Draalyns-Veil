class Weapon:
    def __init__(self, name, accuracy=0, critChance=0, damage=0, damageRoll=0, procCoefficient=0, staminaConsumption=0, stun=False, poison=False, bleed=False):
        self.name = name
        self.damage = damage
        self.procCoefficient = procCoefficient
        self.staminaConsumption = staminaConsumption
        self.stun = stun
        self.poison = poison
        self.bleed = bleed
        self.damageRoll = damageRoll
        self.accuracy = accuracy
        self.critChance = critChance

weaponsList = {
    "Greatsword": Weapon(name = "Greatsword", accuracy=75, critChance=5, damage=10, damageRoll=6, procCoefficient=0, staminaConsumption=5),
    "Battleaxe": Weapon(name="Battleaxe", accuracy=85, damage=8, critChance=5, damageRoll=6, procCoefficient=0, staminaConsumption=4),
    "Hammer": Weapon(name="Hammer", accuracy=75, damage=7, critChance=8, damageRoll=4, procCoefficient=0, staminaConsumption=4, stun=True),
    "Morning Star": Weapon(name="Morning Star", accuracy=80, critChance=10, damage=7, damageRoll=7, procCoefficient=0, staminaConsumption=4),
    "Sword": Weapon(name="Sword", damage=6, damageRoll=5, accuracy=90, critChance=12, procCoefficient=0, staminaConsumption=3),
    "Katana": Weapon(name="Katana", damage=5, damageRoll=3, accuracy=80, critChance=15, procCoefficient=0, staminaConsumption=3, bleed=True),
    "Quaterstaff": Weapon(name="Quarterstaff", damage=5, accuracy=85, critChance=10, damageRoll=6, procCoefficient=0, staminaConsumption=3),
    "Club": Weapon(name="Club", damage=4, damageRoll=4, accuracy=80, critChance=10, procCoefficient=0, staminaConsumption=3, stun=True),
    "Dagger": Weapon(name="Dagger", damage=2, damageRoll=2, accuracy=95, critChance=40, procCoefficient=0, staminaConsumption=1, bleed=True),
    "Poison-Tipped Dagger": Weapon(name="Poison-Tipped Dagger", damage=1, accuracy=85, critChance=20, damageRoll=2, procCoefficient=0, staminaConsumption=2, poison=True),
    "Hook": Weapon(name="Hook", damage=0, damageRoll=2, procCoefficient=0, accuracy=90, critChance=12, staminaConsumption=2, bleed=True),
    "Fists": Weapon(name="Weapon", damage=1, damageRoll=3, procCoefficient=0, accuracy=90, critChance=1, staminaConsumption=2,)  
}