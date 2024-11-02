from pygame import mixer


class Levels(object):

    def __init__(self, scroll, skills) -> None:
        self.skillList = skills
        self.scroll = scroll
        xpLevel = {
            1: 0,
            2: 9,
            3: 24,
            4: 55
        }

        for i in range(5, 10):
            xpLevel[i] = int((xpLevel[i - 1] * 1.7))


        for i in range(10, 20):
            xpLevel[i] = int(xpLevel[i - 1] * 1.3 + 100)

        for i in range(20, 40):
            xpLevel[i] = xpLevel[i - 1] + 4500

        self.xpLevel = xpLevel
        self.partySkills = {
            "Hero": {
                2: None,
                3: "Singe",
                4: None,
                5: "Heal"
            }
        }

    def allLevels(self):

        for k in self.xpLevel.keys():
            print(f"Level {k}: {self.xpLevel[k]}")
    
    def characterLevel(self, character):
        lvl = character.level
        temp = character.name + "'s Level:"
        self.scroll.text(f"{temp} {lvl}")
        self.scroll.text(f"Experience needed for next level: {self.xpLevel[lvl + 1] - character.experience}")
    
    def partyLevels(self, characterList):
        for char in characterList:
            self.characterLevel(char)
    
    def levelUp(self, characterList):
        for i in range(len(characterList)):
            c = characterList[i]

            while c.experience >= self.xpLevel[c.level + 1]:
                c.level += 1
                
                if mixer.music.get_busy():
                    mixer.music.stop()
                
                mixer.music.load("sounds\save.mp3")
                mixer.music.play()
                self.scroll.text(f"{c.name} has reached level {c.level}!", colour='yellow', stop=True)
                
                c.hitpoints = c.maxHitpoints
                c.sp = c.maxSp
                
                skill = self.partySkills[c.type][c.level]
                if skill != None:
                    c.skills.append(self.skillList[skill])
                    self.scroll.text(f"{c.name} has learnt a new skill: {skill}!", colour='yellow', hold=True, stop=True)