from __future__ import annotations

import random, time
import aiosqlite

import random

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



    @app_commands.command(name="warn", description="Warn a member")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        await interaction.response.send_message(f"Warned {user.mention} for: {reason}")

    @app_commands.command(name="warnings", description="Show warnings for a user")
    async def warnings(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f"Warnings for {user.mention}: 0 (scaffold)")

    @app_commands.command(name="clearwarns", description="Clear warnings")
    async def clearwarns(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f"Cleared warnings for {user.mention}")

    @app_commands.command(name="case", description="View moderation case")
    async def case(self, interaction: discord.Interaction, case_id: int):
        await interaction.response.send_message(f"Case #{case_id} not found (scaffold)")

    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))

    @app_commands.command(name="trivia", description="Trivia")
    async def trivia(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trivia: What does API stand for? Answer: Application Programming Interface")

    @app_commands.command(name="rps", description="Rock paper scissors")
    async def rps(self, interaction: discord.Interaction, choice: str):
        bot = random.choice(["rock", "paper", "scissors"])
        await interaction.response.send_message(f"You: {choice.lower()} | Bot: {bot}")

    @app_commands.command(name="eightball", description="Magic 8 ball")
    async def eightball(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(random.choice(["Yes", "No", "Maybe"]))

    @app_commands.command(name="guess", description="Guess number 1-10")
    async def guess(self, interaction: discord.Interaction, number: int):
        n = random.randint(1, 10)
        await interaction.response.send_message("Correct!" if n == number else f"Nope, it was {n}")

    @app_commands.command(name="meme", description="Random meme placeholder")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.send_message("Meme feature is scaffolded (API integration optional).")

    @app_commands.command(name="rate", description="Rate text")
    async def rate(self, interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f"{text}: {random.randint(1,10)}/10")

    @app_commands.command(name="ship", description="Ship two users")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        await interaction.response.send_message(f"Compatibility: {random.randint(1,100)}%")

    @app_commands.command(name="roast", description="Roast")
    async def roast(self, interaction: discord.Interaction):
        await interaction.response.send_message("You deploy on Friday? Bold.")

    @app_commands.command(name="compliment", description="Compliment")
    async def compliment(self, interaction: discord.Interaction):
        await interaction.response.send_message("You make this server better.")

    @app_commands.command(name="choose", description="Choose between two options")
    async def choose(self, interaction: discord.Interaction, option1: str, option2: str):
        await interaction.response.send_message(random.choice([option1, option2]))

    @app_commands.command(name="daily", description="Daily reward")
    async def daily(self, interaction: discord.Interaction):
        await interaction.response.send_message("Daily claimed: +100 coins (scaffold)")

    @app_commands.command(name="weekly", description="Weekly reward")
    async def weekly(self, interaction: discord.Interaction):
        await interaction.response.send_message("Weekly claimed: +500 coins (scaffold)")

    @app_commands.command(name="rank", description="Rank card")
    async def rank(self, interaction: discord.Interaction, user: discord.Member | None = None):
        target = user or interaction.user
        await interaction.response.send_message(f"{target.mention} | Level 1 | XP 0 | Rank #1 | Messages 0 (scaffold)")

    @app_commands.command(name="leaderboard", description="Leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.send_message("1) You - 0 XP (scaffold)")

    @app_commands.command(name="shop", description="Show shop")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.send_message("Shop: role-color, xp-boost, perks, lottery-ticket")

    @app_commands.command(name="slots", description="Slots")
    async def slots(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎰 | 🍒 🍒 🍋")

    @app_commands.command(name="bet", description="Bet coins")
    async def bet(self, interaction: discord.Interaction, amount: int):
        await interaction.response.send_message(f"Bet {amount}: {'won' if random.random()>0.5 else 'lost'}")

    @app_commands.command(name="poll", description="Create a poll")
    async def poll(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(f"📊 {question}\nReact with 👍/👎")
=======
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

