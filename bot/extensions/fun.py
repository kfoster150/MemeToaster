import hikari
import lightbulb
import os, random, re
from io import BytesIO
import logging

from bot import Bot
from bot.pic import render

current_guilds = [833477250841837598, # Tutorial
                  328380613411209218, # Orbiters United
                  ]

inputImageDir = './data/images/input'
categories = os.listdir(inputImageDir)
categories.sort()

plugin = lightbulb.Plugin("Functions")

@plugin.command
@lightbulb.command(name = "stats", description = "Show stats about the MemeToaster", guilds = current_guilds)
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
@lightbulb.option(name = "caption", description = "caption to attach", type = str, default = "",
                    modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name = "category", description = "picture category", type = str, required = True)
@lightbulb.command(name = "meme", description = "Put a picture category and caption in the toaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_meme(ctx: lightbulb.Context) -> None:
    caption = ctx.options.caption
    category = ctx.options.category.lower()
    
    if len(caption) > 125:
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
                render(imagePath, caption).save(imageBinary, 'PNG')

                imageBinary.seek(0)
                await channel.send(imageBinary)

            await ctx.edit_last_response("Toasting meme... DING")


# @plugin.command
# @lightbulb.option(name = "category_caption", description = "picture & category", type = str, required = True, 
#                 modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
# @lightbulb.command(name = "meme", description = "Put a picture category and caption in the toaster", guilds = current_guilds)
# @lightbulb.implements(lightbulb.PrefixCommand)
# async def command_prefix_meme(ctx: lightbulb.Context) -> None:
#     logging.info(ctx.options.category_caption)
#     category = re.match(r"\w+", ctx.options.category_caption)[0]
#     logging.info(f"category: {category}")
#     caption = re.sub(category, "", ctx.options.category_caption).strip()
#     logging.info(f"caption: {caption}")
    

    
#     if len(caption) > 125:
#         await ctx.respond("""
# It's a meme, not your master's thesis. Your caption has to be 125 characters or less.""")
    
#     else:
#         categoryPath = os.path.join(inputImageDir, category)

#         if not category in categories:
#             await ctx.respond(f"""
# Sorry, I don't have any pictures for '{category}'
# Use toast.help or toast.stats for a list of categories
# """)

#         else:
#             await ctx.respond("Toasting meme...")

#             images = os.listdir(categoryPath)
#             imageChoice = random.choice(images)
#             imagePath = os.path.join(categoryPath, imageChoice)

#             channel = ctx.get_channel()
 
#             with BytesIO() as imageBinary:
#                 render(imagePath, caption).save(imageBinary, 'PNG')

#                 imageBinary.seek(0)
#                 await channel.send(imageBinary)

#             await ctx.edit_last_response("Toasting meme... DING")


def load(bot: Bot):
    bot.add_plugin(plugin)

def unload(bot: Bot):
    bot.remove_plugin(plugin)
