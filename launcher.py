import os

from bot.bot import Bot

if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    bot = Bot()
    bot.run()

'''
run like this:
python -OO launcher.py

invite links
Main:
https://discord.com/api/oauth2/authorize?client_id=920060661294309378&permissions=8&scope=bot%20applications.commands

Dev:
https://discord.com/api/oauth2/authorize?client_id=925887767475531878&permissions=8&scope=bot%20applications.commands

hikari docs:
https://www.hikari-py.dev/hikari/index.html

lightbulb docs:
https://hikari-lightbulb.readthedocs.io/en/latest/
'''