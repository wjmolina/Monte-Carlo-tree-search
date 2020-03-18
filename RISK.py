class Country:
    def __init__(self):
        self._owner=None
        self._neighbors=set()
    @staticmethod
    def MakeNeighbors(*countries):
        for i in range(len(countries)-1):
            for j in range(i+1,len(countries)):
                countries[i]._neighbors.add(countries[j])
                countries[j]._neighbors.add(countries[i])
class Continent:
    def __init__(self,bonusUnitsAward,*countries):
        self._bonusUnitsAward=bonusUnitsAward
        self._countries=set()
        self.AddCountries(*countries)
    def AddCountries(self,*countries):
        for country in countries:
            self._countries.add(country)
class World:
    def __init__(self,*continents):
        self._continents=set()
        self.AddContinents(*continents)
    def AddContinents(self,*continents):
        for continent in continents:
            self._continents.add(continent)
class Player:
    def __init__(self):
        self._bonusUnits=0
class Game:
    def __init__(self,world):
        self._world=world
        self._player1=Player()
        self._player2=Player()
        self._currentPlayer=self._player1
        self._currentTurn=0
    def DoTurn(self):
        if self._currentTurn==0:
            self._currentPlayer._bonusUnits+=5
            for continent in self._world._continents:
                self._currentPlayer._bonusUnits+=continent._bonusUnitsAward if all([country._owner==self._currentPlayer for country in continent._countries]) else 0

# First Continent
country01=Country()
country02=Country()
country03=Country()
country04=Country()
country05=Country()
country06=Country()
country07=Country()
Country.MakeNeighbors(country01,country02,country03)
Country.MakeNeighbors(country02,country03,country04)
Country.MakeNeighbors(country03,country04,country05)
Country.MakeNeighbors(country04,country05,country06)
Country.MakeNeighbors(country05,country06,country07)
continent01=Continent(8,country01,country02,country03,country04,country05,country06,country07)
# Second Continent
country08=Country()
country09=Country()
country10=Country()
Country.MakeNeighbors(country08,country09,country10)
continent02=Continent(4,country08,country09,country10)
# Third Continent
country11=Country()
country12=Country()
country13=Country()
Country.MakeNeighbors(country11,country12,country13)
continent03=Continent(4,country11,country12,country13)
# Intercontinental Connections
Country.MakeNeighbors(country01,country03,country09)
Country.MakeNeighbors(country05,country07,country12)
Country.MakeNeighbors(country10,country11)
# World
world01=World(continent01,continent02,continent03)
# Game
game01=Game(world01)

# Tests
for continent in world01._continents:
    for country in continent._countries:
        country._owner=game01._player1
game01.DoTurn()
print(game01._currentPlayer._bonusUnits)