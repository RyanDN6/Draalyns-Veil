class Armour:
    def __init__(self, type, name, defence=0, users=None, cost=0):
        self.type = type
        self.name = name
        self.defence = defence

        if users == None:
            self.users = []
        else:
            self.users = users

        self.cost = cost

armourList = {
    "Cloth Bandana": Armour(name="Cloth Bandana", type="Head", defence=2, users=["Hero"], cost=25),
    "Padded Shirt": Armour(name="Padded Shirt", type="Body", defence=3, users=["Hero"], cost=40),
    "Plank": Armour(name="Plank", type="Shield", defence=2, users=["Hero"], cost=20)
}