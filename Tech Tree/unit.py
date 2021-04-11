class Unit:
    code = 0
    name = ""
    minerals = 0
    gas = 0
    gameSpeed: int = 0
    supply = 0
    unlockedOn = 0  # Se utiliza la id del edificio
    builtOn = 0
    maxQty = 0

    def __init__(self, code, name, minerals, gas, gameSpeed, supply, unlockedOn, builtOn, maxQty):
        self.code = code
        self.name = name
        self.minerals = minerals
        self.gas = gas
        self.gameSpeed = gameSpeed
        self.supply = supply
        self.unlockedOn = unlockedOn
        self.builtOn = builtOn
        self.maxQty = maxQty
