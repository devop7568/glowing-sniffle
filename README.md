# PulseGuard Discord Bot

Feature-rich Discord bot with social systems plus a high-throughput browser-search cog.

## Features
- Reputation and trust commands
- Community proposals and voting
- Economy basics (`/daily`, `/weekly`)
- Browser engine commands:
  - `/browser_search query max_results` (up to 1000, best effort)
  - `/browser_filter title_contains domain_contains url_contains`

## Setup
1. Create a Discord application and bot token.
2. Enable privileged intents:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`
3. Install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
4. Configure env vars:
   - `DISCORD_TOKEN=...`
   - `DISCORD_GUILD_ID=...` (optional, faster command sync)
   - `DATABASE_PATH=pulseguard.db` (optional)
5. Run:
   - `python src/bot.py`

## Notes
- Search throughput depends on network conditions and upstream search rate limits.
- Filtering works on the latest cached `/browser_search` results per user.
