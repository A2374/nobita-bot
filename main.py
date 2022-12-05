import os
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import qrcode
import datetime
import matchs

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
plataforms = ('Twitch', 'Youtube', 'Trovo', 'Tiktok')

@client.event
async def on_ready():
    print('Bot ready!')
    await client.tree.sync()
    change_status.start()

# Commands
@client.command()
async def info(ctx):
    embed = discord.Embed(title='Rules', description='The rules are basic', color=discord.Color.blue())
    embed.set_author(name='kat simmonds', icon_url='https://pbs.twimg.com/profile_images/1518799750753046529/x5CA1JC7_400x400.jpg', url='https://twitter.com/xkatsimmonds')
    await ctx.send(embed=embed)
@client.command()
async def test(ctx):
    view = View()

    for match in matchs.today:
        if (match['date'] == str(datetime.date.today())):
            async def button_callback(interaction, response = match['image']):
                if response == 'None': response = 'https://thumbs.gfycat.com/CalculatingFloweryCopperbutterfly-max-1mb.gif'
                await interaction.response.send_message(response)

            button = Button(label=match['title'], style=discord.ButtonStyle.blurple)
            button.callback = button_callback

            view.add_item(button)

    await ctx.send(embed=discord.Embed(title='Today\'s matches', color=discord.Color.green()), view=view)

# Slash commands
@client.tree.command(name='announcement', description='Create an announcement')
async def announcement(interaction: discord.Interaction, title: str, description: str, thumbnail: str):
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
    embed.set_image(url=thumbnail)
    await interaction.response.send_message(embed=embed)
@client.tree.command(name='qr', description='Generate a QR code')
async def generator_qr_code(interaction: discord.Interaction, data: str):
    img = qrcode.make(data)
    img.save('qr.png')
    embed = discord.Embed(title='QR generator', description='Convert: {0}'.format(data), color=discord.Color.purple())
    file = discord.File('./qr.png', filename='qr.png')
    embed.set_image(url='attachment://qr.png')
    await interaction.response.send_message(file=file, embed=embed)
    file.close()
    os.remove('qr.png')

@tasks.loop(seconds=600)
async def change_status():
    bot_status = random.choice(plataforms)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=bot_status))

client.run(TOKEN)