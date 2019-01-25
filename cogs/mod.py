import discord
from discord.ext import commands
import asyncio

class mod():
    def __init__(self,bot):
        self.bot=bot
        self.bansays=["**{}** został wysłany na wakacje",
                    "Młotek sprawiedliwości uderzył tym razem w **{}**",
                    "**{}** rozpłynął się w powietrzu"]

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,reason="Brak powodu"):
        if not member:
            return await ctx.send('Kogo?')
        await ctx.send(random.choice(bansays).format(member))
        await member.send(f"zostałeś zbanowany na `{ctx.guild.name}`.\nZa `{reason}`.\nAby odwołać się od bana napisz do {ctx.author.mention}.")
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member=None,*,reason="Brak powodu"):
        if not member:
            return await ctx.send('Kogo?')
        await ctx.send(random.choice(bansays))
        await member.send(f"zostałeś kicknięty z `{ctx.guild.name}`.\nZa `{reason}`")
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_any_role("Admin","Mod", "Helper")
    async def mute(self,ctx,member:discord.Member=None,time:int=10,*,reason='Brak powodu'):
        if not member:
            return await ctx.send('Kogo?')
        role=discord.utils.get(ctx.guild.roles,name="Muted")
        await member.add_roles(role)
        await ctx.send(f"Drodzy państwo **{member}** został wyciszony, wszyscy świętują.")
        await member.send(f"zostałeś wyciszony na `{ctx.guild.name}`.\nZa `{reason}`.\nNa czas **{time}**")
        time=time*60
        await asyncio.sleep(time)
        await member.remove_roles(role)
        await ctx.send(f"**{member}** został odciszony")
        await member.send(f'Kara wyciszenia na `{ctx.guild.name}` skończyła się. Miłej dalszej rozmowy.')

    @commands.command()
    @commands.has_any_role("Admin","Mod", "Helper")
    async def unmute(self,ctx,member:discord.Member):
        role=discord.utils.get(ctx.guild.roles,name="Muted")
        if role in ctx.author.roles:
            await member.remove_roles(role)
            await ctx.send(f"**{member}** został odciszony")
            await member.send(f'Kara wyciszenia na `{ctx.guild.name}` została zdjęta przez {ctx.author}. Miłej dalszej rozmowy.\nps. ja bym za to podziękował :wink:')
        else:
            await ctx.send(f'{member} nie jest wyciszony.')

def setup(bot):
    bot.add_cog(mod(bot))
