from __future__ import annotations

import datetime as dt
import statistics
from collections import Counter

import discord
import networkx as nx
from discord import app_commands
from discord.ext import commands


class SocialIntelligence(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str) -> None:
        self.bot = bot
        self.db_path = db_path

    @app_commands.command(name="vouch", description="Vouch for a member with a reason")
    async def vouch(self, interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        import aiosqlite

        if user.id == interaction.user.id:
            await interaction.response.send_message("You cannot vouch for yourself.", ephemeral=True)
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR REPLACE INTO reputations(guild_id, voucher_id, target_id, reason)
                VALUES(?, ?, ?, ?)""",
                (interaction.guild_id, interaction.user.id, user.id, reason),
            )
            await db.commit()

        await interaction.response.send_message(f"✅ Vouch recorded for {user.mention}.")

    @app_commands.command(name="trustscore", description="View trust network score for a member")
    async def trustscore(self, interaction: discord.Interaction, user: discord.Member) -> None:
        import aiosqlite

        graph = nx.DiGraph()
        async with aiosqlite.connect(self.db_path) as db:
            rows = await (await db.execute(
                "SELECT voucher_id, target_id FROM reputations WHERE guild_id = ?", (interaction.guild_id,)
            )).fetchall()

        for voucher_id, target_id in rows:
            graph.add_edge(voucher_id, target_id)

        if len(graph) == 0:
            await interaction.response.send_message("No reputation graph data yet.", ephemeral=True)
            return

        pagerank = nx.pagerank(graph, alpha=0.85)
        score = pagerank.get(user.id, 0.0)
        trusted_by_mod = any((r.permissions.manage_messages for r in user.roles))
        mutual_ring = len(list(nx.simple_cycles(graph))) > 0

        await interaction.response.send_message(
            f"Trust score for {user.mention}: `{score:.4f}`\n"
            f"Trusted by moderators: `{'yes' if trusted_by_mod else 'no'}`\n"
            f"Suspicious mutual-vouching rings detected: `{'yes' if mutual_ring else 'no'}`"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO messages(guild_id, user_id, channel_id, content) VALUES (?, ?, ?, ?)",
                (message.guild.id, message.author.id, message.channel.id, message.content[:500]),
            )
            await db.execute(
                """INSERT INTO user_stats(guild_id, user_id, xp, messages_count, joined_at)
                VALUES (?, ?, 5, 1, ?)
                ON CONFLICT(guild_id, user_id) DO UPDATE SET
                xp = xp + 5,
                messages_count = messages_count + 1""",
                (message.guild.id, message.author.id, message.author.joined_at),
            )
            await db.commit()

    @app_commands.command(name="behavior", description="Analyze member behavior risk")
    async def behavior(self, interaction: discord.Interaction, user: discord.Member) -> None:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            rows = await (await db.execute(
                "SELECT content, created_at FROM messages WHERE guild_id=? AND user_id=? ORDER BY created_at DESC LIMIT 200",
                (interaction.guild_id, user.id),
            )).fetchall()

        if len(rows) < 5:
            await interaction.response.send_message("Not enough behavior data yet.", ephemeral=True)
            return

        times = [dt.datetime.fromisoformat(r[1]) for r in rows if r[1]]
        deltas = [abs((times[i] - times[i + 1]).total_seconds()) for i in range(len(times) - 1)]
        variance = statistics.pvariance(deltas) if len(deltas) > 2 else 0
        copy_ratio = sum(1 for content, _ in rows if len(content) > 20 and content.count(" ") < 3) / len(rows)
        account_age_days = (dt.datetime.now(dt.timezone.utc) - user.created_at).days

        risk = min(100, int((variance / 5000) + (copy_ratio * 35) + (20 if account_age_days < 30 else 0)))

        await interaction.response.send_message(
            f"Behavior report for {user.mention}:\n"
            f"- Risk score: `{risk}/100`\n"
            f"- Activity anomaly index: `{variance:.2f}`\n"
            f"- Possible alt account: `{'high' if account_age_days < 14 and risk > 60 else 'low'}`"
        )
