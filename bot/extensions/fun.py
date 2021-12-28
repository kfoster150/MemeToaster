import hikari
import lightbulb
import logging
import os, random
from io import BytesIO

from bot import Bot
from bot.pic import render

inputImageDir = './data/images/input'
categories = os.listdir(inputImageDir)
categories.sort()

plugin = lightbulb.Plugin("Functions")

@plugin.command
@lightbulb.command(name = "stats", description = "Show stats about the MemeToaster", aliases = ("stats",), guilds = [833477250841837598])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_stats(ctx: lightbulb.Context) -> None:

    # Create list of categories with number of files
    cats_list = []
    num_list = []
    for c in categories:
        num_pics = len(os.listdir(os.path.join(inputImageDir, c)))
        pics = str(num_pics) + ' pictures'
        cats_list.append((c, pics))
        num_list.append(num_pics)

    num_cats = len(categories)

    # Create embed object
    embed = hikari.Embed(color = 0xFF0000)

    embed.add_field(name = 'Number of categories', value = str(num_cats))
    embed.add_field(name = 'Total number of pictures', value = str(sum(num_list)))
    embed.add_field(name = '\u200b', value = "Number of pictures per category:", inline = False)

    for name, value in cats_list:
        embed.add_field(name = name, value = value, inline = False)

    # send embed object
    await ctx.respond(embed = embed)


@plugin.command
@lightbulb.option(name = "message", description = "message to send", type = str, default = "still testing")
@lightbulb.option(name = "category", description = "picture category", type = str, default = "test")
@lightbulb.command(name = "meme", description = "Do a meme.", aliases = ("pic","emote",), guilds = [833477250841837598])
@lightbulb.implements(lightbulb.SlashCommand)
async def command_meme(ctx: lightbulb.Context) -> None:
    message = ctx.options.message
    category = ctx.options.category.lower()
    
    if len(message) > 126:
        await ctx.respond("""
It's a meme, not your master's thesis. Your caption has to be 125 characters or less.""")
    
    else:
        categoryPath = os.path.join(inputImageDir, category)

        if not category in categories:
            await ctx.respond(f"""
Sorry, I don't have any pictures for '{category}'
Use toast.help or toast.stats for a list of categories
""")

        else:
            await ctx.respond("Toasting meme...")

            images = os.listdir(categoryPath)
            imageChoice = random.choice(images)
            imagePath = os.path.join(categoryPath, imageChoice)

            channel = ctx.get_channel()
 
            with BytesIO() as imageBinary:
                render(imagePath, message).save(imageBinary, 'PNG')

                imageBinary.seek(0)
                await channel.send(imageBinary)

            await ctx.edit_last_response("Toasting meme... DING")


def load(bot: Bot):
    bot.add_plugin(plugin)

def unload(bot: Bot):
    bot.remove_plugin(plugin)
