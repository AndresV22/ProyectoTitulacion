import building


class TechTree:
    buildings = []

    def __init__(self):
        templarArchives = building.Building("templar archives", 150, 200, 36, 0, 0, [
                                            "twilight council", "pylon"], [], [])
        darkShrine = building.Building("dark shrine", 150, 150, 71, 0, 0, [
            "twilight council", "pylon"], [], [])
        fleetBeacon = building.Building("fleet beacon", 300, 200, 43, 0, 0, [
                                        "stargate", "pylon"], [], ["tempest", "carrier", "mothership"])
        roboticsBay = building.Building("robotics bay", 150, 150, 46, 0, 0, [
                                        "robotics facility", "pylon"], [], ["colossus", "disruptor"])
        shieldBattery = building.Building("shield battery", 100, 0, 29, 100, 100, [
            "cybernetics core", "pylon"], [], [])
        twilightCouncil = building.Building("twilight council", 150, 100, 36, 0, 0, [
                                            "cybernetics core", "pylon"], ["templar archives", "dark shrine"], [])
        stargate = building.Building("stargate", 150, 150, 43, 0, 0, [
            "cybernetics core", "pylon"], ["fleet beacon"], ["phoenix", "oracle", "void ray"])
        roboticsFacility = building.Building("robotics facility", 150, 100, 46, 0, 0, [
            "cybernetics core", "pylon"], ["robotics bay"], ["observer", "warp prism", "immortal"])
        ciberneticsCore = building.Building("cibernetics core", 150, 0, 36, 0, 0, ["gateway", "pylon"], [
                                            "shield battery", "twilight council", "stargate", "robotics facility"], [])
        photonCannon = building.Building(
            "photon cannon", 150, 0, 29, 0, 0, [], [], [])
        nexus = building.Building("nexus", 400, 0, 71, 50, 200, [], [
            "gateway", "forge"], ["probe", "mothership"])
        gateway = building.Building("gateway", 150, 0, 46, 50, 200, ["nexus", "pylon"], ["cybernetics core"], [
            "zealot", "stalker", "sentry", "adept", "high templar", "dark templar"])
        forge = building.Building("forge", 150, 0, 32, 0, 0, [
            "nexus", "pylon"], ["photon cannon"], [])
        assimilator = building.Building(
            "assimilator", 75, 0, 21, 0, 0, [], [], [])
        pylon = building.Building("pylon", 100, 0, 18, 0, 0, [], [], [])

        self.buildings.append(nexus)
        self.buildings.append(assimilator)
        self.buildings.append(pylon)
        self.buildings.append(gateway)
        self.buildings.append(forge)
        self.buildings.append(ciberneticsCore)
        self.buildings.append(photonCannon)
        self.buildings.append(shieldBattery)
        self.buildings.append(twilightCouncil)
        self.buildings.append(stargate)
        self.buildings.append(roboticsFacility)
        self.buildings.append(templarArchives)
        self.buildings.append(darkShrine)
        self.buildings.append(fleetBeacon)
        self.buildings.append(roboticsBay)

    def showTree(self):
        for building in self.buildings:
            print(building.name)

    def addBuilding(self, building):
        self.buildings.append(building)

    def findBuildingByName(self, name):
        for building in self.buildings:
            if building.name == name:
                return building
