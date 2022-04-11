import hikari
import lightbulb
import random

from bot import Bot
from data import mt_sql_tags

class ToasterHelp(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context):
        # Override this method to change the message sent when the help command
        # is run without any arguments.

        tags = mt_sql_tags(output = "DataFrame")
        topTags = tags[tags['count'] > 14]['tag'].tolist()
        topTags.sort()
        otherTags = random.sample(
            tags[tags['count'] < 15]['tag'].tolist(),
            k = 3)

        
        splitList = [[],[],[]]
        rows = round(len(topTags)/3)
        col = 0
        counter = 0
        for tag in topTags:
            splitList[col].append(tag)
            counter += 1
            if counter == rows:
                col += 1
                counter = 0

        tags_embed = ["\n".join(splitList[0]),
                      "\n".join(splitList[1]),
                      "\n".join(splitList[2])]

        print(tags_embed[0])
        print(tags_embed[1])
        print(tags_embed[2])
        print(otherTags)

        # Create embed object
        embed = hikari.Embed(title = 'HOW TO USE',
        description = """
1. Type `/meme` in the message bar
2. Select `tag`, and type a valid tag
3. Select `caption`, and type your caption
""",
                        color = 0xFF0000)

        embed.add_field(name = 'TOP TAGS', value = tags_embed[0],inline = True)
        embed.add_field(name = '\u200b', value = tags_embed[1], inline = True)
        embed.add_field(name = '\u200b', value = tags_embed[2], inline = True)

        embed.add_field(name = "Try these tags too!", value = "\n".join(otherTags))

        embed.add_field(name = '\u200b', value = """
Type `/tags` for more options

Full documentation:
https://github.com/kfoster150/MemeToaster#readme

Feedback? Picture/Tag Suggestions?
Email: `DiscordMemeToaster@gmail.com`""")

        # send embed object
        await context.respond(embed = embed)

    async def send_plugin_help(self, context, plugin):
        # Override this method to change the message sent when the help command
        # argument is the name of a plugin.
        pass

    async def send_command_help(self, context, command):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command.
        pass

    async def send_group_help(self, context, group):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command group.
        pass

    async def object_not_found(self, context, obj):
        # Override this method to change the message sent when help is
        # requested for an object that does not exist
        pass



def load(bot: Bot):
    bot.d.old_help_command = bot.help_command
    bot.help_command = ToasterHelp(bot)

def unload(bot):
    bot.help_command = bot.d.old_help_command
    del bot.d.old_help_command