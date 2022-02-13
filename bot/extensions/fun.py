import hikari
import lightbulb
import os, random, string
import pandas as pd
from io import BytesIO

from bot import Bot
from bot.pic import render
from data import mt_sql_connect, mt_sql_tags

current_guilds = [os.environ['HOME_GUILD_ID'], # Testing Server 1
                  os.environ['ORBITERS_GUILD_ID'] # Testing Server 2
                  ]

plugin = lightbulb.Plugin("Functions")

##### Create tags list
query_str = """
SELECT tg.tag, count(tf.filename_id)
FROM tag_filename AS tf
LEFT JOIN tag AS tg
ON tf.tag_id = tg.id
WHERE tg.tag <> ''
GROUP BY tg.tag
ORDER BY count(tf.filename_id) DESC, tg.tag;"""

tagsDf = pd.read_sql(query_str, con = mt_sql_connect())
tagsList = zip(tagsDf['tag'], tagsDf['count'])

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

    '''
    tags = mt_sql_tags()

    query_str = """
SELECT COUNT(tf.filename_id)
FROM tag
LEFT JOIN tag_filename AS tf
ON tag.id = tf.tag_id
WHERE tag.tag = %s"""

    # Create list of tags with number of pictures
    tags_list = []
    num_list = []
    for tag in tags:
        with mt_sql_connect().cursor() as cur:
            cur.execute(query_str, (tag,))
            num_pics = cur.fetchone()[0]
        pics = str(num_pics) + ' pictures'
        tags_list.append((tag, pics))
        num_list.append(num_pics)

    num_tags = len(tags)

    # Create embed object
    embed = hikari.Embed(color = 0xFF0000)

    embed.add_field(name = 'Number of tags', value = str(num_tags))
    embed.add_field(name = 'Total number of pictures', value = str(sum(num_list)))
    embed.add_field(name = '\u200b', value = "Number of pictures per tag:", inline = False)

    for name, value in tags_list:
        embed.add_field(name = name, value = value, inline = False)

    '''

    # send response
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
            imagePath = os.path.join('./data/images/db', imageChoice)

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
