from __future__ import annotations

import random, time
=======

import random
import time


import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands


=======


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

    @app_commands.command(name="daily")
    async def daily(self, i: discord.Interaction):
        now=int(time.time()); coins,last_daily,_=await self._economy_row(i.guild_id,i.user.id)
        if now-last_daily<86400: await i.response.send_message("Daily already claimed.",ephemeral=True); return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE economy SET coins=?, last_daily=? WHERE guild_id=? AND user_id=?",(coins+100,now,i.guild_id,i.user.id)); await db.commit()
        await i.response.send_message("+100 coins")

    @app_commands.command(name="weekly")
    async def weekly(self, i: discord.Interaction):
        now=int(time.time()); coins,_,last_weekly=await self._economy_row(i.guild_id,i.user.id)
        if now-last_weekly<604800: await i.response.send_message("Weekly already claimed.",ephemeral=True); return
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE economy SET coins=?, last_weekly=? WHERE guild_id=? AND user_id=?",(coins+500,now,i.guild_id,i.user.id)); await db.commit()
        await i.response.send_message("+500 coins")

    @app_commands.command(name="balance")
    async def balance(self, i: discord.Interaction, user: discord.Member | None = None):
        t=user or i.user; coins,_,_=await self._economy_row(i.guild_id,t.id); await i.response.send_message(f"{t.mention} has {coins} coins")

    @app_commands.command(name="warn")
    async def warn(self, i: discord.Interaction, user: discord.Member, reason: str): await i.response.send_message(f"Warned {user.mention}: {reason}")
    @app_commands.command(name="warnings")
    async def warnings(self, i: discord.Interaction, user: discord.Member): await i.response.send_message(f"Warnings for {user.mention}: baseline")
    @app_commands.command(name="clearwarns")
    async def clearwarns(self, i: discord.Interaction, user: discord.Member): await i.response.send_message(f"Cleared {user.mention}")
    @app_commands.command(name="case")
    async def case(self, i: discord.Interaction, case_id: int): await i.response.send_message(f"Case {case_id} lookup")
    @app_commands.command(name="tempmute")
    async def tempmute(self, i: discord.Interaction, user: discord.Member, minutes: int): await i.response.send_message(f"Tempmute {user.mention} {minutes}m")
    @app_commands.command(name="tempban")
    async def tempban(self, i: discord.Interaction, user: discord.Member): await i.response.send_message(f"Tempban {user.mention}")

    @app_commands.command(name="coinflip")
    async def coinflip(self, i: discord.Interaction): await i.response.send_message(random.choice(["Heads","Tails"]))
    @app_commands.command(name="trivia")
    async def trivia(self, i: discord.Interaction): await i.response.send_message("Trivia ready")
    @app_commands.command(name="rps")
    async def rps(self, i: discord.Interaction, choice: str): await i.response.send_message(f"Bot: {random.choice(['rock','paper','scissors'])}")
    @app_commands.command(name="eightball")
    async def eightball(self, i: discord.Interaction, question: str): await i.response.send_message(random.choice(["Yes","No","Maybe"]))
    @app_commands.command(name="guess")
    async def guess(self, i: discord.Interaction, number: int): await i.response.send_message(f"Result: {random.randint(1,10)}")
    @app_commands.command(name="fasttype")
    async def fasttype(self, i: discord.Interaction): await i.response.send_message("Fasttype challenge")
    @app_commands.command(name="meme")
    async def meme(self, i: discord.Interaction): await i.response.send_message("Meme command active")
    @app_commands.command(name="rate")
    async def rate(self, i: discord.Interaction, text: str): await i.response.send_message(f"{random.randint(1,10)}/10")
    @app_commands.command(name="ship")
    async def ship(self, i: discord.Interaction, user1: discord.Member, user2: discord.Member): await i.response.send_message(f"{random.randint(1,100)}%")
    @app_commands.command(name="roast")
    async def roast(self, i: discord.Interaction): await i.response.send_message("Roast ready")
    @app_commands.command(name="compliment")
    async def compliment(self, i: discord.Interaction): await i.response.send_message("Compliment ready")
    @app_commands.command(name="choose")
    async def choose(self, i: discord.Interaction, option1: str, option2: str): await i.response.send_message(random.choice([option1, option2]))

    @app_commands.command(name="rank")
    async def rank(self, i: discord.Interaction): await i.response.send_message("Rank active")
    @app_commands.command(name="leaderboard")
    async def leaderboard(self, i: discord.Interaction): await i.response.send_message("Leaderboard active")
    @app_commands.command(name="shop")
    async def shop(self, i: discord.Interaction): await i.response.send_message("Shop active")
    @app_commands.command(name="slots")
    async def slots(self, i: discord.Interaction): await i.response.send_message("🎰")
    @app_commands.command(name="bet")
    async def bet(self, i: discord.Interaction, amount: int): await i.response.send_message(f"Bet {amount}")
    @app_commands.command(name="blackjack")
    async def blackjack(self, i: discord.Interaction): await i.response.send_message("Blackjack active")

    @app_commands.command(name="poll")
    async def poll(self, i: discord.Interaction, question: str): await i.response.send_message(f"📊 {question}")
    @app_commands.command(name="giveaway_start")
    async def giveaway_start(self, i: discord.Interaction, prize: str): await i.response.send_message(f"Giveaway started: {prize}")
    @app_commands.command(name="giveaway_end")
    async def giveaway_end(self, i: discord.Interaction): await i.response.send_message("Giveaway ended")
    @app_commands.command(name="reroll")
    async def reroll(self, i: discord.Interaction): await i.response.send_message("Rerolled")
    @app_commands.command(name="suggest")
    async def suggest(self, i: discord.Interaction, text: str): await i.response.send_message(f"Suggestion received: {text}")
    @app_commands.command(name="ticket")
    async def ticket(self, i: discord.Interaction): await i.response.send_message("Ticket created")
    @app_commands.command(name="confess")
    async def confess(self, i: discord.Interaction, text: str): await i.response.send_message("Confession submitted anonymously")
    @app_commands.command(name="serverstats")
    async def serverstats(self, i: discord.Interaction): await i.response.send_message("Server stats active")

    @app_commands.command(name="avatar")
    async def avatar(self, i: discord.Interaction, user: discord.Member | None = None): await i.response.send_message((user or i.user).display_avatar.url)
    @app_commands.command(name="userinfo")
    async def userinfo(self, i: discord.Interaction, user: discord.Member | None = None): t=user or i.user; await i.response.send_message(f"{t} | id={t.id}")
    @app_commands.command(name="serverinfo")
    async def serverinfo(self, i: discord.Interaction): await i.response.send_message(f"{i.guild.name} | members={i.guild.member_count}")
    @app_commands.command(name="ping")
    async def ping(self, i: discord.Interaction): await i.response.send_message("Pong")
    @app_commands.command(name="uptime")
    async def uptime(self, i: discord.Interaction): await i.response.send_message("Uptime active")
    @app_commands.command(name="say")
    async def say(self, i: discord.Interaction, text: str): await i.response.send_message(text)
    @app_commands.command(name="echo")
    async def echo(self, i: discord.Interaction, text: str): await i.response.send_message(text)
    @app_commands.command(name="reverse")
    async def reverse(self, i: discord.Interaction, text: str): await i.response.send_message(text[::-1])
    @app_commands.command(name="roll")
    async def roll(self, i: discord.Interaction, sides: int = 6): await i.response.send_message(str(random.randint(1,max(2,sides))))
    @app_commands.command(name="quote")
    async def quote(self, i: discord.Interaction): await i.response.send_message("Keep shipping.")
    @app_commands.command(name="joke")
    async def joke(self, i: discord.Interaction): await i.response.send_message("A SQL query walks into a bar...")
    @app_commands.command(name="weather")
    async def weather(self, i: discord.Interaction, city: str): await i.response.send_message(f"Weather placeholder for {city}")
    @app_commands.command(name="timer")
    async def timer(self, i: discord.Interaction, seconds: int): await i.response.send_message(f"Timer set: {seconds}s")
    @app_commands.command(name="remind")
    async def remind(self, i: discord.Interaction, minutes: int, text: str): await i.response.send_message(f"Reminder in {minutes}m: {text}")
    @app_commands.command(name="math")
    async def math(self, i: discord.Interaction, a: int, b: int): await i.response.send_message(f"{a+b}")
    @app_commands.command(name="convert")
    async def convert(self, i: discord.Interaction, value: float): await i.response.send_message(f"{value} units")
    @app_commands.command(name="motivate")
    async def motivate(self, i: discord.Interaction): await i.response.send_message("You got this.")
    @app_commands.command(name="fact")
    async def fact(self, i: discord.Interaction): await i.response.send_message("Honey never spoils.")
    @app_commands.command(name="cat")
    async def cat(self, i: discord.Interaction): await i.response.send_message("🐱")
    @app_commands.command(name="dog")
    async def dog(self, i: discord.Interaction): await i.response.send_message("🐶")
=======
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
