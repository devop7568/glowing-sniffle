# PulseGuard Discord Bot

Feature-rich Discord bot with unique social intelligence systems:
- Reputation Web (trust network graph)
- Behavioral Pattern Detection
- Dynamic Identity Roles
- Server Democracy (proposals + votes)
- Social Heatmap + Forecasting

## Setup

1. Create a Discord application and bot token.
2. Enable privileged intents: `SERVER MEMBERS INTENT`, `MESSAGE CONTENT INTENT`.
3. Install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
4. Configure env vars (optional):
   - `DISCORD_GUILD_ID=...` (optional, for faster command sync)
   - `DATABASE_PATH=pulseguard.db` (optional)
5. Set bot token in `src/bot.py`:
   - `bot_token = "PASTE_YOUR_BOT_TOKEN_HERE"`
6. Run:
   - `python src/bot.py`

## Commands
- `/vouch @user reason`
- `/trustscore @user`
- `/behavior @user`
- `/propose title body`
- `/vote proposal_id yes|no`
- `/heatmap`
- `/forecast`

## Notes
- Role evolution requires roles named exactly: `Regular`, `Core Member`, `Veteran`.
- Current democracy executor stores proposals and tallies votes; extend with automated action handlers.


## Token
- Set token directly in `src/bot.py` via `bot_token`.
- Environment `DISCORD_TOKEN` is not used for startup.
