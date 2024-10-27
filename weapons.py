class Weapon:
    def __init__(self, name, accuracy=0, critChance=0, damage=0, damageRoll=0, stun=False, poison=False, bleed=False, users=None):
        self.name = name
        self.damage = damage
        self.stun = stun
        self.poison = poison
        self.bleed = bleed
        self.damageRoll = damageRoll
        self.accuracy = accuracy
        self.critChance = critChance
        if users == None:
            self.users = []
        else:
            self.users = users

weaponsList = {
    "Greatsword": Weapon(name = "Greatsword", accuracy=75, critChance=5, damage=10, damageRoll=6, users=["Hero"]),
    "Battleaxe": Weapon(name="Battleaxe", accuracy=85, damage=8, critChance=5, damageRoll=6),
    "Hammer": Weapon(name="Hammer", accuracy=75, damage=7, critChance=8, damageRoll=4, stun=True),
    "Morning Star": Weapon(name="Morning Star", accuracy=80, critChance=10, damage=7, damageRoll=7),
    "Sword": Weapon(name="Sword", damage=6, damageRoll=3, accuracy=92, critChance=8, users=["Hero"]),
    "Katana": Weapon(name="Katana", damage=5, damageRoll=3, accuracy=80, critChance=15, bleed=True),
    "Quaterstaff": Weapon(name="Quarterstaff", damage=5, accuracy=85, critChance=10, damageRoll=6),
    "Club": Weapon(name="Club", damage=4, damageRoll=4, accuracy=80, critChance=10, stun=True),
    "Dagger": Weapon(name="Dagger", damage=2, damageRoll=2, accuracy=95, critChance=40, bleed=True),
    "Poison-Tipped Dagger": Weapon(name="Poison-Tipped Dagger", damage=1, accuracy=85, critChance=20, damageRoll=2, poison=True),
    "Hook": Weapon(name="Hook", damage=0, damageRoll=2, accuracy=90, critChance=12, bleed=True),
    "Fists": Weapon(name="Weapon", damage=1, damageRoll=3, accuracy=90, critChance=1)  
}