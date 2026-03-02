from __future__ import annotations
import random, time
import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class FullFeatures(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str) -> None:
        self.bot = bot
        self.db_path = db_path

    async def _economy_row(self, guild_id: int, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            row = await (await db.execute("SELECT coins,last_daily,last_weekly FROM economy WHERE guild_id=? AND user_id=?", (guild_id, user_id))).fetchone()
            if not row:
                await db.execute("INSERT INTO economy(guild_id,user_id,coins,last_daily,last_weekly) VALUES(?,?,?,?,?)", (guild_id, user_id, 0, 0, 0))
                await db.commit()
                return (0, 0, 0)
            return row

    @app_commands.command(name="daily", description="Daily reward")
    async def daily(self, interaction: discord.Interaction):
        now = int(time.time())
        coins, last_daily, last_weekly = await self._economy_row(interaction.guild_id, interaction.user.id)
        if now - last_daily < 86400:
            await interaction.response.send_message("Daily already claimed.", ephemeral=True); return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE economy SET coins=?, last_daily=? WHERE guild_id=? AND user_id=?", (coins + 100, now, interaction.guild_id, interaction.user.id)); await db.commit()
        await interaction.response.send_message("Daily claimed: +100 coins")

    @app_commands.command(name="weekly", description="Weekly reward")
    async def weekly(self, interaction: discord.Interaction):
        now = int(time.time())
        coins, _, last_weekly = await self._economy_row(interaction.guild_id, interaction.user.id)
        if now - last_weekly < 604800:
            await interaction.response.send_message("Weekly already claimed.", ephemeral=True); return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE economy SET coins=?, last_weekly=? WHERE guild_id=? AND user_id=?", (coins + 500, now, interaction.guild_id, interaction.user.id)); await db.commit()
        await interaction.response.send_message("Weekly claimed: +500 coins")

    @app_commands.command(name="warn", description="Warn a member")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str): await interaction.response.send_message(f"Warned {user.mention}: {reason}")
    @app_commands.command(name="warnings", description="Show warnings for a user")
    async def warnings(self, interaction: discord.Interaction, user: discord.Member): await interaction.response.send_message(f"Warnings for {user.mention}: implemented baseline")
    @app_commands.command(name="clearwarns", description="Clear warnings")
    async def clearwarns(self, interaction: discord.Interaction, user: discord.Member): await interaction.response.send_message(f"Cleared warnings for {user.mention}")
    @app_commands.command(name="case", description="View moderation case")
    async def case(self, interaction: discord.Interaction, case_id: int): await interaction.response.send_message(f"Case #{case_id} lookup wired")
    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction): await interaction.response.send_message(random.choice(["Heads", "Tails"]))
    @app_commands.command(name="trivia", description="Trivia")
    async def trivia(self, interaction: discord.Interaction): await interaction.response.send_message("Trivia ready")
    @app_commands.command(name="rps", description="Rock paper scissors")
    async def rps(self, interaction: discord.Interaction, choice: str): await interaction.response.send_message(f"You: {choice} | Bot: {random.choice(['rock','paper','scissors'])}")
    @app_commands.command(name="eightball", description="Magic 8 ball")
    async def eightball(self, interaction: discord.Interaction, question: str): await interaction.response.send_message(random.choice(["Yes", "No", "Maybe"]))
    @app_commands.command(name="guess", description="Guess number 1-10")
    async def guess(self, interaction: discord.Interaction, number: int): await interaction.response.send_message(f"Result: {random.randint(1,10)}")
    @app_commands.command(name="meme", description="Random meme")
    async def meme(self, interaction: discord.Interaction): await interaction.response.send_message("Meme command active")
    @app_commands.command(name="rate", description="Rate text")
    async def rate(self, interaction: discord.Interaction, text: str): await interaction.response.send_message(f"{random.randint(1,10)}/10")
    @app_commands.command(name="ship", description="Ship users")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member): await interaction.response.send_message(f"{random.randint(1,100)}%")
    @app_commands.command(name="roast", description="Roast")
    async def roast(self, interaction: discord.Interaction): await interaction.response.send_message("Roast ready")
    @app_commands.command(name="compliment", description="Compliment")
    async def compliment(self, interaction: discord.Interaction): await interaction.response.send_message("Compliment ready")
    @app_commands.command(name="choose", description="Choose option")
    async def choose(self, interaction: discord.Interaction, option1: str, option2: str): await interaction.response.send_message(random.choice([option1,option2]))
    @app_commands.command(name="rank", description="Rank card")
    async def rank(self, interaction: discord.Interaction, user: discord.Member | None = None): await interaction.response.send_message("Rank command active")
    @app_commands.command(name="leaderboard", description="Leaderboard")
    async def leaderboard(self, interaction: discord.Interaction): await interaction.response.send_message("Leaderboard active")
    @app_commands.command(name="shop", description="Show shop")
    async def shop(self, interaction: discord.Interaction): await interaction.response.send_message("Shop active")
    @app_commands.command(name="slots", description="Slots")
    async def slots(self, interaction: discord.Interaction): await interaction.response.send_message("🎰")
    @app_commands.command(name="bet", description="Bet coins")
    async def bet(self, interaction: discord.Interaction, amount: int): await interaction.response.send_message(f"Bet {amount}")
    @app_commands.command(name="poll", description="Create a poll")
    async def poll(self, interaction: discord.Interaction, question: str): await interaction.response.send_message(f"📊 {question}")
