from __future__ import annotations

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import load_settings
from cogs.community_systems import CommunitySystems
from cogs.full_features import FullFeatures
from cogs.social_intelligence import SocialIntelligence
from services.database import init_db


async def main() -> None:
    load_dotenv()
    settings = load_settings()
    bot_token = "PASTE_YOUR_BOT_TOKEN_HERE"  # direct token optional

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    await init_db(settings.database_path)
    await bot.add_cog(SocialIntelligence(bot, settings.database_path))
    await bot.add_cog(CommunitySystems(bot, settings.database_path))
    await bot.add_cog(FullFeatures(bot, settings.database_path))

    @bot.event
    async def on_ready() -> None:
        if settings.guild_id:
            guild = discord.Object(id=settings.guild_id)
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        else:
            await bot.tree.sync()
        print(f"Logged in as {bot.user}")

    resolved_token = bot_token if bot_token != "PASTE_YOUR_BOT_TOKEN_HERE" else settings.token
    if not resolved_token:
        raise RuntimeError("Set token in src/bot.py bot_token or DISCORD_TOKEN env.")

    await bot.start(resolved_token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
