import discord
import json
from math import ceil
import asyncio
import base64

intents = discord.Intents().all()
client = discord.Client(intents=intents)

  
with open('config.json') as f:
    config = json.load(f)

with open('guild_config.json') as f:
    guild_config = json.load(f)
    print(f"Loaded guild config: {guild_config}")


channel_id = 1087786338331398204

@client.event
async def on_ready():
    guild = client.guilds[0] # assuming your bot is only in one guild
    print(guild.id)


@client.event
async def on_message(message):
    global channel_id

    if message.author.bot:
        return

    # Delete messages sent in the specified channel that don't start with the command prefix "!"
    if message.channel.id == channel_id and not message.content.startswith('!'):
        await message.delete()
        embed = discord.Embed(
            title="Recoil Generator",
            description="Verwende den Befehl `!recoil` und schreibe dahinter die Zahlen des Recoils deiner M416. Diese Reihenfolge verwenden: Rotpunkt, 2x-Scope, 3x-Scope, 4x-Scope und 6x-Scope\n\nBeispiel: `!recoil 200 185 180 165 155`",
            color=discord.Color.from_rgb(231, 76, 60)
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1077225467721023569/1087812554962767933/IMG_0048.png")
        error_message = await message.channel.send(embed=embed)
        await asyncio.sleep(120)
        await error_message.delete()
        return
  
    if message.content.startswith('!'):
        if not message.content.startswith('!recoil'):
            await message.delete()
            return
        
        if channel_id is None or message.channel.id != channel_id:
            print(f"Ignoring command in channel {message.channel.name} ({message.channel.id}). Expected channel ID: {channel_id}")
            return

        numbers = message.content.split()[1:]
        if len(numbers) != 5:
          await message.delete()
          embed = discord.Embed(
              title="Recoil Generator",
              description="Verwende den Befehl `!recoil` und schreibe dahinter die Zahlen des Recoil deiner M416. Diese Reihenfolge verwenden: Rotpunkt, 2x-Scope, 3x-Scope, 4x-Scope und 6x-Scope\n\nBeispiel: `!recoil 200 185 180 165 155`",
              color=discord.Color.from_rgb(231, 76, 60)
          )
          embed.set_image(url="https://cdn.discordapp.com/attachments/1077225467721023569/1087812554962767933/IMG_0048.png")
          error_message = await message.channel.send(embed=embed)
          await asyncio.sleep(120)
          await error_message.delete()
          return
        
        try:
            numbers = [float(n) for n in numbers]
            if not all(0 <= n <= 238 for n in numbers):
                await message.delete()
                embed = discord.Embed(
                    title="Fehler",
                    description="Bitte gib Zahlen zwischen 0 und 238 ein.",
                    color=discord.Color.from_rgb(231, 76, 60)
                )
                await message.channel.send(embed=embed, delete_after=30)
                return
        except ValueError:
            await message.delete()
            embed = discord.Embed(
                title="Fehler",
                description="Bitte gib gültige Zahlen ein.",
                color=discord.Color.from_rgb(231, 76, 60)
            )
            await message.channel.send(embed=embed, delete_after=30)
            return

        author_mention = message.author.mention
        await message.delete()
        author_message = f"{author_mention}"
        embed = discord.Embed(title='Hier sind deine angepassten Waffeneinstellungen.',color=discord.Color.green())
        for weapon, factors in config.items():
            values = [ceil(n * f) for n, f in zip(numbers, factors)]
            embed.add_field(name=weapon, value=' | '.join(str(v) for v in values), inline=False)
        await message.channel.send(author_message, embed=embed)

    elif message.content.startswith('!channel'):
        if not message.author.guild_permissions.administrator:
            return
        
        channel_name = message.content.split()[1][2:-1]
        channel = discord.utils.get(message.guild.channels, name=channel_name)
        if channel is None:
            return

        channel_id = channel.id
        guild_config[str(message.guild.id)] = channel_id

        with open('guild_config.json', 'w') as f:
            json.dump(guild_config, f)

client.run('bot_token')
