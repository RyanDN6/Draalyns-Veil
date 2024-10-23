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

#This function types attackers out one at a time, and can colour/play sound
def text(words="", delay=0.015, colour='white', sound=False):
    for char in words:
        if sound:
            playsound.playsound(sound="sounds/text.mp3", block=False) #playsound function needs to be downloaded, type "pip install playsound" into your terminal
        sleep(delay)
        print(f"\033[1;{colours[colour]};40m{char}", end="", flush=True) #DO NOT TOUCH THIS, IT WILL BREAK THE WHOLE FUNCTION
        if char in ".,!?:;": #Makes the text wait a little longer once it encounters puncuation. Makes text flow nicer
            sleep(delay * 5)
    print("\n") #Printing an empty line at the end just makes the writing easier to read, giving space between lines

class Taunt(object):
    def __init__(self, name="Taunt", staminaConsumption=3, hit="me"):
        self.name = name
        self.staminaConsumption = staminaConsumption
        self.hit = hit
    def use(self, attacker):
        attacker.stamina -= self.staminaConsumption
        attacker.taunt = True
        text(f"{attacker.name} taunts their opponents!\nThe enemies now target {attacker.name}.")


class Heal(object):
    def __init__(self, name="Heal", staminaConsumption=5, hit="party"):
        self.name = name
        self.staminaConsumption = staminaConsumption
        self.hit = hit
    def use(self, attacker, target):
        attacker.stamina -= self.staminaConsumption
        hp = target.hitpoints
        target.hitpoints = min(target.hitpoints + target.maxHitpoints // 5, target.maxHitpoints)
        text(f"{attacker.name} emits a healing aura.\n{target.name} heals for {target.hitpoints - hp} HP!")
        text(words=f"{fight.healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}", colour='green', delay=0)

class Senkatto(object):
    def __init__(self, name="Senkatto", staminaConsumption=6, hit="enemy"):
        self.name = name
        self.staminaConsumption = staminaConsumption
        self.hit = hit
    def use(self, attacker, target):
        attacker.stamina -= self.staminaConsumption
        text(f"{attacker.name} strikes relentlessly!")
        if attacker.stamina > 0:
            damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
            if target.defend:
                damage = damage // 2

        if random.randint(1,2) == 1:
            text(f"{attacker.name} draws blood! {target.name} is bleeding.", colour='red')
            target.bleeding = True
            text(f"{attacker.name} recovers 2 stamina!")
            attacker.stamina += 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        if target.ally:
            return text(f"{target.name} takes {damage} damage!", colour='red')
        else:
            return text(f"The {target.name} takes {damage} damage!", colour='red')