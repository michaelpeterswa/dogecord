# michaelpeterwswa
# bot.py

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import toml
from discord import Embed, Game, Status
from discord.ext import commands

secrets = toml.load("../secrets.toml")

bot = commands.Bot(command_prefix="$", description="dogecord")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        activity=Game(name="💎👐 bitch | $doge"), status=Status.dnd
    )

@bot.command(pass_context=True)
async def beep(ctx):
  await ctx.message.channel.send("boop ✅")

@bot.command(pass_context=True)
async def doge(ctx):
  data = get_doge_data()
  if data == -1:
    await ctx.message.channel.send("API failure, nw")
  else:
    doge_quote = data["data"]["DOGE"]["quote"]["USD"]
    doge_price = "${:.6f}".format(doge_quote["price"])
    doge_percent1 = "{:.2f}%".format(doge_quote["percent_change_1h"])
    doge_percent24 = doge_quote["percent_change_24h"]

    if doge_quote["percent_change_1h"] > 0:
      doge_color = 0x25FF5D
    else:
      doge_color = 0xFF4325

    embed = Embed(
        title="🚀 doge report 🚀", color=doge_color
    )
    embed.add_field(name="current price: ", value=doge_price, inline=True)
    embed.add_field(name="percent change (1h): ", value=doge_percent1, inline=True)
    embed.set_footer(text="to the fuckin moon.")
    await ctx.message.channel.send(embed=embed)

def get_doge_data():
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'convert':'USD',
    'symbol' : 'DOGE'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': secrets["cmc"],
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
    return -1

if __name__ == '__main__':
  bot.run(secrets["disc"])
  