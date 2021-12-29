import hikari
import lightbulb
import logging
import os

from bot import Bot

inputImageDir = './data/images/input'
categories = os.listdir(inputImageDir)
categories.sort()

class ToasterHelp(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context):
        # Override this method to change the message sent when the help command
        # is run without any arguments.

        # Create list of categories with number of files
        cats_list = [[],[],[]]
        counter = 0
        for c in categories:
            cats_list[counter % 3].append(c)
            counter += 1

        cats_embed = ["\n".join(cats_list[0]),
                      "\n".join(cats_list[1]),
                      "\n".join(cats_list[2])]

        # Create embed object
        embed = hikari.Embed(title = 'HOW TO USE',
        description = """
1. Type `/meme` in the message bar
2. Select `category`, and type a valid category
3. Select `message`, and type your message
""",
                        color = 0xFF0000)

        embed.add_field(name = 'CATEGORIES', value = cats_embed[0],inline = True)
        embed.add_field(name = '\u200b', value = cats_embed[1], inline = True)
        embed.add_field(name = '\u200b', value = cats_embed[2], inline = True)

        embed.add_field(name = '\u200b', value = """
Type `/stats` for more details
Feedback? Picture/Category Suggestions?
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