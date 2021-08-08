import discord
import json
from discord.ext import commands, tasks

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import random
from os import getenv
from dotenv import load_dotenv


load_dotenv()

transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/1hive/honeyswap-v2")
client = Client(transport=transport)
query = gql(
    """
    query {
        token(id:"0xeaf7b3376173df8bc0c22ad6126943cc8353c1ee"){
            derivedETH
        }
    }
"""
)


# loading up the json
with open("airdrop.json") as SaveSetup:
    dictOn = json.load(SaveSetup)

TOKEN = getenv("TOKEN")

# setting the prefix
bot = commands.Bot(command_prefix="Cheems-")


# gets the current price on honeyswap
async def grabPrice():
    return (await client.execute_async(query))["token"]["derivedETH"][0:5]


# price command
@bot.command(help="Tells you price of cheems in USD", brief="What it said before")
async def price(ctx):
    price = await grabPrice()
    await ctx.channel.send(f"The current price of Cheemscoin is ${price}")


# Profit command
@bot.command(
    help="Tells you your current profit", brief="Takes(amount of cheems) and multiplies by price"
)
async def profit(ctx, arg):
    price = await grabPrice()
    await ctx.channel.send(float(arg) * float(price))


# registration This POS also took forever
@bot.command(help="Registers you for the database", brief="Puts you in a json file, yo")
async def register(ctx, arg):
    nh = "@" + ctx.author.name + "#" + ctx.author.discriminator
    address = arg
    addressCheck = "0x" in arg
    if addressCheck == False:
        print(nh)
        await ctx.channel.send("Your request failed, Please try again")
    else:
        with open("airdrop.json", "w") as Save:
            dictOn[nh] = address
            json.dump(dictOn, Save)
        await ctx.channel.send("You have now been added to our database!")


# tipping this POS took so long
@bot.command(help="Tip a friend!", brief="Ping your friend to retrieve their wallet address!")
async def tip(ctx, member: discord.Member):
    memberPull = "@" + str(member)
    registerCheck = memberPull in dictOn

    if registerCheck == True:
        await ctx.channel.send(dictOn[memberPull])
    else:
        await ctx.channel.send(
            f"{member.mention} is not registered. Please register using the Cheems-register command followed by your wallet address. "
        )


# find another persons balance!
@bot.command(help="Pull someone elses balance!", brief="see the dough")
async def bal(ctx, member: discord.Member):
    findBal = "@" + str(member)
    walletCheck = findBal in dictOn
    if walletCheck == True:
        await ctx.channel.send(
            "https://blockscout.com/xdai/mainnet/address/" + dictOn[findBal] + "/tokens"
        )
    else:
        await ctx.channel.send(
            "That person is not registered to our database. Please use Cheems-register to be added to our database!"
        )


CBT_PHRASES = [
    "I am goimg to spamnk your ballms",
    "Kimcks you imn ballsm",
    "Timckles your uremthra",
    "snimp snimp :scissors:",
    "Squeemzes your comck",
    "Parmtakes in bosnian emthic cleamsing",
]
# fuck you all. i hate every one of you
@bot.command(help="comck and ballm tormture", brief="sugma")
async def cbt(ctx):
    cbtphrase = random.choice(CBT_PHRASES)
    await ctx.channel.send(cbtphrase)


# tells someone to shut up
@bot.command(help="tell someone to shut up", brief="same as previous")
async def shut(ctx, member):
    await ctx.channel.send(f"Shut the fuck up {member}")


# putting price in the status
@bot.event
async def on_ready():
    changeStatus.start()
    print("Bot is ready!")


# change the price in the status every 30 mins
@tasks.loop(minutes=30)
async def changeStatus():
    price = await grabPrice()
    print(price)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"${price}")
    )


# bot running
bot.run(TOKEN)
