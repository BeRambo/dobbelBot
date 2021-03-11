import discord
from discord.ext import commands
import os
import asyncio
from classModule import Game
from classModule import Player
from classModule import Score
from classModule import Dice
from classModule import Throw

#variables for the discord bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix= "$", intents=intents)

#variables for the game
game = Game()
worp = Throw()

#other functions
def takeDrawScore(Player):
  return Player.drawScore

@bot.event
async def on_ready():
    print('We have logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    await bot.change_presence(activity=discord.Game(name='1-2-en'))

@bot.command()
async def join(ctx):
  if not game.started:
    player = Player(ctx.author)
    game.addPlayer(player)
    await ctx.send("{} is toegevoegd aan de lijst met spelers!".format(player.name))
    game.showPlayers() #debug option
  else:
    await ctx.send("Er is nog een spel bezig, je kan pas meedoen bij een nieuw spel.")


@bot.command()
async def gooi(ctx):
  if game.checkActive(ctx.author.id): #checks if this is the active player
    worp.shake()
    for dobbelsteen in worp.throwArray: #stuur foto van dobbelsteen
      image = discord.File('img/' + str(dobbelsteen) + '.png')
      await ctx.send(file=image)

    await ctx.send(worp.printThrow())


@bot.command()
async def start(ctx):
  #start phase
  if len(game.participants) == 1:
    await ctx.send('Ge kunt geen spel alleen spelen, zuiplap!')
  elif len(game.participants) == 0:
    await ctx.send('Typ $join om mee te doen aan het spel. Wanneer iedereen klaar is, typ je $start om het spel te starten.')
  else:
    game.start()
    await ctx.send(f"{game.participants[0].name} mag beginnen!")

  #functions for input validation
  def checkGooi(m):
    return m.content == "$gooi" and m.channel == ctx.channel and m.author.id == game.getActivePlayer().discriminator
  def checkGooiEen(m):
    return m.content == "$gooiEen" and m.channel == ctx.channel and m.author.id == game.getActivePlayer(True).discriminator
  def checkAnswer(m):
    msgContent = m.content[0].lower()
    return msgContent == "j" and m.author.id == game.getActivePlayer().discriminator or msgContent == "n" and m.channel == ctx.channel and m.author.id == game.getActivePlayer().discriminator


  while game.started and len(game.participants) >= 1:
    game.newRound()

    for player in game.participants: #elke speler 1x aan de beurt
      player.active = True #starts turn
      mention = '<@'+str(player.discriminator)+'>'
      await ctx.send(mention + " is aan de beurt!")

      if player != game.participants[0]: #geeft highscore weer bij alle spelers, behalve de eerste
        await ctx.send(f"De hoogste score is {game.highScore.printScore()}, door {game.highScore.name} in {game.highScore.tries} tries")

      for i in range(1, game.highScore.tries+1): #max zoveel keer gooien als degene van de highscore
        await ctx.send('Typ $gooi om te gooien.')
        await bot.wait_for("message", check=checkGooi)
        await asyncio.sleep(1)
        await ctx.send('Aantal worpen: ' + str(i))

        score = worp.score #haalt score op bij gooi fuc 
        player.setScore(Score(player.name, player.discriminator, score, i)) #slaat score op in player
        print("Players score: " + str(player.score)) #debug option

        if score == 7: #bij 7 mag je niet opnieuw
            break

        if i < game.highScore.tries: #zonder dit zou je bij de laatste beurt deze vraag ook nog krijgen
          await ctx.send('\n\nWil je opnieuw gooien? (J/N)')
          msg = await bot.wait_for("message", check=checkAnswer) #captures the msg
          msgContent = msg.content.lower()
          #await ctx.send(msgContent) #debug option
          
          if msgContent[0] == "n": #breaks out of for loop (end turn)
            break

      player.active = False #ends turn
      if player == game.participants[0] or player.score > game.highScore.score: #highscore set at 1st player or when score is improved
        game.setHighScore(player)
      

    #gelijkspel phase
    game.checkDraw() #checkt voor gelijkspel na de ronde
    if game.drawPlayers:
      await ctx.send("######################################" )
      await ctx.send(f"Er is een gelijkspel! Deze spelers gooiden allemaal {game.highScore.printScore().lower()}:")
      for player in game.drawPlayers: await ctx.send(player.name)
      await ctx.send("Deze spelers mogen nu allemaal 1 dobbelsteen gooien, de hoogste wint!" )
      await ctx.send("######################################" )

    while len(game.drawPlayers) > 1:
      for player in game.drawPlayers:
        player.active = True
        mention = '<@' + str(player.discriminator) + '>'
        await ctx.send(mention + ' is aan de beurt! Typ $gooiEen om een teerling te werpen.')

        #waits for throwone
        await bot.wait_for("message", check=checkGooiEen)
        drawThrow = Dice().roll() 
        image = discord.File('img/' + str(drawThrow) + '.png')
        await ctx.send(file=image)
        player.drawScore = drawThrow #saves the drawScore in the player (in drawPlayers)
        player.active = False

      game.drawPlayers.sort(key=takeDrawScore, reverse=True) #puts the highest throw first
      game.removeDrawPlayers() #removes every lower score
      
    game.checkWinner()

    #einde van de ronde; speler met hoogste begint, laagste zuipt?
    await ctx.send("Einde van deze ronde, het spel gaat automatisch verder. Typ '$stop' om te stoppen met spelen." )
    await ctx.send("######################################" )
    await ctx.send(f"De winnaar van deze ronde is {game.participants[0].name}, met een worp van {game.highScore.printScore().lower()}!")
    await ctx.send("######################################" )
    await ctx.send(f"En de verliezer van deze ronde is {game.participants[-1].name}, 3 slokken voor u!" )
    await ctx.send("######################################" )

  game.reset()

@bot.command()
async def stop(ctx):
  game.stop()
  await ctx.send("De game wordt gestopt na deze ronde. Yuuw!" )

bot.run(os.getenv('TOKEN'))