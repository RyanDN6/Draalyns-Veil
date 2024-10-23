import classes, pyfiglet, winsound, playsound, enemies, fight, random, skills
from time import sleep

letters = ["A", "B", "C", "D", "E", "F"]

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

class TextScroller:
    def __init__(self):
        self.delay = 0.04  # Default base speed

    def confirm(self): 
        a = ""
        while a not in ["y", "n"]:
            for char in "(y/n)":
                print(f"\033[1;32;40m{char}", end="")
            
            print(":", end=" ")
            a = input()
        
        return a.lower() == "y"

    def scrollSpeed(self):
        while True:
            try:
                print("Choose your scroll speed:")
                print("1 (FASTEST)")
                print("2 (FASTER)")
                print("3 (FAST)")
                print("4 (NORMAL)")
                print("5 (SLOW)")
                print("6 (SLOWER)")
                print("7 (SLOWEST)")
                n = int(input())
                if 0 < n < 8:
                    speed = float(f"0.0{n}")
                    example = "This is a sample text for you to see your target speed. If you would like to change your choice, type 'n'. Otherwise, type 'y' to confirm."
                    for i in range(len(example)):
                        print(example[i], end="", flush=True)
                        sleep(speed)
                        if example[i] in ".,!?:;":
                            sleep(speed * 5)
                    
                    print("\n")

                    if self.confirm():
                        self.delay = speed  # Update the base delay
                        return speed
                    else:
                        continue 
            
            except Exception:
                continue

    def text(self, words="", colour='white', slow=False, fast=False):

        d = self.delay
        
        if slow:
            d = max(0.1, self.delay * 3)
        elif fast:
            d = 0
        
        for char in words:
            sleep(d)  # Use the class's delay attribute
            print(f"\033[1;{colours[colour]};40m{char}", end="", flush=True) 
            
            if char in ".,!?:;":
                sleep(self.delay * 5)
        
        print("\n")


def menu(scroll):
    while True: # Will have a save/load function hopefully, for now just a title screen.
        scroll.text(pyfiglet.figlet_format("Draayln's Veil"), colour='blue') #may need to pip install pyfiglet, im not too sure but if it doesnt work then yes do it
        sleep(2)
        print("\n" * 4)
        
        menuOptions = ["New", "Save", "Load", "Options"]

        scroll.text("'New' = NEW GAME", colour='blue')
        scroll.text("'Save' = SAVE GAME", colour='blue')
        scroll.text("'Load' = LOAD GAME", colour='blue')
        scroll.text("'Options' = OPTIONS", colour='blue')
        
        print("TYPE OUT YOUR CHOICE")
        a = input().capitalize()
        
        while a not in menuOptions:
            print("TYPE OUT YOUR CHOICE")
            a = input().capitalize()
    
    #if a == "New":
        #start()

"""
while True:
    text(words="Choose your class:", sound=True)
    options = ["===================", "Barbarian", "Pirate", "Samurai", "Paladin", "Assassin", "==================="] # more will be added here. can be soft coded but not for now.
    text(words="\n".join(options))
    text(words="Type a name to view more.", sound=True)
    choice = input().capitalize() #inputting names is case-insensitive using the .capitalize() function

    while choice not in options:
        text("Type a name to view more.")
        choice = input().capitalize()

    character = getattr(classes, choice)()
    text(f'\n{character.info}\nWeapon: {character.weapon.name}\nSkill: {character.skill}') #Gives some info on the class you typed

    if confirm():
        text(words=f"You've chosen the {choice}.", colour='red', sound=True)
    else:
        continue
    while True:
        text("Please enter your character's name.")
        name = input()
        if name == "":
            text("Your name can't be blank.")
            continue
        else:
            text(f"Are you sure you want the name '{name}'")
        if confirm():
            character.name = name
            text(f"Your name is {character.name}, the {choice}")
            sleep(1)
            break
        else:
            continue
    break
Buddy = classes.Samurai()
Buddy.name = "Buddy"
characterList = [character, Buddy] #Adds your character to a list that will eventually have up to 4 characters inside.
Buddy.skills.append(getattr(skills, "Heal")())
text("Would you like a quick tutorial?")

if confirm():

    while True:
        winsound.PlaySound(None, winsound.SND_FILENAME) #This is how to stop the original song
        text("Time for your first battle...", delay=0.06, sound=True)
        winsound.PlaySound("sounds/Battle.wav", winsound.SND_LOOP + winsound.SND_ASYNC) #This starts the battle theme
        enemyList = [enemies.Goblin(), enemies.Goblin()] #This can be randomised, for now is hardcoded as its a tutorial
        #enemyList = [enemies.Sephiroth()] #Bossfight test
        experience = 0
        gold = 0
        for enemy in enemyList:
            text(f"A {enemy.name} approaches!")
        #text(f"The One-Winged Angel perches.", delay=0.1, colour="purple")
        enemies_dead = False
        characters_dead = False

        taunt_temp = 0

        while len(characterList) != 0 and len(enemyList) != 0: #Due to perma death, the fight continues until either the list of enemies or the list of characters is empty.
            entities = enemyList + characterList #Puts every active member of the fight together
            order = sorted(entities, key=lambda x: x.stamina) #Uses lambda to sort by stamina for whos turn it is 
            attacker = order[-1] # order[-1] is the highest stamina currently
    
            sleep(1)

            if attacker.bleeding:
                hp = attacker.hitpoints
                attacker.hitpoints = max(0, attacker.hitpoints - int(attacker.maxHitpoints * 0.08) + 1)
                if attacker.ally:
                    text(f"{attacker.name}'s bleeds.\n{attacker.name} takes {hp - attacker.hitpoints} damage!", colour="red")
                else:
                    text(f"The {attacker.name}'s bleeds.\nThe {attacker.name} takes {hp - attacker.hitpoints} damage!", colour="red")

            if attacker.poisoned:
                hp = attacker.hitpoints
                attacker.hitpoints = max(0, attacker.hitpoints - int((attacker.maxHitpoints * attacker.poisoned) + 1))
                if attacker.ally:
                    text(f"The venom attacks {attacker.name}.\n{attacker.name} takes {hp - attacker.hitpoints} damage!", colour="purple")
                else:
                    text(f"The venom attacks the {attacker.name}.\nThe {attacker.name} takes {hp - attacker.hitpoints} damage!", colour="purple")
                attacker.poisoned = min(0.16, attacker.poisoned * 2)
                
            if attacker.stunned:
                if attacker.ally:
                    text(f"{attacker.name} is too stunned to move!", colour="yellow")
                else:
                    text(f"The {attacker.name} is too stunned to move!", colour="yellow")
                            
            if attacker.hitpoints == 0:
                if attacker.ally:
                    text(f"{attacker.name} has died!")
                    characterList.remove(attacker)
                else:
                    text(f"The {attacker.name} has died!")
                    experience += attacker.experiencePoints
                    gold += attacker.gold
                    enemyList.remove(attacker) #Remove dead enemies from the list


            if attacker in characterList: #If the highest stamina is in your party
                
                text(f"Its {attacker.name}'s turn!")

                for character in characterList:
                    text(words=f"{fight.staminaBar(character.name, character.stamina, character.maxStamina, character.maxStamina)}", colour='green', delay=0)
                    if character.hitpoints / character.maxHitpoints < 0.25: #if hp < 25%: their name is red
                        text(words=f"{fight.healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4)}", colour='red', delay=0)
                    elif character.hitpoints / character.maxHitpoints < 0.5: #if hp < 50%: their name is yellow
                        text(words=f"{fight.healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4)}", colour='yellow', delay=0)
                    else:
                        text(words=f"{fight.healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4)}", delay=0)
                ################################################### ONLY WAY I CAN MANAGE TO RESET SKILLS IS IN HERE ONCE ITS THEIR TURN
                if attacker.defend:
                    text(f"{attacker.name} lowers their guard.")
                    attacker.defend = False

                if attacker.taunt:
                    taunt_temp += 1
                    if taunt_temp == 2:
                        attacker.taunt = False
                        text(f"{attacker.name}'s taunt wears off.")
                ###################################################
                

                text(words=f"Enter = Attack ({attacker.weapon.staminaConsumption} Stamina) | 's' = Skills | 'i' = Item | 'd' = Defend | 'f' = Flee |'?' = Info |", delay=0, colour="cyan")
                a = input()

                if a == "":
                    while True:
                        try:
                            text("Attack who? (Type the NUMBER of the enemy)")
                            i = 0
                            for enemy in enemyList:
                                status_indicators = []
                                if enemy.stunned:
                                    status_indicators.append("(Stn)")
                                if enemy.poisoned:
                                    status_indicators.append("(Psn)")
                                if enemy.bleeding:
                                    status_indicators.append("(Bld)")

                                status_string = " ".join(status_indicators)

                                if enemy.hitpoints / enemy.maxHitpoints < 0.25:
                                    text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}", colour='red')
                                elif enemy.hitpoints / enemy.maxHitpoints < 0.5:
                                    text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}", colour='yellow')
                                else:
                                    text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}")
                                
                                i += 1
                            pick = int(input()) - 1
                            enemy.name = enemy.name.split("(")[0]
                            target = enemyList[pick]
                            fight.attack(attacker, target)
                            break
                        except Exception:
                            continue

                elif a == "f":
                    text("This is a tutorial, fight!")
                    continue
                elif a == "d":
                    fight.defend(attacker)
                elif a == "s":
                        try:
                            text("Which skill? (Type the NUMBER of the skill)")
                            skillList = attacker.skills
                            i = 0
                            for skill in skillList:
                                i = i + 1
                                if attacker.stamina - skill.staminaConsumption < 0:
                                    text(f"{i} = {skill.name} ({skill.staminaConsumption})", colour="red")
                                else:
                                    text(f"{i} = {skill.name} ({skill.staminaConsumption})")
                            pick = int(input()) - 1
                            tempSkill = skillList[pick]


                            if tempSkill.hit == "me":
                                tempSkill.use(attacker)


                            elif tempSkill.hit == "party":
                                text("Use on who? (Type the NUMBER of the ally)")
                                i = 0
                                for character in characterList:
                                    i = i + 1
                                    if character.hitpoints / character.maxHitpoints < 0.25: #if hp < 25%: their name is red
                                        text(f"{i} = {character.name} ", colour='red')
                                    elif character.hitpoints / character.maxHitpoints < 0.5: #if hp < 50%: their name is yellow
                                        text(f"{i} = {character.name}", colour='yellow')
                                    else:
                                        text(f"{i} = {character.name}")
                                pick = int(input()) - 1
                                target = characterList[pick]
                                tempSkill.use(attacker, target)


                            elif tempSkill.hit == "enemy":
                                text("Attack who? (Type the NUMBER of the enemy)")
                                i = 0
                                for enemy in enemyList:
                                    status_indicators = []
                                    if enemy.stunned:
                                        status_indicators.append("(Stn)")
                                    if enemy.poisoned:
                                        status_indicators.append("(Psn)")
                                    if enemy.bleeding:
                                        status_indicators.append("(Bld)")

                                    status_string = " ".join(status_indicators)

                                    if enemy.hitpoints / enemy.maxHitpoints < 0.25:
                                        text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}", colour='red')
                                    elif enemy.hitpoints / enemy.maxHitpoints < 0.5:
                                        text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}", colour='yellow')
                                    else:
                                        text(f"{i + 1} = {enemy.name} {" ".join(status_indicators)}")
                                    
                                    i += 1

                                pick = int(input()) - 1
                                target = enemyList[pick]
                                tempSkill.use(attacker, target)

                        except Exception:
                            continue
                for target in enemyList:
                    if target.hitpoints == 0:
                        text(f"{target.name} has died!")
                        experience += target.experiencePoints
                        gold += target.gold
                        enemyList.remove(target) #Remove dead enemies from the list

            else:
                text(f"It's the {attacker.name}'s turn")
                target = random.choice(characterList) #Party is attacked at random

                for character in characterList:
                    if character.taunt:
                        target = character
                        text(f"The enemy is enraged by {character.name}'s taunt!")

                sleep(1)
                fight.attack(attacker, target)
                text(words=f'{fight.healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}', delay=0, colour="red") #Displays health bar
                if target.hitpoints == 0:
                    text(f"{target.name} has died!")
                    characterList.remove(target) #removes dead party member - permadeath
                print()
        text("All enemies have been defeated!")
        text(f"You gained {experience} XP.")
        text(f"You gained {gold} Gold.")

        break
else:
    text("Choose which path")
"""

if __name__ == '__main__':
    scroll = TextScroller()
    scroll.scrollSpeed()
    scroll.text("This is a test please work... PLEASE!!")

    menu(scroll)