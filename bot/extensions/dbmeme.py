import hikari
import lightbulb
import os, random, string
import pandas as pd
from psycopg2 import connect
from io import BytesIO
import logging

from bot import Bot
from bot.pic import render

current_guilds = [833477250841837598] # Tutorial

inputImageDir = './data/images/db'
params = dict(dbname = 'dev', user = 'dev', 
            password = 'memetoaster', 
            host = 'localhost', port = '5432')
con = connect(**params)
tags = pd.read_sql("SELECT tag FROM tag;", con = con).values




plugin = lightbulb.Plugin("Functions")

@plugin.command
@lightbulb.option(name = "caption", description = "caption to attach", type = str, default = "",
                    modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name = "tag", description = "picture tag", type = str, required = True)
@lightbulb.command(name = "dbmeme", description = "Put a picture tag and caption in the toaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
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
            logging.info(type(images))
            logging.info(images)
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
