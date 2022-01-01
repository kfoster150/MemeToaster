import logging

import hikari
import lightbulb
from apscheduler.schedulers.asyncio import AsyncIOScheduler

__VERSION__ = '0.2.0'

HOME_GUILD_ID = 833477250841837598
STDOUT_CHANNEL_ID = 872682916788973638

class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone = 'utc')

        with open("./secrets/token", mode = "r", encoding = "utf-8") as f:
            token = f.read().strip()

        super().__init__(
            prefix = "toast.",
            token = token,
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