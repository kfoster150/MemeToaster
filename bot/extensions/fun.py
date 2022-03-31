import hikari
import lightbulb
import os, random, string
import pandas as pd
import boto3
from io import BytesIO

from bot import Bot
from bot.pic import render
from data import mt_sql_connect, mt_sql_tags

BUCKET = 'memetoaster'
FOLDER = 'images/db/'

current_guilds = [os.environ['HOME_GUILD_ID'], # Testing Server 1
                  os.environ['ORBITERS_GUILD_ID'] # Testing Server 2
                  ]

plugin = lightbulb.Plugin("Functions")

##### Create tags list

tagsList = mt_sql_tags()

with mt_sql_connect().cursor() as cur:
    cur.execute("SELECT COUNT(id) FROM tag;")
    num_tags = cur.fetchone()[0]
    cur.execute("SELECT COUNT(id) FROM filename;")
    num_pics = cur.fetchone()[0]

# Create txt file
f = open("data/tags.txt", "w+")

f.write(f"Number of tags: {num_tags}\n\n")
f.write(f"Total number of pictures: {num_pics}\n\n")
f.write("Number of pictures per tag:\n\n")

for tag, count in tagsList:
    f.write(f"{tag}\n{count}\n\n")

f.close()
#####

@plugin.command
@lightbulb.command(name = "stats", description = "Show stats about the MemeToaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_stats(ctx: lightbulb.Context) -> None:
    await ctx.respond("https://raw.githubusercontent.com/kfoster150/MemeToaster2/heroku/data/tags.txt")

@plugin.command
@lightbulb.option(name = "caption", description = "caption to attach", type = str, default = "",
                    modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option(name = "tag", description = "picture tag", type = str, required = True)
@lightbulb.command(name = "meme", description = "Put a picture tag and caption in the toaster", guilds = current_guilds)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def command_meme(ctx: lightbulb.Context) -> None:
    caption = ctx.options.caption.strip()
    tag = ctx.options.tag.translate(str.maketrans('', '', string.punctuation)).lower()
    
    if len(caption) > 125:
        await ctx.respond("""
It's a meme, not your master's thesis. Your caption has to be 125 characters or less.""")
    
    else:

        if not tag in dict(mt_sql_tags()):
            await ctx.respond(f"""
Sorry, I don't have any pictures for '{tag}'
Use toast.help or toast.stats for a list of categories
""")

        else:
            await ctx.respond("Toasting meme...")

            query_by_tag = """
SELECT filename FROM filename AS f
	LEFT JOIN tag_filename AS tf
	ON f.id = tf.filename_id
    	LEFT JOIN tag
        ON tf.tag_id = tag.id
WHERE tag.tag = %s"""

            images = pd.read_sql(query_by_tag, con = mt_sql_connect(), params = (tag,)).filename.values
            imageChoice = random.choice(images)

            query_by_filename = """
SELECT tag FROM tag as tg
    LEFT JOIN tag_filename AS tf
    ON tg.id = tf.tag_id
        LEFT JOIN filename AS f
        ON tf.filename_id = f.id
WHERE f.filename = %s"""

            tags = pd.read_sql(query_by_filename, 
                                con = mt_sql_connect(), 
                                params = (imageChoice,)).tag.tolist()
            tagsHashed = ["#" + t for t in tags]
            tagsSend = " ".join(tagsHashed)

            channel = ctx.get_channel()

            s3 = boto3.Session(
                aws_access_key_id = os.environ['AWS_ACCESS_KEY'],
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
            ).resource('s3')
 
            with BytesIO() as imageBinaryDload:
                with BytesIO() as imageBinarySend:
                    s3.Bucket('memetoaster').download_fileobj('images/db/' + imageChoice, imageBinaryDload)
                    render(imageBinaryDload, caption).save(imageBinarySend, 'JPEG')

                    imageBinarySend.seek(0)

                    embed = hikari.Embed()
                    embed.set_footer(tagsSend)
                    embed.set_image(imageBinarySend)
                    await channel.send(embed)

                await ctx.edit_last_response("Toasting meme... DING")



def load(bot: Bot):
    bot.add_plugin(plugin)

def unload(bot: Bot):
    bot.remove_plugin(plugin)
