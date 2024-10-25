import weapons

class Character(object):
    def __init__(self, ally=True, type="", name="", info="", maxHitpoints=100, defence=0, attack=0, magic=0, agility=0, evasion=0, luck=0, skill="", weapon="Fists", sp=20, spRecovery=3, defend=False, taunt=False, stunned=False, poisoned=0, bleeding=False):
        self.skill = skill
        self.level = 0
        self.experience = 0
        self.type = type
        self.skills = []
        self.ally = ally
        self.name = name
        self.info = info
        self.maxHitpoints = maxHitpoints
        self.hitpoints = self.maxHitpoints
        self.defence = defence
        self.attack = attack
        self.magic = magic
        self.agility = agility
        self.evasion = evasion
        self.luck = luck
        self.weapon = weapons.weaponsList[weapon]
        self.sp = sp
        self.maxSp = self.sp
        self.spRecovery = spRecovery
        self.defend = defend
        self.taunt = taunt
        self.stunned = stunned
        self.poisoned = poisoned
        self.bleeding = bleeding
    
class Hero(Character):
    def __init__(self):
        super().__init__(type="Hero", name="Hero", info="Hailing from a lineage of Kings and determined to stop the source of the land's blight, he wields his sword and shield", maxHitpoints=30, defence=0, attack=2, magic=2, agility=15, skill="Singe", weapon="Sword", sp=6)

class Barbarian(Character):
    def __init__(self):
        super().__init__(type="Barbarian", name="Barbarian", info="The Barbarian is a kilt-clad warrior hungry for destruction. Big damage and health numbers, little stamina.", maxHitpoints=50, agility=5, weapon="Battleaxe", skill="Bloodrage", sp=5)

class Samurai(Character):
    def __init__(self):
        super().__init__(type="Samurai", name="Samurai", info="The Samurai is a disciplined killer, adept and honourable.", maxHitpoints=25, agility=12, weapon="Katana", skill="Senkatto", sp=8)

class Pirate(Character):
    def __init__(self):
        super().__init__(type="Pirate", name="Pirate",info="The Pirate is a plundering outlaw, experienced with combat and their cutlass.", maxHitpoints=35, agility=18, weapon="Hook", skill="Plunder", sp=6)

class Paladin(Character):
    def __init__(self):
        super().__init__(type="Paladin", name="Paladin", info="The Paladin is the King's loyal subject, a strong and stoic knight", maxHitpoints=60, agility=8, weapon="Hammer", skill="Taunt", sp=10)

class Assassin(Character):
    def __init__(self):
        super().__init__(type="Assassin", name="Assassin", info="The Assassin is a lethal and deadly hunter. Fast attacks with a high chance for critical hits.", maxHitpoints=20, agility=25, weapon="Dagger", skill="Backstab", sp=9)