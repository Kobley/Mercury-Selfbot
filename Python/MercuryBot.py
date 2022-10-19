import discord,time,io,aiohttp,asyncio,json,os,random,nekos,pyfiglet
import requests as req
import pyperclip as pc
from colorama import Fore, Style
from itertools import islice
from console.utils import set_title
from discord.ext import commands

with open("./config.json") as f:
    config = json.load(f)
    prefix = config['Settings']['Prefix']
    token = config['Settings']['Token']
    sniper = "Disabled"
    nitro_sniper = config['Settings']['nitro_sniper']
    if nitro_sniper.find("true") != -1:
        sniper = "Active"
    else:
        sniper = "Disabled"
    XRapidAPI_Key = config['Settings']['RapidAPI-Key']

MercuryBot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=True)

#Events

@MercuryBot.event
async def on_ready():
    username = f"{MercuryBot.user.name}#{MercuryBot.user.discriminator}"
    ver = "101822"
    print(f"> Authenticated as {username}. Ready!")
    sleep(1.5)
    set_title(f"Mercury SelfBot | {username} | Version: {ver}")
    load(0.01, 1, 0.0625, username)

#Commands

@MercuryBot.command()
async def GenMeme(ctx, args1, args2, args3 = ""):
    text = args2.replace("_"," ")
    text2 = args3.replace("_"," ")
    logText = f"Top Text: {text} Bottom Text: {text2}"
    log("MemeGen", logText)
    GenerateMeme(args1, text, text2)
    await ctx.message.edit(content=pc.paste())

@MercuryBot.command()
async def MemeIDS(ctx):
    log("Meme ID List", "")
    dict = {1: "`368228430` : `Megamind 'no bitches' meme`", 
            2: "`124822590` : `car drifting right road sign`",
            3: "`217743513` : `UNO Draw 25 Cards`",
            4: "`188390779` : `Woman Yelling At Confused Cat`",
            5: "`155067746` : `Surprised Pikachu`",
            6: "`8072285` : `Doge`",
            7: "`178591752` : `Tuxedo Winnie The Pooh`",
            8: "`80707627` : `Sad Pablo Escobar`",
            9: "`405658` : `Grumpy Cat`",
            10: "`196652226` : `Spongebob Ight Imma Head Out`",
            11: "`12403754` : `Bad Pun Dog`",}
    await ctx.message.delete()
    await ctx.send(dict)

@MercuryBot.command()
async def ping(ctx):
    log("Ping", "")
    await ctx.message.edit(content=f"Pong! {round(MercuryBot.latency * 1000)}ms")

@MercuryBot.command(aliases=['hentai'])
async def nsfw(ctx, *, searchTerm: str): 
    log("Nsfw", f"Search Term: {searchTerm}")
    await ctx.message.delete()
    possible = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
        'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
        'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
        'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
        'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
        'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
        'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
        ]

    if searchTerm in possible:
        await ctx.send(nekos.img(searchTerm))
        return
    else: 
        await ctx.send(f"Invalid search term. Please use one of the following:{possible}")
        return

@MercuryBot.command()
async def owoify(ctx, *, text: str):
    log("owoify", text)
    await ctx.message.delete()
    await ctx.send(nekos.owoify(text))
    return

@MercuryBot.command(aliases=['figlet'])
async def ascii(ctx, *, text: str):
    log("Ascii", text)
    await ctx.message.delete()
    await ctx.send(f'```{pyfiglet.figlet_format(text)}```')

@MercuryBot.command(aliases=['geolocate', 'dox'])
async def geoIP(ctx, args1):
    ip = args1;
    log("GeoLocate IP", f"IP: {ip}")
    url = f"https://ip-geo-location.p.rapidapi.com/ip/{ip}"
    querystring = {"format":"json"}
    headers = {
        "X-RapidAPI-Host": "ip-geo-location.p.rapidapi.com",
        "X-RapidAPI-Key": XRapidAPI_Key
    }
    data = req.get(url, headers=headers, params=querystring).json()
    the_json = {
        "IP": data["ip"],
        "Country": data["country"]["name"],
        "City": data["city"]["name"],
        "Region": data["area"]["name"],
        "Latitude": data["location"]["latitude"],
        "Longitude": data["location"]["longitude"]
    }
    finalJson = json.dumps(the_json, indent=4, sort_keys=True, ensure_ascii=False).replace("'", '"')
    await ctx.message.delete()
    await ctx.send(content=f'''```json\n{finalJson}```''')

@MercuryBot.command(aliases=['pfp', 'avatar'])
async def av(ctx, user: discord.Member):
    await ctx.message.delete()
    format = "gif"
    # user = user or ctx.author
    if user.is_avatar_animated() != True:
        format = "png"
    avatar = user.avatar_url_as(format = format if format != "gif" else None)
    async with aiohttp.ClientSession() as session:
        async with session.get(str(avatar)) as resp:
            image = await resp.read()
    with io.BytesIO(image) as file:
        await ctx.send(file = discord.File(file, f"Avatar.{format}"))

@MercuryBot.command()
async def backupServer(ctx):
    await ctx.message.delete()
    await MercuryBot.create_guild(f'backup-{ctx.guild.name}')
    await asyncio.sleep(4)
    for g in MercuryBot.guilds:
        if f'backup-{ctx.guild.name}' in g.name:
            for c in g.channels:
                await c.delete()
            for cate in ctx.guild.categories:
                x = await g.create_category(f"{cate.name}")
                for chann in cate.channels:
                    if isinstance(chann, discord.VoiceChannel):
                        await x.create_voice_channel(f"{chann}")
                    if isinstance(chann, discord.TextChannel):
                        await x.create_text_channel(f"{chann}")
    try:
        await g.edit(icon=ctx.guild.icon_url)
    except:
        pass

@MercuryBot.command(aliases=['eval'])
async def math(ctx, *, equation):
    await ctx.message.delete()
    await ctx.send(f'```{eval(equation)}```')

#Functions

sleep = lambda t: time.sleep(t)

slice_ = lambda n, iterable: list(islice(iterable, n))

log = lambda t, arg: print(f"Used Command: {t} | Arguments: {arg}")

clear = lambda: os.system('cls')

randomInt = lambda l, h: random.randint(l,h)

def switch(boolean: bool):
    boolean = not boolean

def GenerateMeme(id, text, text2):
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':"lowlife_",
        'password':"tx42FSShfsRbLKY",
        'template_id':id,
        'text0':text,
        'text1':text2,
    }
    response = req.post(URL,params=params).json()
    pc.copy(response['data']['url'])

def randomIP():
	ip = ".".join(map(str, (randomInt(0,255)for _ in range(4))))
	return ip

def Start(t, name):
    print(f"                                               ╔═══════════════════════╗")
    print(f"                                              ╔╝        Kobley's       ╚╗")    
    print(f"                                              ║  ╔╦╗╔═╗╦═╗╔═╗╦ ╦╦═╗╦ ╦  ║")
    print(f"                                              ║  ║║║║╣ ╠╦╝║  ║ ║╠╦╝╚╦╝  ║")
    print(f"                                              ║  ╩ ╩╚═╝╩╚═╚═╝╚═╝╩╚═ ╩   ║")
    print(f"                                              ╚╗        SelfBot        ╔╝")
    print(f"                                               ╚═══════════════════════╝")
    print(f"")
    print(f"                                          ╔════════════════════════════════╗")
    print(f"                                         ╔╝ Use The Help Command To Get    ╚╗")
    print(f"                                         ║  Started!                        ║")
    print(f"                                         ║                                  ║")
    print(f"                                         ║  Prefix: {prefix}                       ║")
    print(f"                                         ║  Name: {name}               ║")
    if sniper == "Active": print(f"                                         ╚╗ Nitro Sniper: {Fore.GREEN}{Style.BRIGHT}{sniper}{Fore.RESET}{Style.RESET_ALL}         ╔╝") 
    else: print(f"                                         ╚╗ Nitro Sniper: {Fore.RED}{Style.BRIGHT}{sniper}{Fore.RESET}{Style.RESET_ALL}         ╔╝")
    print(f"                                          ╚════════════════════════════════╝")
    print(f"")
    print(f"")

def getFuniText():
    lol = random.randrange(1, 10)
    if lol == 1:
        return "loading"
    elif lol == 2:
        return "BLM"
    elif lol == 3:
        return "what are you looking at?"
    elif lol == 4:
        return "meow"
    elif lol == 5:
        return "ඞ sus? ඞ"
    elif lol == 6:
        return "( ͡° ͜ʖ ͡°)"
    elif lol == 7:
        return "lmao"
    elif lol == 8:
        return "pacolegion"
    elif lol == 9:
        return "quoifeur"
    elif lol == 10:
        return "feur"

def progressBar(interval):
    funi = getFuniText()
    loading = f"{funi}: [----------]"
    for i in range(101):
        sleep(interval)
        print("\r"+loading+" %d%%" % i)
        if i == 10 or i == 20 or i == 30 or i == 40 or i == 50 or i == 60 or i == 70 or i == 80 or i == 90 or i == 100:
            loading = loading.replace("-","=",1)
        print()

def load(Barinterval, time2load, menuTimer, name):
    clear()
    progressBar(Barinterval)
    sleep(1)
    clear()
    sleep(time2load)
    if(menuTimer != 0):
        Start(menuTimer, name)
    else:
        Start(0.0001, name)

MercuryBot.run(token, bot=False)