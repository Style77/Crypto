import discord
from discord.ext import commands
import random
import requests
import asyncio
from itertools import cycle
import os
import praw
import time

start_time = time.time()
bot=commands.Bot(command_prefix='.')
bot.remove_command('help')
bot.colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]
bot.col = int(random.random() * len(bot.colours))
"""statusy"""
url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
response = requests.get(url)
value = response.json()['bpi']['USD']['rate']
url1 = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
response1 = requests.get(url1)
value1 = response1.json()['USD']
url2 = 'https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD'
response2 = requests.get(url2)
value2 = response2.json()['USD']
status=["1BTC = {}USD".format(value),"1ETH = {}USD".format(value1),"1DOGE = {}USD".format(value2)]

reddit = praw.Reddit(client_id=os.environ["client_id"],client_secret=os.environ["client_secret"],user_agent='Crypto')

@bot.command(pass_context=True)
async def uptime():
    seconds = time.time() - start_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    w, d = divmod(d, 7)
    await bot.say(f"Im online: `{int(w)}weeks : {int(d)}days : {int(h)}h : {int(m)}m : {int(s)}s`")

@bot.event
async def on_ready():
    print('-----------')
    print('Ready')
    print('Bot name: '+bot.user.name)
    print('bot ID: '+bot.user.id)
    print('-----------')

@bot.event
async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(50)

@bot.command(pass_context=True,aliases=['leave','quit'])
async def suicide(ctx):
    if message.author.bot:
        return
    else:
        author=ctx.message.author
        await bot.say('Hey, {} You really want to be kicked? Think about it... **YOU HAVE 15sec**'.format(author.mention))
        r=await bot.wait_for_message(author=author,channel=ctx.message.channel,timeout=15)
        if r.content == 'yes':
            msg = await bot.say('***Always in our hearts*** :broken_heart:')
            await bot.add_reaction(msg,'😫')
            await bot.add_reaction(msg,'3⃣')
            await asyncio.sleep(1)
            await bot.remove_reaction(msg, '3⃣',member=bot.user)
            await bot.add_reaction(msg,'2⃣')
            await asyncio.sleep(1)
            await bot.remove_reaction(msg, '2⃣',member=bot.user)
            await bot.add_reaction(msg,'1⃣')
            await asyncio.sleep(1)
            await bot.remove_reaction(msg, '1⃣',member=bot.user)

            await bot.kick(author)
        else:
            await bot.say('xd so why you take my time')
        
@bot.command(pass_context=True)
async def news(ctx):
    if message.author.bot:
        return
    else:    
        sub = reddit.subreddit('CryptoCurrency').new()
        post_to_pick = random.randint(1, 5)
        for i in range(0, post_to_pick):
            submission = next(x for x in sub if not x.stickied)
        picture = submission.url

        e=discord.Embed(title='CryptoCurrency',description=submission.title,color=0xf87c47,timestamp=ctx.message.timestamp)
        e.set_author(name='Reddit',icon_url='https://vignette.wikia.nocookie.net/hayday/images/1/10/Reddit.png/revision/latest?cb=20160713122603')
        e.set_image(url=picture)
        e.set_footer(text=submission.url)
        await bot.say(embed=e)
        #await bot.say(submission.url)

@bot.command(pass_context=True)
async def price(ctx,name=None):
    if message.author.bot:
        return
    else:   
        if not name:
            await bot.say('`.price DASH` - or something')
        else:
            try:
                urlc = f'https://min-api.cryptocompare.com/data/price?fsym={name}&tsyms=USD'
                responsec = requests.get(urlc)
                valuec = responsec.json()['USD']
                await bot.say(f'Price of {name} is {valuec}USD')
            except Exception as e:
                await bot.say('I cant find that currency')

@bot.command(pass_context=True,aliases=['server'])
async def serverinfo(ctx):
     if message.author.bot:
        return
     else:       
        server=ctx.message.server
        nazwy = [role.name for role in server.role_hierarchy]
        value = "\n".join(nazwy)
        servercreated = str(server.created_at).split('.', 1)[0]
        e=discord.Embed(description=server.name,color=bot.colours[bot.col],timestamp=ctx.message.timestamp)
        e.set_author(name=server.name,icon_url=server.icon_url)
        e.set_thumbnail(url=server.icon_url)
        e.add_field(name='Server created at',value=servercreated)
        e.add_field(name='Owner',value=server.owner.mention)
        e.add_field(name='Members',value=server.member_count)
        e.add_field(name='Region',value=server.region)
        e.add_field(name='Default channel',value=server.default_channel)
        e.add_field(name='MFA level:',value=str(server.mfa_level))
        e.add_field(name='AFK time',value=str(server.afk_timeout)+'sek')
        e.add_field(name='AFK channel',value=str(server.afk_channel))
        e.add_field(name='Big? +250members',value=str(server.large))
        e.add_field(name='Hierarchy',value=str(value),inline=True)
        e.set_footer(text='ID: {}'.format(server.id))
        await bot.say(embed=e)            
            
@bot.command(pass_context=True,aliases=['help'])
async def info(ctx):
    if message.author.bot:
        return
    else:        
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        url1 = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
        response1 = requests.get(url1)
        value1 = response1.json()['USD']
        url2 = 'https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD'
        response2 = requests.get(url2)
        value2 = response2.json()['USD']
        e=discord.Embed(title="Select the reaction to get info about currency and price",color=bot.colours[bot.col],timestamp=ctx.message.timestamp)
        e.set_author(name='Crypto')
        e.set_footer(text='Made by: `Style dont mention me ples#9445` | Avatar by: `K*urwaKruci#4055`')
        msg = await bot.say(embed=e)
        await bot.add_reaction(msg,'btc:494145792102105089')
        await bot.add_reaction(msg,'ethereum:494153529653592085')
        await bot.add_reaction(msg,'DOGE:494156739802038273')
        b=await bot.wait_for_reaction(message=msg,user=ctx.message.author)
        #print(b.reaction.emoji)
        if str(b.reaction.emoji) == '<:btc:494145792102105089>':
            e1=discord.Embed(description='Bitcoin (₿) is a cryptocurrency, a form of electronic cash.\nIt is a decentralized digital currency without a central bank or single administrator that can be sent from user to user on the peer-to-peer bitcoin network without the need for intermediaries.\n' ,color=bot.colours[bot.col])
            e1.set_author(name='Bitcoin',icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
            e1.set_footer(text='Price of Bitcoin: 1 BTC = {}'.format(value))
            await bot.edit_message(msg,embed=e1)
            await bot.remove_reaction(msg,'btc:494145792102105089',ctx.message.author)
            await bot.remove_reaction(msg,'btc:494145792102105089',bot.user)
            await bot.remove_reaction(msg,'DOGE:494156739802038273',bot.user)
            await bot.remove_reaction(msg,'ethereum:494153529653592085',bot.user)
        if str(b.reaction.emoji) == '<:ethereum:494153529653592085>':
            e2=discord.Embed(description='Ether is a cryptocurrency whose blockchain is generated by the Ethereum platform.\nEther can be transferred between accounts and used to compensate participant mining nodes for computations performed.\n' ,color=bot.colours[bot.col])
            e2.set_author(name='Ethereum',icon_url='https://s2.coinmarketcap.com/static/img/coins/32x32/1027.png')
            e2.set_footer(text='Price of Ethereum: 1 ETH = {}'.format(value1))
            await bot.edit_message(msg,embed=e2)
            await bot.remove_reaction(msg,'ethereum:494153529653592085',ctx.message.author)
            await bot.remove_reaction(msg,'ethereum:494153529653592085',bot.user)
            await bot.remove_reaction(msg,'DOGE:494156739802038273',bot.user)
            await bot.remove_reaction(msg,'btc:494145792102105089',bot.user)
        if str(b.reaction.emoji) == '<:DOGE:494156739802038273>':
            e3=discord.Embed(description='Dogecoin (symbol: Ð and D) is a cryptocurrency featuring a likeness of the Shiba Inu dog from the "Doge" Internet meme as its logo.\nIntroduced as a "joke currency" on 6 December 2013, Dogecoin quickly developed its own online community and reached a capitalization of US$60 million in January 2014.' ,color=bot.colours[bot.col])
            e3.set_author(name='Dogecoin',icon_url='https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png')
            e3.set_footer(text='Price of Dogecoin: 1 DOGE = {}'.format(value2))
            await bot.edit_message(msg,embed=e3)
            await bot.remove_reaction(msg,'DOGE:494156739802038273',ctx.message.author)
            await bot.remove_reaction(msg,'DOGE:494156739802038273',bot.user)
            await bot.remove_reaction(msg,'ethereum:494153529653592085',bot.user)
            await bot.remove_reaction(msg,'btc:494145792102105089',bot.user)

class Error_handler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error: Exception, ctx: commands.Context):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await bot.send_message(ctx.message.channel, '{} is disabled.'.format(ctx.command))
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed=discord.Embed(title="{} Cant be used in pm's".format(ctx.command))
                await bot.send_message(ctx.message.author, embed=embed)
                return
            except discord.Forbidden:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                embed=discord.Embed(title='Bad argument')
                await bot.send_message(ctx.message.channel, embed=embed)
                return
        
bot.loop.create_task(change_status())
bot.run(os.environ["TOKEN"])
