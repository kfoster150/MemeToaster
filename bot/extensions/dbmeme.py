import hikari
import lightbulb
import os, random, string
from lightbulb.errors import LightbulbError
import pandas as pd
from psycopg2 import connect
from urllib.parse import urlparse
from io import BytesIO
import logging

from bot import Bot
from bot.pic import render

current_guilds = [os.environ['HOME_GUILD_ID'], # Testing Server 1
                  os.environ['ORBITERS_GUILD_ID'] # Testing Server 2
                  ]

url = urlparse(os.environ['DATABASE_URL'])

con = connect(
    dbname = url.path[1:],
    user = url.username,
    password = url.password,
    host = url.hostname,
    port = url.port
)
tags = pd.read_sql("SELECT tag FROM tag;", con = con).values

plugin = lightbulb.Plugin("Functions")
inputImageDir = './data/images/db'

@plugin.command
@lightbulb.command(name = "dbhelp", description = "Get help with MemeToaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_db_help(ctx = lightbulb.context) -> None:
        tags_list = [[],[],[]]
        counter = 0
        for tag in tags:
            tags_list[counter % 3].append(tag)
            counter += 1

        tags_embed = ["\n".join(tags_list[0]),
                      "\n".join(tags_list[1]),
                      "\n".join(tags_list[2])]

        # Create embed object
        embed = hikari.Embed(title = 'HOW TO USE',
        description = """
1. Type `/meme` in the message bar
2. Select `category`, and type a valid category
3. Select `message`, and type your message
""",
                        color = 0xFF0000)

        embed.add_field(name = 'CATEGORIES', value = tags_embed[0],inline = True)
        embed.add_field(name = '\u200b', value = tags_embed[1], inline = True)
        embed.add_field(name = '\u200b', value = tags_embed[2], inline = True)

        embed.add_field(name = '\u200b', value = """
Type `/stats` for more details
Feedback? Picture/Category Suggestions?
Email: `DiscordMemeToaster@gmail.com`""")

        # send embed object
        await ctx.respond(embed = embed)



@plugin.command
@lightbulb.command(name = "dbstats", description = "Show stats about the MemeToaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_stats(ctx: lightbulb.Context) -> None:

    query_str = f"""
SELECT COUNT(tf.filename_id)
FROM tag AS tg
LEFT JOIN tag_filename AS tf
ON tg.id = tf.tag_id
WHERE tg.tag = """

    # Create list of categories with number of files
    tags_list = []
    num_list = []
    for tag in tags:
        tag = tag[0]
        with con.cursor() as cur:
            cur.execute(query_str + f"'{tag}'" + ";")
            num_pics = cur.fetchone()[0]
        pics = str(num_pics) + ' pictures'
        tags_list.append((tag, pics))
        num_list.append(num_pics)

    num_tags = len(tags)

    # Create embed object
    embed = hikari.Embed(color = 0xFF0000)

    embed.add_field(name = 'Number of categories', value = str(num_tags))
    embed.add_field(name = 'Total number of pictures', value = str(sum(num_list)))
    embed.add_field(name = '\u200b', value = "Number of pictures per category:", inline = False)

    for name, value in tags_list:
        embed.add_field(name = name, value = value, inline = False)

    # send embed object
    await ctx.respond(embed = embed)

@plugin.command
@lightbulb.option(name = "caption", description = "caption to attach", type = str, default = "",
                    modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name = "tag", description = "picture tag", type = str, required = True)
@lightbulb.command(name = "dbmeme", description = "Put a picture tag and caption in the toaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_meme(ctx: lightbulb.Context) -> None:
    caption = ctx.options.caption.strip()
    tag = ctx.options.tag.translate(str.maketrans('', '', string.punctuation)).lower()
    
    if len(caption) > 125:
        await ctx.respond("""
It's a meme, not your master's thesis. Your caption has to be 125 characters or less.""")
    
    else:

        if not tag in tags:
            await ctx.respond(f"""
Sorry, I don't have any pictures for '{tag}'
Use toast.help or toast.stats for a list of categories
""")

        else:
            await ctx.respond("Toasting meme...")

            query_by_tag = f"""
SELECT filename FROM filename AS f
	LEFT JOIN tag_filename AS tf
	ON f.id = tf.filename_id
    	LEFT JOIN tag
        ON tf.tag_id = tag.id
WHERE tag.tag = '{tag}';
"""

            images = pd.read_sql(query_by_tag, con = con).filename.values
            imageChoice = random.choice(images)
            imagePath = os.path.join(inputImageDir, imageChoice)

            channel = ctx.get_channel()
 
            with BytesIO() as imageBinary:
                render(imagePath, caption).save(imageBinary, 'JPEG')

                imageBinary.seek(0)
                await channel.send(imageBinary)

            await ctx.edit_last_response("Toasting meme... DING")


def load(bot: Bot):
    bot.add_plugin(plugin)

def unload(bot: Bot):
    bot.remove_plugin(plugin)
