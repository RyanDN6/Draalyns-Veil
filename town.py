import os

class Town(object):

    def __init__(self, scroll):

        self.scroll = scroll
        self.names = {
            "Plains": "Legacia"
        }
    
    def enter(self, area, characterList, first=False, quest=False):
        
        os.system('cls')
        
        dialogue = {
            "Plains": "Welcome back Your Highness, I trust your journey was safe. What can we do for you?"
        }
        
        if first:
            self.scroll.text(dialogue[area])
        else:
            self.scroll.text("Where to next?")
        
        options = {
            "s": "shop",
            "c": "church",
            "i": "inn",
            "t": "talk",
            "l": "leave"
        }

        for option in options.keys():
            self.scroll.text(f"{option} = {options[option].capitalize()}", fast=True)
        
        a = input()

        while a not in options:
            a = input().capitalize()

        getattr(self, options[a])(area, characterList)



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
                self.scroll.text("Not enough Gold!")

            else:
                
                gold -= cost
                for i in range(len(characterList)):
                    characterList[i].hitpoints = characterList[i].maxHitpoints
                    characterList[i].sp = characterList[i].maxSp
                
                self.scroll.text("Resting...", slow=True, hold=True, sound=True)
                self.scroll.text(f"All memebers of {characterList[0].name}'s party have had their HP and SP restored!", stop=True)
        
        self.scroll.text("Thank you for visiting, please do come back again!", stop=True)

        self.enter(area, characterList)
    

    def leave(self, area, characterList):
        self.scroll.text(f"Leaving {self.names[area]}...", slow=True, hold=True)
