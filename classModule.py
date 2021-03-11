import random
import copy

class Player:
  def __init__(self, author):
    self.name = author.name
    self.discriminator = author.id
    self.score = 0
    self.tries = 0
    self.drawScore = 0
    self.active = False

  def setScore(self, Score):
    self.score = Score.score
    self.tries = Score.tries


class Score:
    def __init__(self, name='' , discriminator='', score = 0, tries = 3):
        self.name = name
        self.discriminator = discriminator
        self.score = score
        self.tries = tries
    
    def setScore(self, Player):
        self.name = Player.name
        self.discriminator = Player.discriminator
        self.score = Player.score
        self.tries = Player.tries

    def resetScore(self):
      self = self.__init__()

    def printScore(self):
      if self.score in range(294, 301):
        if self.score == 300:
          repl = '3 apen, kut'
        elif self.score == 299:
          repl = 'Soixant neuf'
        else:
          zandScore = 300 - self.score
          repl = 'Zand van ' + str(zandScore)
      elif self.score == 7: repl = '7, adje kut!'
      else: repl = self.score
      return str(repl)
      

class Game:
  def __init__(self):
    self.highScore = Score()
    self.participants = []
    self.started = False
    self.roundsPlayed = 0
    self.drawPlayers = []
  
  def addPlayer(self, Player):
    self.participants.append(Player)

  def showPlayers(self):
    for p in self.participants: print(f"{p.name}, {p.discriminator}\n")

  def start(self):
    self.started = True
    randomInt = random.randint(0, len(self.participants)-1)
    self.rotatePlayers(randomInt) #chooses a random startplayer, and puts it first in the list

  def stop(self):
    self.started = False

  def retrievePosition(self, idToFind):
    for i, p in enumerate(self.participants): #finds the position in participants, based on id
      if p.discriminator == idToFind:
        return i

  def getPlayer(self, id):
    playerPos = self.retrievePosition(id) #get the position of the player in the participants array
    return self.participants[playerPos]

  def getActivePlayer(self, drawGame = False): #returns the active player, std from participants. if true, taken from drawPlayers
    if drawGame:
      li = self.drawPlayers
    else:
      li = self.participants

    for player in li:
      if player.active:
        return player

  def checkActive(self, id):
    playerObject = self.getPlayer(id)
    if playerObject.active:
      return True
    else: return False

  def rotatePlayers(self, n):
    for i in range(0, n):
      self.participants.append(self.participants.pop(0))

  def newRound(self):
    for p in self.participants:
      p.score = 0
      p.tries = 0
    self.roundsPlayed += 1
    self.highScore.resetScore()
    self.drawPlayers = []

  def reset(self):
    self = self.__init__()

  def setHighScore(self, Player):
    if self.highScore.name != '': #keeps the tries if the score is improved
      Player.tries = copy.copy(self.highScore.tries)
    self.highScore.setScore(Player)

  def checkDraw(self): #checks if someone has the same score as the highscore
    for player in self.participants:
      if player.score == self.highScore.score and player.name != self.highScore.name:
        self.drawPlayers.append(player)

    if self.drawPlayers: #adds original winner to drawPlayers
      posOrigWinner = self.retrievePosition(self.highScore.discriminator)
      self.drawPlayers.append(self.participants[posOrigWinner]) 

  def checkWinner(self):
    if not self.drawPlayers: #if no drawgame, winner is in highScore
      id = self.highScore.discriminator
    else:
      id = self.drawPlayers[0].discriminator

    winnerPos = self.retrievePosition(id)
    self.rotatePlayers(winnerPos)

  def removeDrawPlayers(self): #removes all players with a lower draw score then the highest
    highestThrow = self.drawPlayers[0].drawScore
    for player in self.drawPlayers:
      if player.drawScore < highestThrow:
        self.drawPlayers.remove(player)


class Dice:
  def __init__(self, sides = 6):
    self.sides = sides

  def roll(self):
    return random.randint(1, self.sides)


class Throw:
  '''
  stores the throw in an array, diceThrow
  countThrow counts the throw, stored in self.score
  printThrow prints the throw, returns it directly
  '''
  def __init__(self):
    self.score = 0
    self.throwArray = []
    self.shake()
    self.countThrow()

  def shake(self):
    self.throwArray = [Dice().roll(), Dice().roll(), Dice().roll()]
    self.countThrow()

  def countThrow(self):
    self.score = 0
    throw = self.throwArray
    if throw[0] == throw[1] and throw[1] == throw[2]: #checkt voor zand
      if throw[0] == 1:
        self.score = 300 #zand van 1 = 300
      else:
        self.score = 300 - throw[0] #2 = 298, 3 = 297, 4=296, 5=295, 6=294
                
    else:
      for dice in throw:
        if dice == 1:
          self.score += 100

        elif dice == 6:
          self.score += 60

        else: self.score += dice

        if self.score == 69: self.score = 299

  def printThrow(self):
    if self.score in range(294, 301):
      if self.score == 300:
        return '3 apen, kut'
      elif self.score == 299:
        return 'Soixant neuf'
      else:
        zandScore = 300 - self.score
        return 'Zand van ' + str(zandScore)
    elif self.score == 7: return '7, adje kut!'
    else: return self.score 