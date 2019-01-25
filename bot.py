import discord
from discord.ext import commands
import os

opts = {'command_prefix': commands.when_mentioned_or("?"),
        'description': 'Prywatny bot stworzony przez @Style#1337',
        'pm_help': None,
        'command_not_found': ''}

bot=commands.Bot(**opts)
ext = ['cogs.stars','cogs.mod']

@bot.event
async def on_ready():
    print('Im working')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You"))

@bot.command(hidden=True, name='reload',aliases=['r'])
@commands.is_owner()
async def _reload(ctx, *, module: str):
    'Reloads a module.'
    try:
        bot.unload_extension(f'''cogs.{module}''')
        bot.load_extension(f'''cogs.{module}''')
    except Exception as e:
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        e = discord.Embed(title='Przeładowano moduł', description=f'''`cogs.{module}` został Przeładowany''', color=16098377, timestamp=ctx.message.created_at)
        await ctx.send(embed=e)

if __name__ == '__main__':
    for extension in ext:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Nie udało sie załadować {}\n{}'.format(extension, exc))

bot.run(os.environ["TOKEN"])
