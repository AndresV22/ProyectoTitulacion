class Building:
    name = ""
    minerals = 0
    gas = 0
    gameSpeed = 0
    initialEnergy = 0
    maxEnergy = 0
    requirements = []
    unlocks = []
    builds = []

    def __init__(self, name, minerals, gas, gameSpeed, initialEnergy, maxEnergy, requirements, unlocks, builds):
        self.name = name
        self.minerals = minerals
        self.gas = gas
        self.gameSpeed = gameSpeed
        self.initialEnergy = initialEnergy
        self.maxEnergy = maxEnergy
        self.requirements = requirements
        self.unlocks = unlocks
        self.builds = builds

    def info(self):
        return '{} costs {} minerals and {} gas. Unlocks {}'.format(self.name, self.minerals, self.gas, self.unlocks)

    def showNext(self):
        if self.unlocks == []:
            print("END")
        else:
            for building in self.unlocks:
                print(building.name)
                building.showNext()

    def showWhatBuilds(self):
        for unit in self.builds:
            print("- ", unit)
