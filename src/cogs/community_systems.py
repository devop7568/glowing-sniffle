from __future__ import annotations

import datetime as dt
from collections import Counter

import discord
from discord import app_commands
from discord.ext import commands, tasks


class CommunitySystems(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str) -> None:
        self.bot = bot
        self.db_path = db_path
        self.role_evolution.start()

    def cog_unload(self) -> None:
        self.role_evolution.cancel()

    @tasks.loop(hours=6)
    async def role_evolution(self) -> None:
        thresholds = [(7, "Regular"), (30, "Core Member"), (180, "Veteran")]
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot or not member.joined_at:
                    continue
                age = (dt.datetime.now(dt.timezone.utc) - member.joined_at).days
                for days, role_name in thresholds:
                    if age >= days:
                        role = discord.utils.get(guild.roles, name=role_name)
                        if role and role not in member.roles:
                            await member.add_roles(role, reason="Dynamic identity role evolution")

    @app_commands.command(name="propose", description="Create a server proposal")
    async def propose(self, interaction: discord.Interaction, title: str, body: str) -> None:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO proposals(guild_id, proposer_id, title, body, action_type, action_payload) VALUES (?, ?, ?, ?, ?, ?)",
                (interaction.guild_id, interaction.user.id, title, body, "announcement", body),
            )
            proposal_id = cursor.lastrowid
            await db.commit()

        await interaction.response.send_message(f"Proposal #{proposal_id} created: **{title}**")

    @app_commands.command(name="vote", description="Vote on a proposal")
    async def vote(self, interaction: discord.Interaction, proposal_id: int, choice: str) -> None:
        import aiosqlite

        vote_yes = choice.lower() == "yes"
        async with aiosqlite.connect(self.db_path) as db:
            column = "yes_votes" if vote_yes else "no_votes"
            await db.execute(f"UPDATE proposals SET {column} = {column} + 1 WHERE id = ? AND guild_id = ?", (proposal_id, interaction.guild_id))
            await db.commit()

        await interaction.response.send_message(f"Vote recorded: `{choice}` on proposal #{proposal_id}.")

    @app_commands.command(name="heatmap", description="Show top active hours")
    async def heatmap(self, interaction: discord.Interaction) -> None:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            rows = await (await db.execute(
                "SELECT strftime('%H', created_at) FROM messages WHERE guild_id = ?", (interaction.guild_id,)
            )).fetchall()

        if not rows:
            await interaction.response.send_message("No activity data yet.", ephemeral=True)
            return

        hours = Counter(int(r[0]) for r in rows if r[0] is not None)
        top = hours.most_common(5)
        text = "\n".join(f"- {h:02d}:00 => {c} messages" for h, c in top)
        await interaction.response.send_message(f"Top activity hours:\n{text}")

    @app_commands.command(name="forecast", description="Forecast next peak activity window")
    async def forecast(self, interaction: discord.Interaction) -> None:
        import aiosqlite

        async with aiosqlite.connect(self.db_path) as db:
            rows = await (await db.execute(
                "SELECT strftime('%w', created_at), strftime('%H', created_at) FROM messages WHERE guild_id = ?",
                (interaction.guild_id,),
            )).fetchall()

        if len(rows) < 20:
            await interaction.response.send_message("Need more data (20+ messages) for forecast.", ephemeral=True)
            return

        slots = Counter((int(d), int(h)) for d, h in rows if d is not None and h is not None)
        day, hour = slots.most_common(1)[0][0]
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        await interaction.response.send_message(f"Predicted next peak: **{days[day]} {hour:02d}:00**")
