import logging
import os

import hikari
import lightbulb
from apscheduler.schedulers.asyncio import AsyncIOScheduler

__VERSION__ = os.environ['VERSION']
if __VERSION__ == "PUBLIC":
    PREFIX = "toast."
elif __VERSION__ == "TEST":
    PREFIX = "test."

HOME_GUILD_ID = os.environ['HOME_GUILD_ID']
STDOUT_CHANNEL_ID = os.environ['STDOUT_CHANNEL_ID']

class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone = 'utc')


        super().__init__(
            prefix = PREFIX,
            token = os.environ['MT_SECRET'],
            intents = hikari.Intents.ALL,
        )


    def run(self) -> None:

        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        
        super().run(
            activity = hikari.Activity(
                name = f"toast.help | /meme",
                type = hikari.ActivityType.WATCHING)
        )


    async def on_starting(self, event: hikari.StartingEvent) -> None:
        self.load_extensions_from("./bot/extensions/")


    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()

        # YO Not guaranteed to be cached in time.
        self.stdout_channel = await self.rest.fetch_channel(STDOUT_CHANNEL_ID)
        await self.stdout_channel.send(f"v{__VERSION__} now online.")
        logging.info("BOT READY")


    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        # YO Message doesn't always send for some reason, but bot shuts down like it should
        await self.stdout_channel.send(f"v{__VERSION__} is shutting down.")
        self.scheduler.shutdown()