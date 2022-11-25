import discord
from discord.ext import commands, tasks
from itertools import cycle, islice
import csv
import datetime
import requests
from bs4 import BeautifulSoup
from tabula import read_pdf , convert_into
from model import Models
models = Models()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)

requests.packages.urllib3.disable_warnings()
url = "https://sks.btu.edu.tr/index.php?sid=235"
response = requests.get(url,verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all("a")

i = 0
for link in links:
    if ('.pdf' in link.get('href', [])) and i ==0:
        i += 1
        print(i ,"Adet Dosya Indiriliyor")
        response = requests.get(link.get('href'),verify=False)
        pdf = open("pdf"+str(i)+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        print(i, "Adet Dosya Indirildi")
print("PDF Dosyasi Indirildi")


df = read_pdf("pdf1.pdf", pages='all')[0]
convert_into("pdf1.pdf", "yemekhane.csv", output_format="csv", pages='all')


now = datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
timer = '{}.{}.{}'.format(day, month, year)

z = 0
with open("yemekhane.csv", encoding="windows-1254") as csvfile:
  reader = csv.reader(csvfile)
  status = []
  for row in reader:
    status.append(row)
    z += 1
x = 2
for i in status:
  if status[x][0] != timer:
    x += 1
  else:
    break
y = 1
newList = []
date = []
newList3 = []
for p in range(z - 2):
  y += 1
  date.append(status[y][0])
  row = [
    f" ----Menü için Tıkla---- \n {status[y][2]} \n {status[y][3]} \n {status[y][4]} \n {status[y][5]}"
  ]
  row2 = [status[y][2], status[y][3], status[y][4], status[y][5]]
  row = "".join(row)
  row2 = "\n".join(row2)
  newList.append(row)
  newList3.append(row2)

    
newList2 = newList.copy()
newList, newDate = islice(newList, x - 2, None), islice(date, x - 2, None)
newList, newDate = cycle(newList), cycle(newDate)


newList4 = []
timer2 = 0
for t in newList3:
  if t == '\n\n\n':
    d = newList3[timer2].replace('\n\n\n', 'Haftasonu Yemek Hizmeti Yoktur')
    newList4.append(d)
    timer2 += 1
  else:
    newList4.append(t)
    timer2 += 1

@client.event
async def on_guild_join(guild):
    #print(dir(guild))
    print(str(guild.id), str(guild.name),str(guild.owner),str(guild.owner_id),guild.member_count)
    models.add_server(str(guild.id), str(guild.owner), str(guild.owner_id), str(guild.name), guild.member_count)

@client.event
async def on_guild_remove(guild):
    print(str(guild.id), str(guild.name),str(guild.owner),str(guild.owner_id),guild.member_count)
    models.delete_server(str(guild.id))

@client.event
async def on_ready():
  change_status.start()
  print("Hafize Ana Botu calisiyor ")


@tasks.loop(minutes=60)
async def change_status():
  if datetime.datetime.utcnow().strftime("%H UTC") == ("00 UTC"):
    await client.change_presence(activity=discord.Game(name=next(newList)))


@change_status.before_loop
async def before_change_status():
  await client.change_presence(activity=discord.Game(name=next(newList)))
  print("donguyu baslattim")

    
@client.command()
async def menu(ctx, number="bugununmenusu"):
  if number=="bugununmenusu":
    number = datetime.datetime.now().day
  if (int(number) > 0):
    bn = (date[int(number) - 1] + " Tarihli Günün Menüsü")
    bnm = newList4[int(number) - 1]
    obnm = bn + "\n" + bnm
    await ctx.send(obnm)
  else:
    print(datetime.datetime.now(), "| biri garip bir seyler deniyor")

client.run("TOKEN")
