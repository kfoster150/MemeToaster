import lightbulb

from bot import Bot

plugin = lightbulb.Plugin("Administrative")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(name = "shutdown", aliases = ("sd",), description = "Shutdown the Bot")
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_shutdown(ctx: lightbulb.Context) -> None:
    await ctx.bot.close()


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(name = "reload", aliases = ("rl",), description = "Restart the bot")
@lightbulb.implements(lightbulb.PrefixCommand)
async def command_reload(ctx: lightbulb.Context) -> None:
    pass


def load(bot: Bot):
    bot.add_plugin(plugin)


def unload(bot: Bot):
    bot.remove_plugin(plugin)