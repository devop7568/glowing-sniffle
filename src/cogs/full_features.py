from __future__ import annotations

import random
import time
from collections import Counter, defaultdict

import discord
from discord import app_commands
from discord.ext import commands


class FullFeatures(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str) -> None:
        self.bot = bot
        self.db_path = db_path
        self.msg_cooldowns: dict[tuple[int, int], float] = {}
        self.warn_thresholds = {3: "mute", 5: "kick", 7: "ban"}

    async def _db(self):
        import aiosqlite
        return await aiosqlite.connect(self.db_path)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        ch = discord.utils.get(member.guild.text_channels, name="general")
        if ch:
            await ch.send(f"Welcome {member.mention} to **{member.guild.name}** 🎉")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return
        key = (message.guild.id, message.author.id)
        now = time.time()
        gain_xp = 10 if now - self.msg_cooldowns.get(key, 0) > 30 else 0
        self.msg_cooldowns[key] = now
        async with await self._db() as db:
            await db.execute("INSERT INTO economy(guild_id,user_id,coins,last_daily,last_weekly) VALUES(?,?,?,?,?) ON CONFLICT(guild_id,user_id) DO NOTHING", (message.guild.id, message.author.id, 0, 0, 0))
            if gain_xp:
                await db.execute("UPDATE user_stats SET xp=xp+?, messages_count=messages_count+1 WHERE guild_id=? AND user_id=?", (gain_xp, message.guild.id, message.author.id))
                await db.execute("UPDATE economy SET coins=coins+2 WHERE guild_id=? AND user_id=?", (message.guild.id, message.author.id))
            await db.commit()

    @app_commands.command(name="warn", description="Warn a member")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        async with await self._db() as db:
            await db.execute("INSERT INTO warnings(guild_id,user_id,moderator_id,reason) VALUES(?,?,?,?)", (interaction.guild_id, user.id, interaction.user.id, reason))
            total = (await (await db.execute("SELECT COUNT(*) FROM warnings WHERE guild_id=? AND user_id=?", (interaction.guild_id, user.id))).fetchone())[0]
            await db.execute("INSERT INTO mod_cases(guild_id,action,target_id,moderator_id,reason) VALUES(?,?,?,?,?)", (interaction.guild_id, "warn", user.id, interaction.user.id, reason))
            await db.commit()
        action = self.warn_thresholds.get(total)
        await interaction.response.send_message(f"Warned {user.mention}. Total warnings: {total}. Auto-action: {action or 'none'}")

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))

    @app_commands.command(name="daily", description="Claim daily coins")
    async def daily(self, interaction: discord.Interaction) -> None:
        now = int(time.time())
        async with await self._db() as db:
            row = await (await db.execute("SELECT last_daily, coins FROM economy WHERE guild_id=? AND user_id=?", (interaction.guild_id, interaction.user.id))).fetchone()
            if not row:
                await db.execute("INSERT INTO economy(guild_id,user_id,coins,last_daily,last_weekly) VALUES(?,?,?,?,?)", (interaction.guild_id, interaction.user.id, 100, now, 0))
                await db.commit()
                await interaction.response.send_message("Claimed 100 coins.")
                return
            last_daily, coins = row
            if now - last_daily < 86400:
                await interaction.response.send_message("Daily already claimed.", ephemeral=True)
                return
            await db.execute("UPDATE economy SET coins=?, last_daily=? WHERE guild_id=? AND user_id=?", (coins + 100, now, interaction.guild_id, interaction.user.id))
            await db.commit()
        await interaction.response.send_message("Claimed 100 coins.")

    @app_commands.command(name="rank", description="Show rank")
    async def rank(self, interaction: discord.Interaction, user: discord.Member | None = None) -> None:
        target = user or interaction.user
        async with await self._db() as db:
            row = await (await db.execute("SELECT xp,messages_count FROM user_stats WHERE guild_id=? AND user_id=?", (interaction.guild_id, target.id))).fetchone()
            if not row:
                await interaction.response.send_message("No rank data.", ephemeral=True)
                return
            xp, messages = row
            lvl = xp // 100
        await interaction.response.send_message(f"{target.mention} Level `{lvl}` | XP `{xp}` | Messages `{messages}`")

    @app_commands.command(name="leaderboard", description="Top active members")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        async with await self._db() as db:
            rows = await (await db.execute("SELECT user_id,xp FROM user_stats WHERE guild_id=? ORDER BY xp DESC LIMIT 10", (interaction.guild_id,))).fetchall()
        text = "\n".join([f"{idx+1}. <@{u}> - {xp} XP" for idx, (u, xp) in enumerate(rows)]) or "No data"
        await interaction.response.send_message(text)
