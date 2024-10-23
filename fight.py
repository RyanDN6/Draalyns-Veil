import random, playsound
from time import sleep

colours = {
    'red': "31",
    'green': "32",
    'yellow': "33",
    'blue': "34",
    'purple': "35",
    'cyan': "36",
    'white': "0",
}

def healthBar(name, hitpoints, maxHitpoints, length):
    dashConvert = int(maxHitpoints / length)
    currentDashes = int(hitpoints / dashConvert)
    remaininghitpoints = length - currentDashes

    hitpointsDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remaininghitpoints
    
    return f"{name}'s HP: {hitpoints}/{maxHitpoints}    |{hitpointsDisplay}{remainingDisplay}|"

def staminaBar(name, stamina, maxStamina, length):
    dashConvert = int(maxStamina / length)
    currentDashes = int(stamina / dashConvert)
    remainingstamina = length - currentDashes

    staminaDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remainingstamina
    
    return f"{name}'s Stamina: {stamina}/{maxStamina} |{staminaDisplay}{remainingDisplay}|"

def text(words="", delay=0.015, colour='white', sound=False):
    for char in words:
        if sound:
            playsound.playsound(sound="sounds/text.mp3", block=False)
        sleep(delay)
        print(f"\033[1;{colours[colour]};40m{char}", end="", flush=True)
        if char in ".,!?:;":
            sleep(delay * 5)
    print("\n")

def defend(attacker):
    if attacker.ally:
        attacker.defend = True
        text(f"{attacker.name} defends!", colour="cyan")

def attack(attacker, target):

    if attacker.ally:
        text(f"{attacker.name} attacks the {target.name}!")
    else:
        text(f"The {attacker.name} attacks {target.name}!")
    if attacker.stamina > 0:
        attacker.stamina -= attacker.weapon.staminaConsumption
        damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
        if target.defend:
            damage = damage // 2
        if attacker.stamina < 0:
            damage = damage // 2
            text("They are too tired for a strong attack...", colour='blue')

        acc = random.randint(1, 100)

        if attacker.stunned:
            acc = 100
            if attacker.ally:
                text(f"{attacker.name} is stunned.", colour="yellow")
            else:
                text(f"The {attacker.name} is stunned.", colour="yellow")

        if acc < attacker.weapon.accuracy:
            if attacker.weapon.bleed:
                if random.randint(1,6) == 1:
                    if target.ally:
                        text(f"The {attacker.name} draws blood! {target.name} is bleeding.", colour='red')
                    else:
                        text(f"{attacker.name} draws blood! The {target.name} is bleeding.", colour='red')
                    target.bleeding = True
            elif attacker.weapon.stun:
                if random.randint(1,3) == 1:
                    if target.ally:
                        text(f"The {attacker.name} lands a concussing blow! {target.name} is stunned.", colour='yellow')
                    else:
                        text(f"{attacker.name} lands a concussing blow! The {target.name} is stunned.", colour='yellow')
                    target.stunned = True
            elif attacker.weapon.poison:
                if random.randint(1,3) == 1:
                    if target.ally:
                        text(f"The {attacker.name} poisons {target.name}!", colour='purple')
                    else:
                        text(f"{attacker.name} poisons the {target.name}!", colour='purple')
                    if target.poisoned == 0:
                        target.poisoned = 0.01
                    else:
                        text(f"But they're already poisoned!", colour='green')
            crit = random.randint(1, 100)
            if crit < attacker.weapon.critChance:
                damage = damage * 2
                target.hitpoints -= damage
                target.hitpoints = max(target.hitpoints, 0)
                if target.ally:
                    return text(f"{attacker.name} landed a critical hit!\nThe {target.name} takes {damage} damage!", colour='red')
                else:
                    return text(f"The {attacker.name} landed a critical hit!\nThe {target.name} takes {damage} damage!", colour='red')
            else:
                target.hitpoints -= damage
                target.hitpoints = max(target.hitpoints, 0)
                if target.ally:
                    return text(f"{target.name} takes {damage} damage!", colour='red')
                else:
                    return text(f"The {target.name} takes {damage} damage!", colour='red')

        else:
            if attacker.ally:
                return text(f"{attacker.name} missed.")
            else:
                return text(f"The {attacker.name} missed.")
    else:
        return text("But they're exhausted...", colour='blue')