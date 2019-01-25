import discord
from discord.ext import commands

class stars():
    def __init__(self,bot):
        self.bot=bot

    async def have_starboard(self,payload):
        guild=self.bot.get_guild(payload.guild_id)
        channel = discord.utils.get(guild.text_channels, name='⭐| Starboard')
        if channel:
            return channel
        else:
            return guild.get_channel(payload.channel_id)

    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⭐":
            if payload.user_id == self.bot.user.id:
                return
            channel = await stars.have_starboard(self, payload)
            channeltoget=self.bot.get_channel(payload.channel_id)
            msg=await channeltoget.get_message(id=payload.message_id)
            if payload.user_id == msg.author.id:
                return
            if msg.author.id == self.bot.user.id:
                return
            gradient = random.choice([16744448, 16777088])
            emotka = random.choice([':dizzy:', ':sparkles:', ':sparkling_heart:', ':star2:'])
            e = discord.Embed(description='{}\n'.format(msg.content), color=gradient, timestamp=msg.created_at)
            if msg.attachments:
                e.set_image(url=msg.attachments[0].url)
            e.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
            msgg = await channel.send(f'{emotka} {channeltoget.mention} ID: {msg.id}',embed=e)
            await msgg.add_reaction('⭐')

def setup(bot):
    bot.add_cog(stars(bot))
