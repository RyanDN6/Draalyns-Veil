import os, sys, copy, platform, classes, levels, pyfiglet, town, enemies, random, map, curses
from time import sleep
from pygame import mixer # Load the required libraries

os.chdir(os.path.dirname(os.path.abspath(__file__)))

mixer.init()

#Difficulty of encounters based on tile of battle
tiles = {
    '.': (1, 2),
    '^': (3, 5),
    '%': (2, 4),
    '~': (1, 3)
}

def clear():
    os.system('cls')

def taunt(scroll, attacker, hit="me", sp_consumption=3):
    attacker.sp -= sp_consumption
    attacker.taunt = True
    scroll.text(f"{attacker.name} taunts their opponents!\nThe enemies now target {attacker.name}.", hold=True)

def heal(scroll, attacker, target, hit="party", sp_consumption=5):
    attacker.sp -= sp_consumption
    hp = target.hitpoints
    target.hitpoints = min(hp + 16 + attacker.magic, target.maxHitpoints)
    scroll.text(f"{attacker.name} emits a healing aura.\n{target.name} heals for {target.hitpoints - hp} HP!")
    scroll.text(words=f"{healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}", colour='green', fast=True, hold=True)

def senkatto(scroll, attacker, target, hit="enemy", sp_consumption=6):
    attacker.sp -= sp_consumption
    scroll.text(f"{attacker.name} strikes relentlessly!")

    if attacker.sp > 0:
        damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
        if target.defend:
            damage //= 2

        if random.randint(1, 2) == 1:
            scroll.text(f"{attacker.name} draws blood! {target.name} is bleeding.", colour='red')
            target.bleeding = True
            scroll.text(f"{attacker.name} recovers 2 SP!", hold=True)
            attacker.sp += 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        return scroll.text(f"{target.name} takes {damage} damage!", colour='red', hold=True)

def singe(scroll, attacker, target, hit="enemy",sp_consumption=3):
    attacker.sp -= sp_consumption
    
    scroll.text(f"{attacker.name} conjures a ball of fire and throws it at {target.name}!")
    
    damage = (attacker.magic + 8 + random.randint(1, 6))
    
    if target.defend:
        damage //= 2

    target.hitpoints -= damage
    target.hitpoints = max(target.hitpoints, 0)
    return scroll.text(f"{target.name} takes {damage} damage!", colour='red', hold=True)

skills = {
    "Singe":
    {
        "name": "Singe",
        "function": singe,
        "spConsumption": 3,
        "hit": "enemy"
    },

    "Heal":
    {
        "name": "Heal",
        "function": heal,
        "spConsumption": 5,
        "hit": "party"
    }
}

class TextScroller:
    def __init__(self, delay=0.04):
        self.delay = delay  # Default base speed
        self.support = self.supports_color()
        self.sound = mixer.Sound('sounds\\text.mp3')
        self.typing = mixer.Channel(1)

        #Colour codes for the text function
        self.colours = {
            'red': "31",
            'green': "32",
            'yellow': "33",
            'blue': "34",
            'purple': "35",
            'cyan': "36",
            'white': "0",
        }

    def supports_color(self):
        """
        Check if the terminal supports color.
        Returns True if ANSI color codes are likely to work.
        """
        # Return True if NO_COLOR is not set (respecting color disable preference)
        if 'NO_COLOR' in os.environ:
            return False
            
        # Force color if FORCE_COLOR is set
        if 'FORCE_COLOR' in os.environ:
            return True

        # Check common color-supporting environment variables
        if any(os.environ.get(var) for var in [
            'TERM', 'COLORTERM', 'CLICOLOR', 'FORCE_COLOR', 'ConEmuANSI'
        ]):
            return True

        # Check for Windows specific environment
        if platform.system().lower() == 'windows':
            return (
                'ANSICON' in os.environ
                or 'WT_SESSION' in os.environ  # Windows Terminal
                or os.environ.get('TERM_PROGRAM') == 'vscode'
                or 'TERM' in os.environ
            )

        # Default to True for non-Windows systems
        return True

    def confirm(self): 
        a = ""
        while a not in ["y", "n"]:
            a = input("Confirm? (y/n): ")
        
        print()
        
        return a.lower() == "y"

    def scrollSpeed(self, first=False):
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
                    speed = float(f"0.0{n}") / 2
                    
                    if first:
                        example = "This is a sample text for you to see your target speed. Go to the options menu to change this."
                    else:
                        example = "This is a sample text for you to see your NEW target speed. Please confirm this change below."
                    
                    for i in range(len(example)):
                        print(example[i], end="", flush=True)
                        sleep(speed)
                        if example[i] in ".,!?:;":
                            sleep(speed * 5)
                    
                    input()
                    print("\n")

                    if first or self.confirm():
                        self.delay = speed
                        return
                    
                    else:
                        continue
            
            except Exception:
                continue

    def text(self, words="", colour='white', sound=False, slow=False, fast=False, stop=False, hold=False, talking=False):
        
        support = self.support
        d = self.delay
        
        if talking:
            d = max(0.05, d)

        if slow:
            d = max(0.1, d * 3)
        elif fast:
            d = 0
        
        for i in range(len(words)):
            
            sleep(d)  # Use the class's delay attribute
            
            
            if sound:
                self.typing.play(self.sound)
            
            if support:
                print(f"\033[1;{self.colours[colour]};40m{words[i]}", end="", flush=True) 
            else:
                print(words[i], end="", flush=True)
            
            if words[i] in ".,!?:;":
                sleep(d * 5)

        
        if hold:
            sleep(1)

        if stop:
            print()
            input()

        print("\n")

def menu(scroll, full=False):
    clear()
    mixer.music.load("sounds\Glorilad.mp3")
    mixer.music.play(-1)
    
    if full:
        scroll.text(pyfiglet.figlet_format("Draayln's Veil"), colour='blue', fast=True, stop=True) #may need to pip install pyfiglet, im not too sure but if it doesnt work then yes do it
        print("\n" * 2)
    
    menuOptions = ["New", "Save", "Load", "Options"]
    
    while True: # Will have a save/load function hopefully, for now just a title screen.
        scroll.text("New\t=\tNEW GAME", colour='blue')
        scroll.text("Save\t=\tSAVE GAME", colour='blue')
        scroll.text("Load\t=\tLOAD GAME", colour='blue')
        scroll.text("Options\t=\tOPTIONS", colour='blue')
        
        print("TYPE OUT YOUR CHOICE")
        a = input().capitalize()
        
        while a not in menuOptions:
            print("TYPE OUT YOUR CHOICE")
            a = input().capitalize()
    
        if a == "Options":
            option = options(scroll)
            if option == 1:
                scroll.scrollSpeed()
                continue
        
        elif a == "New":

            party = start(scroll)
            mixer.music.fadeout(3000)
            scroll.text("Your journey begins now!", slow=True, sound=True)
            plains = plains_map()

            playMap(plains[1], plains[0], plains[2], party, scroll)

def options(scroll):
    while True:
        try:
            clear()
            scroll.text("----------Options----------")
            options = ["Change Scroll Speed"]
            
            for i in range(len(options)):
                scroll.text(f"{i + 1} = {options[i]}")

            pick = int(input("Setting: "))
            if 0 < pick <= len(options):
                return pick
        except Exception:
            continue

def start(scroll):
    character = classes.Hero()



    while True:
        
        clear()

        scroll.text("Please enter your character's name.")
        name = input()
        if name == "":
            name = "Hero"

        scroll.text(f"Are you sure you want the name '{name}'?")
        if scroll.confirm():
            character.name = name
            scroll.text(f"Your name is {character.name}, the Prince of Legacia", hold=True)
            break
        else:
            continue
    
    party = [character]
    
    return party

def displayCharacters(scroll, Characters, choose=False):
    for i in range(len(Characters)):
        status_indicators = []
        
        if Characters[i].stunned:
            status_indicators.append("(Stn)")

        if Characters[i].poisoned:
            status_indicators.append("(Psn)")

        if Characters[i].bleeding:
            status_indicators.append("(Bld)")
        
        if status_indicators:
            status_indicators = " ".join(status_indicators) + " "
        else:
            status_indicators = ""
        
        if choose:
            for i in range(len(Characters)):
                character = Characters[i]

                if character.hitpoints / character.maxHitpoints < 0.25:
                    col = "red"
                elif character.hitpoints / character.maxHitpoints < 0.5:
                    col = "yellow"
                else:
                    col = "white"
                
                scroll.text(f"{i + 1} = {character.name} {status_indicators} {healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4, small=True)}", colour=col, fast=True)
        else:

            for character in Characters:
                scroll.text(words=f"{status_indicators}{spBar(character.name, character.sp, character.maxSp, character.maxSp)}", colour='green', fast=True)
                
                if character.hitpoints / character.maxHitpoints < 0.25:
                    col = "red"
                elif character.hitpoints / character.maxHitpoints < 0.5:
                    col = "yellow"
                else:
                    col = "white"
                
                scroll.text(f"{' '.join(status_indicators) }{healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4)}", colour=col, fast=True)

def displayEnemies(scroll, aliveEnemies):
    for i in range(len(aliveEnemies)):
        status_indicators = []
        
        if aliveEnemies[i].stunned:
            status_indicators.append("(Stn)")

        if aliveEnemies[i].poisoned:
            status_indicators.append("(Psn)")

        if aliveEnemies[i].bleeding:
            status_indicators.append("(Bld)")


        status_string = " ".join(status_indicators)


        if aliveEnemies[i].hitpoints / aliveEnemies[i].maxHitpoints < 0.25:
            scroll.text(f"{i + 1} = {aliveEnemies[i].name} {status_string}", colour='red')

        elif aliveEnemies[i].hitpoints / aliveEnemies[i].maxHitpoints < 0.5:
            scroll.text(f"{i + 1} = {aliveEnemies[i].name} {status_string}", colour='yellow')

        else:
            scroll.text(f"{i + 1} = {aliveEnemies[i].name} {status_string}")          

def healthBar(name, hitpoints, maxHitpoints, length, small=False):
    name += "'s HP:"
    dashConvert = int(maxHitpoints / length)
    currentDashes = int(hitpoints / dashConvert)
    remaininghitpoints = length - currentDashes

    hitpointsDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remaininghitpoints

    if small:
        return f"|{hitpointsDisplay}{remainingDisplay}|"
    
    return f"{name:<30} {hitpoints}/{maxHitpoints}\t|{hitpointsDisplay}{remainingDisplay}|"

def spBar(name, sp, maxSp, length, small=False):
    name += "'s SP:"
    dashConvert = int(maxSp / length)
    currentDashes = int(sp / dashConvert)
    remainingsp = length - currentDashes

    spDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remainingsp
    
    if small:
        return f"|{spDisplay}{remainingDisplay}|"
    
    return f"{name:<30} {sp}/{maxSp}\t|{spDisplay}{remainingDisplay}|"

def defend(scroll, attacker):
    attacker.defend = True
    scroll.text(f"{attacker.name} defends!", colour="cyan", stop=True)

def attack(scroll, attacker, target):
    scroll.text(f"{attacker.name} attacks {target.name}!")
    damage = max((attacker.attack + attacker.weapon.damage + random.randint(0, attacker.weapon.damageRoll)) - target.defence, 1)
    
    if target.defend:
        damage = damage // 2
        scroll.text(f"{target.name} defends the attack!", colour='blue')

    acc = random.randint(1, 100)

    if attacker.stunned:
        acc = 100  # Force a miss if attacker is stunned
        scroll.text(f"{attacker.name} is stunned.", colour="yellow")

    if acc < attacker.weapon.accuracy:
        # Check for bleed, stun, and poison effects independently
        if attacker.weapon.bleed:
            if random.randint(1, 6) == 1:
                scroll.text(f"{attacker.name} draws blood! {target.name} is bleeding.", colour='red', hold=True)
                target.bleeding = True

        if attacker.weapon.stun:
            if random.randint(1, 3) == 1:
                scroll.text(f"{attacker.name} lands a concussing blow! {target.name} is stunned.", colour='yellow', hold=True)
                target.stunned = True

        if attacker.weapon.poison:
            if random.randint(1, 3) == 1:
                scroll.text(f"{attacker.name} poisons {target.name}!", colour='purple', hold=True)
                if target.poisoned == 0:
                    target.poisoned = 0.01
                else:
                    sleep(0.5)
                    scroll.text(f"But they're already poisoned!", colour='green', hold=True)

        # Check for critical hit
        crit = random.randint(1, 100)
        if crit < attacker.weapon.critChance:
            damage = max(damage * 2, attacker.attack + attacker.weapon.damage + random.randint(0, attacker.weapon.damageRoll))
            target.hitpoints -= damage
            target.hitpoints = max(target.hitpoints, 0)  # Ensure HP doesn't go below 0
            return scroll.text(f"{attacker.name} landed a critical hit!\n{target.name} takes {damage} damage!", colour='red', hold=True)

        # Apply regular damage
        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)  # Ensure HP doesn't go below 0
        return scroll.text(f"{target.name} takes {damage} damage!", colour='red', hold=True)

    else:
        return scroll.text(f"{attacker.name} missed.", colour='blue', hold=True)

def melee(scroll, attacker, aliveEnemies):
    while True:
        try:
            scroll.text("Attack who? (Type the NUMBER of the enemy)." )
            displayEnemies(scroll, aliveEnemies)
            
            scroll.text(f"'q' to return.")
            pick = input()
            if pick == "q":
                return pick
            
            pick = int(pick) - 1

            target = aliveEnemies[pick]
            
            attack(scroll, attacker, target)
            break

        except Exception:
            continue

def skill(scroll, attacker, characterList, aliveEnemies):
    
    while True:
        try:
            scroll.text("Which skill? (Type the NUMBER of the skill)")
            scroll.text(spBar(attacker.name, attacker.sp, attacker.maxSp, attacker.maxSp), colour='green', fast=True)
            skillList = attacker.skills
            
            i = 0
            for skill in skillList:
                i = i + 1
                
                if attacker.sp < skill["spConsumption"]:
                    scroll.text(f"{i} = {skill['name']} ({skill['spConsumption']} SP)", colour="red")
                
                else:
                    scroll.text(f"{i} = {skill['name']} ({skill['spConsumption']} SP)")
            
            scroll.text(f"'q' to return.")
            pick = input()
            if pick == "q":
                return pick
            
            pick = int(pick) - 1
            if pick < 0 or pick >= len(skillList):
                i = 0
                continue
            
            if attacker.sp >= skillList[pick]["spConsumption"]:
                tempSkill = skillList[pick]
                i = 0
            else:
                scroll.text("Not enough SP!", colour='red')
                i = 0
                continue

            if tempSkill["hit"] == "me":
                tempSkill["function"](scroll, attacker)

            elif tempSkill["hit"] == "party":
                scroll.text("Use on who? (Type the NUMBER of the ally)")
                
                displayCharacters(scroll, characterList, choose=True)

                scroll.text(f"'q' to return.")
                pick = input()
                if pick == "q":
                    continue

                pick = int(pick) - 1
                if 0 <= pick < len(characterList):
                    target = characterList[pick]
                    tempSkill["function"](scroll, attacker, target)

            elif tempSkill["hit"] == "enemy":
                scroll.text("Attack who? (Type the NUMBER of the enemy)")
                displayEnemies(scroll, aliveEnemies)
            
                scroll.text(f"'q' to return.")
                pick = input()
                if pick == "q":
                    continue

                pick = int(pick) - 1

                if 0 <= pick < len(aliveEnemies):
                    target = aliveEnemies[pick]
                    tempSkill["function"](scroll, attacker, target)

            break
        except Exception as e:
            scroll.text(f"an error occured: {str(e)}", stop=True)
            continue

def battle(scroll, enemyList=None, characterList=[], tile="."):
    mixer.music.load("sounds\Ambush.mp3")
    mixer.music.play(-1)
    clear()
    battle_experience = 0
    battle_gold = 0
    if enemyList == None:
        enemyList = generateEnemies(tile)

    for i in range(len(enemyList)):
        scroll.text(f"A {enemyList[i].type} approaches!")  # Initial enemy encounter text
        sleep(0.5)
    sleep(1)
    
    taunt_temp = 0

    aliveCharacters = characterList
    aliveEnemies = enemyList
    sort = 0
    while len(aliveCharacters) != 0 and len(aliveEnemies) != 0: #The fight continues until either the list of enemies or the list of characters is empty.
        entities = aliveCharacters + aliveEnemies #Puts every active member of the fight together
        order = list(sorted(entities, key=lambda x: x.agility, reverse=True)) #Uses lambda to sort by sp for whos turn it is
        attacker = order[sort] # order[0] is the highest agility currently

        clear()
        if attacker.bleeding:
            hp = attacker.hitpoints
            attacker.hitpoints = max(0, attacker.hitpoints - int(attacker.maxHitpoints * 0.08) + 1)
            scroll.text(f"{attacker.name} bleeds.\n{attacker.name} takes {hp - attacker.hitpoints} damage!", colour="red")

        if attacker.poisoned:
            hp = attacker.hitpoints
            attacker.hitpoints = max(0, attacker.hitpoints - int((attacker.maxHitpoints * attacker.poisoned) + 1))
            scroll.text(f"The venom attacks {attacker.name}.\n{attacker.name} takes {hp - attacker.hitpoints} damage!", colour="purple")
            attacker.poisoned = min(0.16, attacker.poisoned * 2)
            
        if attacker.stunned:
            scroll.text(f"{attacker.name} is too stunned to move!", colour="yellow")
            sort += 1
            sort = sort % len(entities)
            attacker.stunned = False
            continue
                        
        if attacker.hitpoints == 0:
            entities.remove(attacker)
            if attacker.ally:
                scroll.text(f"{attacker.name} has died!")
                aliveCharacters.remove(attacker)
                sort = sort % len(entities)
                continue
            
            else:
                scroll.text(f"{attacker.name} has died!")
                battle_experience += attacker.experiencePoints
                battle_gold += attacker.gold
                aliveEnemies.remove(attacker) #Remove dead enemies from the list
                sort = sort % len(entities)
                continue

        if attacker.defend:
            scroll.text(f"{attacker.name} lowers their guard.")
            attacker.defend = False

        if attacker in characterList:
            while True:
                displayCharacters(scroll, characterList)
                
                scroll.text(f"It's {attacker.name}'s turn!")
                ################################################### ONLY WAY I CAN MANAGE TO RESET SKILLS IS IN HERE ONCE ITS THEIR TURN
                
                if attacker.taunt:
                    taunt_temp += 1
                    
                    if taunt_temp == 3:
                        attacker.taunt = False
                        scroll.text(f"{attacker.name}'s taunt wears off.")
                
                ################################################### ONLY WAY I CAN MANAGE TO RESET SKILLS IS IN HERE ONCE ITS THEIR TURN
                
                scroll.text(words=f"{attacker.name}: 'a' = Attack | 's' = Skills | 'i' = Item | 'd' = Defend | 'f' = Flee |'?' = Info |", colour="cyan", fast=True)
                
                a = input()

                if a == "a":
                    if melee(scroll, attacker, aliveEnemies) == "q":
                        continue
                    break

                elif a == "f":
                    scroll.text("Escaping...", slow=True, hold=True, sound=True)
                    if random.randint(1, 3) == 1:
                        scroll.text("You got away!", hold=True)
                        clear()
                    
                    else:
                        scroll.text("You fail to escape!", hold=True)
                        break
                
                elif a == "d":
                    defend(scroll, attacker)
                    break
                
                elif a == "s":
                        if len(attacker.skills) == 0:
                            scroll.text("You have no skills!")
                        else:
                            check = False
                            for s in attacker.skills:
                                if attacker.sp >= s["spConsumption"]:
                                    check = True
                            
                            if check:
                                if skill(scroll, attacker, characterList, aliveEnemies) == "q":
                                     continue
                                break
                            else:
                                scroll.text(f"Not enough SP to use any skills!", hold=True)

            for target in aliveEnemies:
                if target.hitpoints == 0:
                    scroll.text(f"{target.name} has died!", hold=True)
                    
                    entities.remove(target)

                    battle_experience += target.experiencePoints
                    battle_gold += target.gold
                    
                    aliveEnemies.remove(target) #Remove dead enemies from the list
                sort = sort % len(entities)
                continue

        else:
            scroll.text(f"It's {attacker.name}'s turn", hold=True)
            target = random.choice(aliveCharacters) #Party is attacked at random

            for character in aliveCharacters:
                if character.taunt:
                    target = character
                    scroll.text(f"The enemy is enraged by {character.name}'s taunt!", hold=True)

            attack(scroll, attacker, target)
            scroll.text(words=f'{healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}', colour="red", fast=True, hold=True) #Displays health bar
            
            if target.hitpoints == 0:
                scroll.text(f"{target.name} has died!", stop=True)
                aliveCharacters.remove(target)
                entities.remove(target)
                sort = sort % len(entities)
                continue
            
        
        sort += 1
        sort = sort % len(entities)
    
    mixer.music.stop()
    if aliveCharacters:

        mixer.music.load("sounds\Victory.mp3")
        mixer.music.play()
        scroll.text("All enemies have been defeated!")
        scroll.text(f"Each Party member receives {battle_experience} XP.")
        scroll.text(f"You gained {battle_gold} Gold.", stop=True)

        characterList[0].gold += battle_gold

        for i in range(len(characterList)):
            c = characterList[i]
            if c.hitpoints == 0:
                c.hitpoints = 1

            c.defend = False
            c.poisoned = False
            c.bleeding = False
            c.stunned = False
            c.taunt = False

            c.experience += battle_experience

            lvl.levelUp(characterList)
        
        clear()
    
    else:
        mixer.music.load("sounds\Determination.mp3")
        mixer.music.play()
        scroll.text("You have been defeated.\n\nGAME OVER", slow=True)
        scroll.text("Return to title screen?")
        if scroll.confirm():
            menu(scroll, full=True)
        else:
            exit()

def generateEnemies(tile):
    
    enemyList = []
    
    choices = [enemy for enemy in enemies.enemyList if tile in enemy.areas]

    power = random.randint(tiles[tile][0], tiles[tile][1])
    
    while len(enemyList) < 6 and power > 3:
        enemy = copy.deepcopy(random.choice(choices))
        enemyList.append(enemy)
        power -= enemy.power
    
    choices = [enemy for enemy in choices if enemy.power < 3]

    while len(enemyList) < 6 and power > 0:
        enemy = copy.deepcopy(random.choice(choices))
        enemyList.append(enemy)
        power -= enemy.power
    
    enemy_count = {}
    
    for i in range(len(enemyList)):
        enemy_type = enemyList[i].type 
        
        if enemy_type in enemy_count:
            enemy_count[enemy_type] += 1
        else:
            enemy_count[enemy_type] = 0
        letter = chr(ord('A') + enemy_count[enemy_type])  
        
        enemyList[i].name = f"{enemyList[i].name} {letter}"
    
    return enemyList

def plains_map():
    plains = map.generateRandomMap(50, 25, ".", 1, (10, 20))    
    plains = map.generateClusters(plains, "^", 3, (40, 80))
    plains = map.generateClusters(plains, "%", 3, (40, 80))
    plains = map.generateRiver(plains)
    #plains = map.generateClusters(plains, "&", 2, (1, 1))
    plains = map.addVillage(plains)
    coords = map.spawn(plains)
    return [coords, plains, "Plains"]

def displayItems(scroll, party):
    clear()
    items = [item for item in party[0].inventory if item.type == "item"]
    scroll.text("----------Items----------", colour='yellow', fast=True)
    
    for i in range(len(items)):
        scroll.text(f"{i + 1} = {items[i].name}")
    
    input()

def equipment(scroll, party):
    clear()
    equipment = [item for item in party[0].inventory if item.type != "item"]
    scroll.text("----------Equipment----------", colour='yellow', fast=True)
    
    for i in range(len(equipment)):
        scroll.text(f"{i + 1} = {equipment[i].name}")
    
    input()

def flush_input(screen):
    # Set the input to non-blocking mode
    screen.nodelay(True)
    
    # Flush all the keys currently in the input buffer
    while screen.getch() != -1:
        pass
    
    # Restore blocking mode after flushing
    screen.nodelay(False)

def init_colors():
    # Check if the terminal supports color
    if curses.has_colors():
        curses.start_color()

        # Initialize color pairs (foreground, background)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # White on black
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Green on black
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Yellow on black
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Blue on black
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)  # Red on black

def curseStart(screen):
    init_colors()

    colour_mapping = {
    "@": curses.color_pair(1),  # Player in white
    ".": curses.color_pair(2),  # Floor in green
    "^": curses.color_pair(3),  # Mountains in yellow
    "~": curses.color_pair(4), #Water in blue
    "!": curses.color_pair(3), #Encounters become red
    "%": curses.color_pair(2), #Forests in green
    "+": curses.color_pair(3),
    "&": curses.color_pair(5),
    "A": curses.color_pair(5),
    "/": curses.color_pair(5),
    "\\": curses.color_pair(5),
    "-": curses.color_pair(5),
    "|": curses.color_pair(5),
    "_": curses.color_pair(5),
    "#": curses.color_pair(3),
    "=": curses.color_pair(3)
    }

    curses.noecho()  # Don't echo key presses
    curses.cbreak()  # React to keys without pressing enter
    screen.keypad(True)  # Enable special keys
    curses.curs_set(0)  # Hide the cursor
    return colour_mapping

def curseEnd(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

def playMap(matrix, player_pos, area, party, scroll=None):

    screen = curses.initscr()
    colour_mapping = curseStart(screen)

    steps = 0    
    mixer.music.load(f"sounds\{area}.mp3")
    mixer.music.play(-1)    
    # Find starting position
    if player_pos == None:
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] == '.':
                    player_pos = (x, y)
                    break

    try:
        while True:

            # Clear screen buffer
            screen.clear()
            x, y = player_pos
            tile = matrix[y][x]

            screen.addstr(1, 1,f" Area: {area} ({x}, {y}) | Gold {party[0].gold}", curses.color_pair(3))
            # Draw top border
            screen.addstr(2, 0,'_' * (len(matrix[0]) * 2 + 2))

            # Draw the map with a border
            for i, row in enumerate(matrix):
                screen.addch(i + 3, 0, '|')  # Left border
                
                for j, char in enumerate(row):
                    colour = colour_mapping.get(char, curses.color_pair(0))
                    if (j, i) == (x, y):
                        screen.addch(i + 3, j * 2 + 1, '@', curses.A_BOLD)  # Player position
                    else:
                        screen.addch(i + 3, j * 2 + 1, ord(char), colour)
                
                screen.addch(i + 3, len(matrix[0]) * 2 + 1, '|')  # Right border

            # Draw bottom border
            screen.addstr(len(matrix) + 3, 0,f"|{'_' * (len(matrix[0]) * 2)}|")  # Bottom border
            screen.addstr(len(matrix) + 5, 1, "w, a, s, d: Move | q: Quit | p: Party | i: Items | e: Equipment | Space: Search | ?: Help")
            screen.addstr(len(matrix) + 6, 1,f"Current tile: {tile}")
            # Refresh the screen
            screen.refresh()
            sleep(.15)
            # Get input
            key = chr(screen.getch())
            if key in ["w", "a", "s", "d"]:
                new_x, new_y = x, y
            
                if key == 'w':
                    new_y = max(0, y - 1)
                elif key == 's':
                    new_y = min(len(matrix) - 1, y + 1)
                elif key == 'a':
                    new_x = max(0, x - 1)
                elif key == 'd':
                    new_x = min(len(matrix[0]) - 1, x + 1)
                       
                tile = matrix[new_y][new_x]    
                # Update position if valid move
                if tile in ['.','^', '%', '|', '#']:
                    player_pos = (new_x, new_y)
                    steps += 1

                    if tile == "|":
                        
                        curseEnd(screen)
                        clear()
                        
                        t.enter(area, party, first=True)
                        steps = 0
                        if matrix[new_y][new_x + 1] != "|":
                            player_pos = (new_x + 1, new_y)
                        else:
                            player_pos = (new_x - 1, new_y)

                        screen = curses.initscr()
                        flush_input(screen)
                        colour_mapping = curseStart(screen)

                    elif tile in ["="]:
                        steps -= 1

                    elif steps > 8 and random.randint(1, 15) == 1:
                        
                        screen.clear()
                        screen.refresh()
                        x, y = player_pos
                        
                        screen.addstr(1, 1,f" Area: {area} ({x}, {y}) | Gold {party[0].gold}", curses.color_pair(3))

                        # Draw top border
                        screen.addstr(2, 0, '_' * (len(matrix[0]) * 2 + 2))  # Top border (without newlines)

                        for i, row in enumerate(matrix):
                            screen.addch(i + 3, 0, '|')  # Left border
                            
                            for j, char in enumerate(row):
                                colour = curses.color_pair(5)
                                if (j, i) == (x, y):
                                    screen.addch(i + 3, j * 2 + 1, '!', curses.A_BLINK)  # Player position
                                else:
                                    screen.addch(i + 3, j * 2 + 1, ord(char), colour)
                            
                            screen.addch(i + 3, len(matrix[0]) * 2 + 1, '|')  # Right border

                        # Draw bottom border
                        screen.addstr(len(matrix) + 3, 0, f"|{'_' * (len(matrix[0]) * 2)}|")  # Bottom border
                        screen.addstr(len(matrix) + 5, 1, "w, a, s, d: Move | q: Quit | p: Party | i: Items | e: Equipment | Space: Search | ?: Help")
                        screen.addstr(len(matrix) + 6, 1,f"Current tile: {tile}")
                        
                        mixer.music.fadeout(100)
                        encounter.play()

                        # Refresh the screen
                        screen.refresh()

                        sleep(1.4)
                        screen.clear()

  
                        flush_input(screen)

                        curseEnd(screen)
                        
                        battle(scroll, None, party, tile)
                        
                        mixer.music.load("sounds\Plains.mp3")
                        mixer.music.play(100, 0, 4000)
                        
                        screen = curses.initscr()
                        colour_mapping = curseStart(screen)

                        flush_input(screen)
                        steps = 0
            else:
                curseEnd(screen)
                clear()
                
                if key == "q":
                    scroll.text("Are you sure you wish to return to the main menu? Progress will NOT BE SAVED")
                    if scroll.confirm():
                        mixer.music.stop()
                        menu(scroll, True)

                elif key == "?":
                    #controls()
                    pass
                
                elif key == "p":
                    displayCharacters(scroll, party)
                    lvl.partyLevels(party)
                    input("Press any key to return")
                elif key == "i":
                    displayItems(scroll, party)
                elif key == "e":
                    equipment(scroll, party)
                    pass                

                screen = curses.initscr()
                colour_mapping = curseStart(screen)
            
    finally:
        # Clean up curses
        curseEnd(screen)

if __name__ == '__main__':
    clear()
    encounter = os.path.join('sounds', 'encounter.mp3')

    encounter = mixer.Sound(encounter)
    
    scroll = TextScroller()
    scroll.scrollSpeed(first=True)
    lvl = levels.Levels(scroll, skills)
    t = town.Town(scroll)

    while True:
        menu(scroll, True)
