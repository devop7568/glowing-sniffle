from __future__ import annotations

import random
import time

import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands


class FullFeatures(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str) -> None:
        self.bot = bot
        self.db_path = db_path

    async def _economy_row(self, guild_id: int, user_id: int) -> tuple[int, int, int]:
        async with aiosqlite.connect(self.db_path) as db:
            row = await (
                await db.execute(
                    "SELECT coins,last_daily,last_weekly FROM economy WHERE guild_id=? AND user_id=?",
                    (guild_id, user_id),
                )
            ).fetchone()
            if not row:
                await db.execute(
                    "INSERT INTO economy(guild_id,user_id,coins,last_daily,last_weekly) VALUES(?,?,?,?,?)",
                    (guild_id, user_id, 0, 0, 0),
                )
                await db.commit()
                return (0, 0, 0)
            return (int(row[0]), int(row[1]), int(row[2]))

    @app_commands.command(name="daily", description="Claim daily reward")
    async def daily(self, interaction: discord.Interaction) -> None:
        now = int(time.time())
        coins, last_daily, _ = await self._economy_row(interaction.guild_id, interaction.user.id)
        if now - last_daily < 86400:
            await interaction.response.send_message("Daily already claimed.", ephemeral=True)
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE economy SET coins=?, last_daily=? WHERE guild_id=? AND user_id=?",
                (coins + 100, now, interaction.guild_id, interaction.user.id),
            )
            await db.commit()
        await interaction.response.send_message("Daily claimed: +100 coins")

    @app_commands.command(name="weekly", description="Claim weekly reward")
    async def weekly(self, interaction: discord.Interaction) -> None:
        now = int(time.time())
        coins, _, last_weekly = await self._economy_row(interaction.guild_id, interaction.user.id)
        if now - last_weekly < 604800:
            await interaction.response.send_message("Weekly already claimed.", ephemeral=True)
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE economy SET coins=?, last_weekly=? WHERE guild_id=? AND user_id=?",
                (coins + 500, now, interaction.guild_id, interaction.user.id),
            )
            await db.commit()
        await interaction.response.send_message("Weekly claimed: +500 coins")

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))
