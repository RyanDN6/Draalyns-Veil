class Skills(object):
    def __init__(self, scroller):
        self.scroll = scroller
        pass

    def taunt(self, attacker, hit="me"):
        sp_consumption = 3
        attacker.sp -= sp_consumption
        attacker.taunt = True
        self.scroll.text(f"{attacker.name} taunts their opponents!\nThe enemies now target {attacker.name}.", stop=True)

    def heal(self, attacker, target, hit="party"):
        sp_consumption = 5
        attacker.sp -= sp_consumption
        hp = target.hitpoints
        target.hitpoints = min(target.hitpoints + target.maxHitpoints // 5, target.maxHitpoints)
        self.scroll.text(f"{attacker.name} emits a healing aura.\n{target.name} heals for {target.hitpoints - hp} HP!")
        self.scroll.text(words=f"{fight.healthBar(target.name, target.hitpoints, target.maxHitpoints, target.maxHitpoints//4)}", colour='green', fast=True, stop=True)

    def senkatto(self, attacker, target, hit="enemy"):
        sp_consumption = 6
        attacker.sp -= sp_consumption
        self.scroll.text(f"{attacker.name} strikes relentlessly!")

        if attacker.sp > 0:
            damage = (attacker.attack + attacker.weapon.damage + random.randint(1, attacker.weapon.damageRoll)) - target.defence
            if target.defend:
                damage //= 2

            if random.randint(1, 2) == 1:
                self.scroll.text(f"{attacker.name} draws blood! {target.name} is bleeding.", colour='red')
                target.bleeding = True
                self.scroll.text(f"{attacker.name} recovers 2 SP!", stop=True)
                attacker.sp += 2

            target.hitpoints -= damage
            target.hitpoints = max(target.hitpoints, 0)
            return self.scroll.text(f"{target.name} takes {damage} damage!", colour='red', stop=True)

    def singe(self, attacker, target, hit="enemy"):
        sp_consumption = 3
        attacker.sp -= sp_consumption
        
        self.scroll.text(f"{attacker.name} conjures a ball of fire and throws it at {target.name}!")
        
        damage = (attacker.magic + 8 + random.randint(1, 6))
        
        if target.defend:
            damage //= 2

        target.hitpoints -= damage
        target.hitpoints = max(target.hitpoints, 0)
        return self.scroll.text(f"{target.name} takes {damage} damage!", colour='red', stop=True)