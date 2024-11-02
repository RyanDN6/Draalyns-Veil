class Item:
    def __init__(self, name, cost=0):
        self.name = name
        self.cost = cost
        self.type = "item"

itemsList = {
    "Holy Water": Item(name="Holy Water", cost=10)
}