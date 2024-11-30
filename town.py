import os, weapons, armours
from pygame import mixer
from time import sleep
from play import itemsList

class Town(object):

    def __init__(self, scroll):

        self.scroll = scroll
        self.names = {
            "Plains": "Legacia"
        }

        self.areaWeapons = {
            "Plains": ["Sword", "Greatsword"]
        }

        self.areaArmour = {
            "Plains": ["Plank", "Cloth Bandana", "Padded Shirt"]
        }

        self.areaItems = {
            "Plains": ["Holy Water", "Health Potion"]
        }

    def enter(self, area, characterList, first=False, quest=False):
        
        os.system('cls')
        
        dialogue = {
            "Plains": {
                False: "Welcome back Your Highness, I trust your journey was safe. What can we do for you?",
                True: "We expected nothing less from you Your Royalty. Please, allow us to assist you in any way."
            }
        }
        
        if first:
            self.scroll.text(f"Entering {self.names[area]}...", slow=True)

            mixer.music.fadeout(500)
            mixer.music.load(f"sounds\{self.names[area]}.mp3")
            mixer.music.play(-1, 0, 1500)

            self.scroll.text(dialogue[area][quest])


        else:
            self.scroll.text("Where to next?")
        
        options = {
            "s": "shop",
            "c": "church",
            "i": "inn",
            "t": "talk",
            "q": "leave"
        }

        for option in options.keys():
            self.scroll.text(f"{option} = {options[option].capitalize()}", fast=True)
        
        a = input()

        while a not in options:
            a = input()

        getattr(self, options[a])(area, characterList)

    def shop(self, area, characterList):
        shopText = {
            "Plains": "Welcome your Highness, what would you like to buy?"
        }

        while True:
            os.system('cls')
            self.scroll.text(shopText[area])
            self.scroll.text("w = Weapons")
            self.scroll.text("a = Armour")
            self.scroll.text("i = Item")
            self.scroll.text("q = Leave Shop")
            a = input().lower()

            if a == "q":
                self.scroll.text("Please do come back again!", stop=True)
                break
            
            if a == "w":
                self.scroll.text("----------Weapons----------", colour='yellow', fast=True)
                for i in range(len(self.areaWeapons[area])):
                    weapon = weapons.weaponsList[self.areaWeapons[area][i]]
                    self.scroll.text(f"{i + 1} = {weapon.name} -> {weapon.cost} Gold", fast=True)

                self.scroll.text("Type the number of the weapon to view more.\nType 'q' to go back.")
                
                pick = input()
                if pick == "q":
                    continue
                
                else:
                    try:
                        pick = int(pick) - 1
                        if 0 <= pick < len(self.areaWeapons[area]):
                            weapon = weapons.weaponsList[self.areaWeapons[area][pick]]
                            cost = weapon.cost
                            item = weapon
                            self.scroll.text(f"Weapon: {weapon.name}\nAttack: {weapon.damage} + d{weapon.damageRoll}\n{"Two Handed" if weapon.twoHanded else "One Handed"}\nAccuracy: {weapon.accuracy}%\nCritical: {weapon.critChance}%\nUsed by: {" ,".join(weapon.users)}\nCost: {weapon.cost} Gold", stop=True)
                        else:
                            continue
                    except Exception:
                        continue
                    
            elif a == "a":
                self.scroll.text("----------Armour----------", colour='yellow', fast=True)

                for i in range(len(self.areaArmour[area])):
                    armour = armours.armourList[self.areaArmour[area][i]]
                    self.scroll.text(f"{i + 1} = {armour.name} -> {armour.cost}", fast=True)

                self.scroll.text("Type the number of the weapon to view more.\nType 'q' to go back.")
                pick = input()
                if pick == "q":
                    continue
            
                else:
                    try:
                        pick = int(pick) - 1
                        if 0 <= pick < len(self.areaArmour[area]):
                            armour = armours.armourList[self.areaArmour[area][pick]]
                            cost = armour.cost
                            item = armour
                            self.scroll.text(f"Type: {armour.type}\nName: {armour.name}\nDefence: {armour.defence}\nUsed by: {" ,".join(armour.users)}\nCost: {armour.cost} Gold", stop=True)
                        else:
                            continue
                    except Exception:
                        continue

            elif a == "i":
                self.scroll.text("----------Item----------", colour='yellow', fast=True)
                for i in range(len(self.areaItems[area])):
                    item = itemsList[self.areaItems[area][i]]
                    self.scroll.text(f"{i + 1} = {item.name} -> {item.cost}", fast=True)
                self.scroll.text("Type the number of the item to view more.\nType 'q' to go back.")
                pick = input()
                if pick == "q":
                    continue
            
                else:
                    try:
                        pick = int(pick) - 1
                        if 0 <= pick < len(self.areaItems[area]):
                            item = itemsList[self.areaItems[area][pick]]
                            cost = item.cost
                            self.scroll.text(f"Name: {item.name}\nCost: {item.cost} Gold", stop=True)
                        else:
                            continue
                    except Exception:
                        continue
                    
            else:
                continue
            
            gold = characterList[0].gold

            self.scroll.text(f"You have {gold} Gold.\nDo you want to purchase this item for {cost} Gold?")

            if self.scroll.confirm():
                
                if gold < cost:
                    self.scroll.text("Not enough Gold!", stop=True)
                    continue

                else:
                    gold -= cost
                    if item.count > 0:
                        characterList[0].inventory.append(item)
                        self.scroll.text(f"The {item.name} has been added to your inventory. Gold: {gold}", stop=True)
                        item.count = 1
                    else:
                        self.scroll.text(f"The {item.name} has been added to your inventory. Gold: {gold}", stop=True)
                        item.count += 1
                    characterList[0].gold = gold
        
        self.enter(area, characterList)

    def inn(self, area, characterList):
        
        os.system('cls')

        innPrice = {
            "Plains": 2,
        }

        innText = {
            "Plains": "Hello your Highness, are you staying for the night? Two gold a bed please."
        }
        
        gold = characterList[0].gold
        
        cost = innPrice[area] * len(characterList)
        self.scroll.text(innText[area])
        self.scroll.text(f"You have {gold} Gold.\nPrice for one night: {cost} Gold")

        if self.scroll.confirm():
            
            if gold < cost:
                self.scroll.text("Not enough Gold!", stop=True)

            else:
                
                gold -= cost
                for i in range(len(characterList)):
                    characterList[i].hitpoints = characterList[i].maxHitpoints
                    characterList[i].sp = characterList[i].maxSp
                
                self.scroll.text("Resting...", slow=True, hold=True, sound=True)
                self.scroll.text(f"All memebers of {characterList[0].name}'s party have had their HP and SP restored!", hold=True)
        
        self.scroll.text("Thank you for visiting, please do come back again!", stop=True)
        characterList[0].gold = gold
        self.enter(area, characterList)
    

    def leave(self, area, characterList):
        self.scroll.text(f"Leaving {self.names[area]}...", slow=True, hold=True)
        mixer.music.fadeout(500)
        mixer.music.load(f"sounds\{area}.mp3")
        mixer.music.play(-1, 0, 500)

