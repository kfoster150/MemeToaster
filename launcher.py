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

invite link:
https://discord.com/api/oauth2/authorize?client_id=920060661294309378&permissions=2147609664&scope=bot%20applications.commands

hikari docs:
https://www.hikari-py.dev/hikari/index.html

lightbulb docs:
https://hikari-lightbulb.readthedocs.io/en/latest/
'''