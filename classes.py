import weapons, skills

class Character(object):
    def __init__(self, ally=True, name="", info="", maxHitpoints=100, defence=0, attack=0, agility=0, evasion=0, luck=0, skill="", weapon="Fists", stamina=50, staminaRecovery=3, defend=False, taunt=False, stunned=False, poisoned=0, bleeding=False):
        self.skill = skill
        self.skills = [getattr(skills, skill)()]
        self.ally = ally
        self.name = name
        self.info = info
        self.maxHitpoints = maxHitpoints
        self.hitpoints = self.maxHitpoints
        self.defence = defence
        self.attack = attack
        self.agility = agility
        self.evasion = evasion
        self.luck = luck
        self.weapon = weapons.weaponsList[weapon]
        self.stamina = stamina
        self.maxStamina = self.stamina
        self.staminaRecovery = staminaRecovery
        self.defend = defend
        self.taunt = taunt
        self.stunned = stunned
        self.poisoned = poisoned
        self.bleeding = bleeding

class Barbarian(Character):
    def __init__(self):
        super().__init__(name="Barbarian", info="The Barbarian is a kilt-clad warrior hungry for destruction. Big damage and health numbers, little stamina.", maxHitpoints=115, weapon="Battleaxe", skill="Bloodrage")

class Samurai(Character):
    def __init__(self):
        super().__init__(name="Samurai", info="The Samurai is a disciplined killer, adept and honourable.", maxHitpoints=95, weapon="Katana", skill="Senkatto")

class Pirate(Character):
    def __init__(self):
        super().__init__(name="Pirate",info="The Pirate is a plundering outlaw, experienced with combat and their cutlass.", maxHitpoints=105, weapon="Hook", skill="Plunder")

class Paladin(Character):
    def __init__(self):
        super().__init__(name="Paladin", info="The Paladin is the King's loyal subject, a strong and stoic knight", maxHitpoints=125, weapon="Hammer", skill="Taunt")

class Assassin(Character):
    def __init__(self):
        super().__init__(name="Assassin", info="The Assassin is a lethal and deadly hunter. Fast attacks with a high chance for critical hits.", maxHitpoints=80, weapon="Dagger", skill="Backstab")