from __future__ import annotations


import asyncio


import discord
from discord.ext import commands
from dotenv import load_dotenv


from config import load_settings
from cogs.community_systems import CommunitySystems
from cogs.full_features import FullFeatures
from cogs.social_intelligence import SocialIntelligence
from cogs.browser_engine import BrowserEngine
from cogs.community_systems import CommunitySystems
from cogs.full_features import FullFeatures
from cogs.social_intelligence import SocialIntelligence
from config import load_settings
from services.database import init_db


async def main() -> None:
    load_dotenv()
    settings = load_settings()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    await init_db(settings.database_path)
    await bot.add_cog(SocialIntelligence(bot, settings.database_path))
    await bot.add_cog(CommunitySystems(bot, settings.database_path))
    await bot.add_cog(FullFeatures(bot, settings.database_path))
    await bot.add_cog(BrowserEngine(bot))


    @bot.event
    async def on_ready() -> None:
        if settings.guild_id:
            guild = discord.Object(id=settings.guild_id)
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} guild command(s) to {settings.guild_id}")
        else:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} global command(s)")

        print(f"Logged in as {bot.user}")

    bot_token = "PASTE_YOUR_BOT_TOKEN_HERE"
    if bot_token == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("Set your bot token directly in src/bot.py")

    await bot.start(bot_token)


if __name__ == "__main__":
    import asyncio

=======

        print(f"Logged in as {bot.user}")

    if not settings.token:
        raise RuntimeError("Set DISCORD_TOKEN in .env or environment.")

    await bot.start(settings.token)


if __name__ == "__main__":
    asyncio.run(main())
