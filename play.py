import os, sys, copy, platform, classes, pyfiglet, winsound, playsound, enemies, random, map, curses
from time import sleep
#For appending letters to enemies of same type in battle
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

#Difficulty of encounters based on tile of battle
tiles = {
    '.': (1, 2),
    '^': (3, 5),
    '%': (2, 3),
    '~': (1, 3)
}

def clear():
    os.system('cls')

def taunt(scroll, attacker, hit="me", sp_consumption=3):
    attacker.sp -= sp_consumption
    attacker.taunt = True
    scroll.text(f"{attacker.name} taunts their opponents!\nThe enemies now target {attacker.name}.", stop=True)

def heal(scroll, attacker, target, hit="party", sp_consumption=5):
    attacker.sp -= sp_consumption
    hp = target.hitpoints
    target.hitpoints = min(target.hitpoints + target.maxHitpoints // 5, target.maxHitpoints)
    scroll.text(f"{attacker.name} emits a healing aura.\n{target.name} heals for {target.hitpoints - hp} HP!")
    scroll.text(words=f"{healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}", colour='green', fast=True, stop=True)

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
            scroll.text(f"{attacker.name} recovers 2 SP!", stop=True)
            attacker.sp += 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        return scroll.text(f"{target.name} takes {damage} damage!", colour='red', stop=True)

def singe(scroll, attacker, target, hit="enemy",sp_consumption=3):
    attacker.sp -= sp_consumption
    
    scroll.text(f"{attacker.name} conjures a ball of fire and throws it at {target.name}!")
    
    damage = (attacker.magic + 8 + random.randint(1, 6))
    
    if target.defend:
        damage //= 2

    target.hitpoints -= damage
    target.hitpoints = max(target.hitpoints, 0)
    return scroll.text(f"{target.name} takes {damage} damage!", colour='red', stop=True)

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

    def text(self, words="", colour='white', slow=False, fast=False, stop=False, hold=False):
        
        support = self.support
        d = self.delay
        
        if slow:
            d = max(0.1, d * 3)
        elif fast:
            d = 0
        
        for char in words:
            
            sleep(d)  # Use the class's delay attribute
            
            if support:
                print(f"\033[1;{colours[colour]};40m{char}", end="", flush=True) 
            else:
                print(char, end="", flush=True)
            
            if char in ".,!?:;":
                sleep(d * 5)
        
        if hold:
            sleep(1)

        if stop:
            print()
            input()

        print("\n")

def menu(scroll, full=False):
    
    if full:
        scroll.text(pyfiglet.figlet_format("Draayln's Veil"), colour='blue', fast=True, stop=True) #may need to pip install pyfiglet, im not too sure but if it doesnt work then yes do it
        print("\n" * 4)
    
    menuOptions = ["New", "Save", "Load", "Options"]
    
    while True: # Will have a save/load function hopefully, for now just a title screen.

        scroll.text("New\t= NEW GAME", colour='blue')
        scroll.text("Save\t= SAVE GAME", colour='blue')
        scroll.text("Load\t= LOAD GAME", colour='blue')
        scroll.text("Options\t= OPTIONS", colour='blue')
        
        print("TYPE OUT YOUR CHOICE")
        a = input().capitalize()
        
        while a not in menuOptions:
            print("TYPE OUT YOUR CHOICE")
            a = input().capitalize()
    
        return a

def options(scroll):
    while True:
        
        clear()

        scroll.text("----------Options----------")
        scroll.text("1 = Change Scroll Speed")
        return input("Setting: ")

def start(scroll):
    character = classes.Hero()
    character.skills = [skills["Singe"], skills["Heal"]]



    while True:
        
        clear()

        scroll.text("Please enter your character's name.")
        name = input()
        if name == "":
            name = "Hero"
        else:
            scroll.text(f"Are you sure you want the name '{name}'?")
        if scroll.confirm():
            character.name = name
            scroll.text(f"Your name is {character.name}, the Prince of Legacia", hold=True)
            break
        else:
            continue
    
    party = [character]
    
    return party

def displayCharacters(scroll, Characters):
    for i in range(len(Characters)):
        status_indicators = []
        
        if Characters[i].stunned:
            status_indicators.append("(Stn)")

        if Characters[i].poisoned:
            status_indicators.append("(Psn)")

        if Characters[i].bleeding:
            status_indicators.append("(Bld)")

        for character in Characters:
            scroll.text(words=f"{" ". join(status_indicators) }{spBar(character.name, character.sp, character.maxSp, character.maxSp)}", colour='green', fast=True)
            
            if character.hitpoints / character.maxHitpoints < 0.25:
                col = "red"
            elif character.hitpoints / character.maxHitpoints < 0.5:
                col = "yellow"
            else:
                col = "white"
            
            scroll.text(f"{" ". join(status_indicators) }{healthBar(character.name, character.hitpoints, character.maxHitpoints, character.maxHitpoints//4)}", colour=col, fast=True)

def displayEnemies(scroll, aliveEnemies):
    while True:
        try:
            scroll.text("Attack who? (Type the NUMBER of the enemy)")
            
            i = 0
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
                
                i += 1
            
            break
        
        except Exception:
            continue    

def healthBar(name, hitpoints, maxHitpoints, length):
    name += "'s HP:"
    dashConvert = int(maxHitpoints / length)
    currentDashes = int(hitpoints / dashConvert)
    remaininghitpoints = length - currentDashes

    hitpointsDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remaininghitpoints
    
    return f"{name:<30} {hitpoints}/{maxHitpoints}\t|{hitpointsDisplay}{remainingDisplay}|"

def spBar(name, sp, maxSp, length):
    name += "'s SP:"
    dashConvert = int(maxSp / length)
    currentDashes = int(sp / dashConvert)
    remainingsp = length - currentDashes

    spDisplay = '█' * currentDashes
    remainingDisplay = ' ' * remainingsp
    
    return f"{name:<30} {sp}/{maxSp}\t|{spDisplay}{remainingDisplay}|"

def defend(scroll, attacker):
    attacker.defend = True
    scroll.text(f"{attacker.name} defends!", colour="cyan", stop=True)

def attack(scroll, attacker, target):
    scroll.text(f"{attacker.name} attacks {target.name}!")
    damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
    
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
            damage = damage * 2
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
            displayEnemies(scroll, aliveEnemies)
            
            pick = int(input()) - 1
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
                
                if attacker.sp >= skill["spConsumption"]:
                    scroll.text(f"{i} = {skill["name"]} ({skill["spConsumption"]} SP)", colour="red")
                
                else:
                    scroll.text(f"{i} = {skill["name"]} ({skill["spConsumption"]} SP)")
            
            pick = int(input()) - 1
            if pick < 0 or pick >= len(skillList):
                continue

            if attacker.sp >= skill["spConsumption"]:
                tempSkill = skillList[pick]
            else:
                scroll.text("Not enough SP!", colour='red')
                continue

            if tempSkill["hit"] == "me":
                tempSkill["function"](scroll, attacker)

            elif tempSkill["hit"] == "party":
                scroll.text("Use on who? (Type the NUMBER of the ally)")
                
                displayCharacters(scroll, characterList)
                pick = int(input()) - 1
                if 0 <= pick < len(characterList):
                    target = characterList[pick]
                    tempSkill["function"](scroll, attacker, target)

            elif tempSkill["hit"] == "enemy":
                displayEnemies(scroll, aliveEnemies)
            
                pick = int(input()) - 1
                if 0 <= pick < len(aliveEnemies):
                    target = aliveEnemies[pick]
                    tempSkill["function"](scroll, attacker, target)
            break

        except Exception as e:
            scroll.text(f"an error occured: {str(e)}", stop=True)
            continue

def battle(scroll, enemyList=None, characterList=[], tile="."):
    
    clear()
    winsound.PlaySound("sounds/Battle.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
    battle_experience = 0
    battle_gold = 0
    if enemyList == None:
        enemyList = generateEnemies(tile)

    for i in range(len(enemyList)):
        scroll.text(f"A {enemyList[i].type} approaches!")  # Initial enemy encounter text
    
    sleep(1)

    taunt_temp = 0

    aliveCharacters = characterList
    aliveEnemies = enemyList
    sort = 0
    while len(aliveCharacters) != 0 and len(aliveEnemies) != 0: #The fight continues until either the list of enemies or the list of characters is empty.
        entities = aliveCharacters + aliveEnemies #Puts every active member of the fight together
        order = list(sorted(entities, key=lambda x: x.agility, reverse=True)) #Uses lambda to sort by sp for whos turn it is
        attacker = order[sort] # order[-1] is the highest sp currently

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
            
            displayCharacters(scroll, characterList)
            
            scroll.text(f"It's {attacker.name}'s turn!")
            ################################################### ONLY WAY I CAN MANAGE TO RESET SKILLS IS IN HERE ONCE ITS THEIR TURN
            
            if attacker.taunt:
                taunt_temp += 1
                
                if taunt_temp == 3:
                    attacker.taunt = False
                    scroll.text(f"{attacker.name}'s taunt wears off.")
            
            ################################################### ONLY WAY I CAN MANAGE TO RESET SKILLS IS IN HERE ONCE ITS THEIR TURN
            
            scroll.text(words=f"{attacker.name}: Enter = Melee | 's' = Skills | 'i' = Item | 'd' = Defend | 'f' = Flee |'?' = Info |", colour="cyan", fast=True)
            
            a = input()

            if a == "":
                melee(scroll, attacker, aliveEnemies)

            elif a == "f":
                scroll.text("Escaping...", slow=True, hold=True)
                if random.randint(1, 3) == 1:
                    scroll.text("You got away!", hold=True)
                    setattr(aliveCharacters[i], "hitpoints", aliveCharacters[i].hitpoints)
                    clear()
                
                else:
                    scroll.text("You fail to escape!", hold=True)

                continue
            
            elif a == "d":
                defend(scroll, attacker)
            
            elif a == "s":
                    skill(scroll, attacker, characterList, aliveEnemies)

            for target in aliveEnemies:
                if target.hitpoints == 0:
                    scroll.text(f"{target.name} has died!")
                    
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
            scroll.text(words=f'{healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}', colour="red", fast=True, stop=True) #Displays health bar
            
            if target.hitpoints == 0:
                scroll.text(f"{target.name} has died!", stop=True)
                aliveCharacters.remove(target)
                entities.remove(target)
                sort = sort % len(entities)
                continue
            
        
        sort += 1
        sort = sort % len(entities)
    
    if aliveCharacters:
        scroll.text("All enemies have been defeated!")
        scroll.text(f"Each Party member receives {battle_experience} XP.")
        scroll.text(f"You gained {battle_gold} Gold.", stop=True)

        
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
        
        clear()
    
    else:
        scroll.text("You have been defeated.\n\nGAME OVER", slow=True)
        exit()

def generateEnemies(tile):
    
    enemyList = []
    
    choices = [enemy for enemy in enemies.enemyList if tile in enemy.areas]

    power = random.randint(tiles[tile][0], tiles[tile][1]) + 2
    
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
    plains = map.generateClusters(plains, "&", 2, (1, 1))
    plains = map.addVillage(plains)
    coords = map.spawn(plains)
    return [coords, plains, "plains"]
    
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

def playMap(matrix, player_pos, area, party, scroll=None):
    """
    Play map using curses for smooth screen updates.
    """
    # Initialize curses
    screen = curses.initscr()
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
    "_": curses.color_pair(5)
    }

    curses.noecho()  # Don't echo key presses
    curses.cbreak()  # React to keys without pressing enter
    screen.keypad(True)  # Enable special keys
    curses.curs_set(0)  # Hide the cursor
    
    steps = 0    
    
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
            
            # Draw top border
            screen.addstr(0, 0, '_' * (len(matrix[0]) * 2 + 2))  # Top border (without newlines)

            # Draw the map with a border
            x, y = player_pos
            for i, row in enumerate(matrix):
                screen.addch(i + 1, 0, '|')  # Left border
                
                for j, char in enumerate(row):
                    colour = colour_mapping.get(char, curses.color_pair(0))
                    if (j, i) == (x, y):
                        screen.addch(i + 1, j * 2 + 1, '@')  # Player position
                    else:
                        screen.addch(i + 1, j * 2 + 1, ord(char), colour)
                
                screen.addch(i + 1, len(matrix[0]) * 2 + 1, '|')  # Right border

            # Draw bottom border
            screen.addstr(len(matrix) + 1, 0, '_' * (len(matrix[0]) * 2 + 2))  # Bottom border

            # Refresh the screen
            screen.refresh()
            
            # Get input
            key = screen.getch()
            new_x, new_y = x, y
            
            if key == ord('q'):
                break
            elif key == ord('w'):
                new_y = max(0, y - 1)
            elif key == ord('s'):
                new_y = min(len(matrix) - 1, y + 1)
            elif key == ord('a'):
                new_x = max(0, x - 1)
            elif key == ord('d'):
                new_x = min(len(matrix[0]) - 1, x + 1)
                
            # Update position if valid move
            if matrix[new_y][new_x] in ['.','^', '%', '|', '~']:
                player_pos = (new_x, new_y)
                steps += 1

                if matrix[new_y][new_x] == "|":
                    #town(area)
                    pass

                elif steps > 8 and random.randint(1, 15) == 1:
                    
                    x, y = player_pos
                                # Draw top border
                    screen.addstr(0, 0, '_' * (len(matrix[0]) * 2 + 2))  # Top border (without newlines)

                    for i, row in enumerate(matrix):
                        screen.addch(i + 1, 0, '|')  # Left border
                        
                        for j, char in enumerate(row):
                            colour = curses.color_pair(5)
                            if (j, i) == (x, y):
                                screen.addch(i + 1, j * 2 + 1, '!')  # Player position
                            else:
                                screen.addch(i + 1, j * 2 + 1, ord(char), colour)
                        
                        screen.addch(i + 1, len(matrix[0]) * 2 + 1, '|')  # Right border

                    # Draw bottom border
                    screen.addstr(len(matrix) + 1, 0, '_' * (len(matrix[0]) * 2 + 2))  # Bottom border

                    # Refresh the screen
                    screen.refresh()

                    sleep(1)
                    screen.clear()

                    tile = matrix[new_y][new_x]
                    flush_input(screen)

                    curses.nocbreak()
                    screen.keypad(False)
                    curses.echo()
                    curses.endwin()
                    
                    battle(scroll, None, party, tile)
                    
                    screen = curses.initscr()
                    curses.noecho()  # Don't echo key presses
                    curses.cbreak()  # React to keys without pressing enter
                    screen.keypad(True)  # Enable special keys
                    curses.curs_set(0)  # Hide the cursor
                    flush_input(screen)
                    steps = 0
            
    finally:
        # Clean up curses
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    
    clear()
    scroll = TextScroller()
    scroll.scrollSpeed(first=True)

    while True:
        choice = menu(scroll, full=True)
        if choice == "Options":
            option = options(scroll)
            if option == "1":
                scroll.scrollSpeed()
                continue
        
        elif choice == "New":
            party = start(scroll)
            scroll.text("Your journey begins now!", slow=True)
            plains = plains_map()

            playMap(plains[1], plains[0], plains[2], party, scroll)