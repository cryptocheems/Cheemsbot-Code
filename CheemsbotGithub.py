#imports
import os
import discord
import json
import requests
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
#end of imports
#loading up the json
with open("airdrop.json") as SaveSetup:
    dictOn = json.load(SaveSetup)
#bad boy this isnt for you...
token = "<where the token should be>"

#selenium setup for honeyswap
url = "https://info.honeyswap.org/token/0xeaf7b3376173df8bc0c22ad6126943cc8353c1ee"
driver = webdriver.Chrome('C:\\Users\\jjsap\\Desktop\\cheemsbot\\chromedriver.exe')
driver.get(url)

#takes the price from honeyswap. did it the hard way, cause why not
def grabPrice():

    global Priceva
    Priceva = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div[3]").text
    print(Priceva)


    driver.refresh()









#setting the prefix
bot = commands.Bot(command_prefix="Cheems-")


#price command
@bot.command(

help="Tells you price of cheems in USD",
brief="What it said before"

)
async def price(ctx):
    grabPrice()
    await ctx.channel.send(f"The current price of Cheemscoin is {Priceva}")


#Profit command
@bot.command(

help="Tells you your current profit",
brief="Takes(amount of cheems) and multiplies by price"

)
async def profit(ctx, arg):
    grabPrice()

    priceva1 = Priceva[1:5]

    await ctx.channel.send(int(arg) * float(priceva1) )
#registration This POS also took forever
@bot.command(
help="Registers you for the database",
brief="Puts you in a json file, yo"
)
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
#tipping this POS took so long
@bot.command(

help="Tip a friend!",
brief="Ping your friend to retrieve their wallet address!"
)
async def tip(ctx,  member: discord.Member):
    memberPull = "@" + str(member)
    registerCheck = memberPull in dictOn


    if registerCheck == True:
        await ctx.channel.send(dictOn[memberPull])
    else:
        await ctx.channel.send(f"{member.mention} is not registered. Please register using the Cheems-register command followed by your wallet address. ")





#putting price in the status
@bot.event
async def on_ready():
    grabPrice()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{Priceva}"))
    print("Bot is ready!")




#bot running
bot.run(token)
