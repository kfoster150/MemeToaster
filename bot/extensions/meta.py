import hikari
import lightbulb

from bot import Bot

plugin = lightbulb.Plugin("Meta")

@plugin.command
@lightbulb.command(name = "ping", description = "Test")
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Latency: {ctx.bot.heartbeat_latency * 1_000:,.0f} ms.")

def load(bot: Bot):
    bot.add_plugin(plugin)

def unload(bot: Bot):
    bot.remove_plugin(plugin)