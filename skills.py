import playsound, fight, weapons, random
from time import sleep

#Colour codes for the text function
colours = {
    'red': "31",
    'green': "32",
    'yellow': "33",
    'blue': "34",
    'purple': "35",
    'cyan': "36",
    'white': "0",
}

def text(words="", colour='white', slow=False, fast=False, stop=False):

    d = 0.015
    
    if slow:
        d = max(0.1, d * 3)
    elif fast:
        d = 0
    
    for char in words:
        sleep(d)  # Use the class's delay attribute
        print(f"\033[1;{colours[colour]};40m{char}", end="", flush=True) 
        
        if char in ".,!?:;":
            sleep(d * 5)
    
    if stop:
        input()

    print("\n")

class Taunt(object):
    def __init__(self, name="Taunt", spConsumption=3, hit="me"):
        self.name = name
        self.spConsumption = spConsumption
        self.hit = hit
    def use(self, attacker):
        attacker.sp -= self.spConsumption
        attacker.taunt = True
        text(f"{attacker.name} taunts their opponents!\nThe enemies now target {attacker.name}.", stop=True)


class Heal(object):
    def __init__(self, name="Heal", spConsumption=5, hit="party"):
        self.name = name
        self.spConsumption = spConsumption
        self.hit = hit
    def use(self, attacker, target):
        attacker.sp -= self.spConsumption
        hp = target.hitpoints
        target.hitpoints = min(target.hitpoints + target.maxHitpoints // 5, target.maxHitpoints)
        text(f"{attacker.name} emits a healing aura.\n{target.name} heals for {target.hitpoints - hp} HP!")
        text(words=f"{fight.healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}", colour='green', fast=True, stop=True)

class Senkatto(object):
    def __init__(self, name="Senkatto", spConsumption=6, hit="enemy"):
        self.name = name
        self.spConsumption = spConsumption
        self.hit = hit
    def use(self, attacker, target):
        attacker.sp -= self.spConsumption
        text(f"{attacker.name} strikes relentlessly!")
        if attacker.sp > 0:
            damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
            if target.defend:
                damage = damage // 2

        if random.randint(1,2) == 1:
            text(f"{attacker.name} draws blood! {target.name} is bleeding.", colour='red')
            target.bleeding = True
            text(f"{attacker.name} recovers 2 SP!", stop=True)
            attacker.sp += 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        return text(f"{target.name} takes {damage} damage!", colour='red', stop=True)
    
class Singe(object):
    def __init__(self, name="Singe", spConsumption=3, hit="enemy"):
        self.name = name
        self.spConsumption = spConsumption
        self.hit = hit
    
    def use(self, attacker, target):
        attacker.sp -= self.spConsumption
        
        text(f"{attacker.name} conjures a ball of fire and throws it at {target.name}!")
        
        damage = (attacker.magic + 8 + random.randint(1, 6))
        
        if target.defend:
            damage //= 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        return text(f"{target.name} takes {damage} damage!", colour='red', stop=True)