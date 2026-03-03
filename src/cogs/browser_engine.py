from __future__ import annotations

import asyncio
import html
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

import discord
from discord import app_commands
from discord.ext import commands


DDG_HTML_ENDPOINT = "https://duckduckgo.com/html/"
RESULT_BLOCK_RE = re.compile(
    r'<a[^>]*class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")


@dataclass(slots=True)
class SearchResult:
    title: str
    url: str


class BrowserEngine(commands.Cog):
    """High-throughput web search with in-memory filtering."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.user_cache: dict[int, list[SearchResult]] = {}

    def _fetch_page(self, query: str, offset: int) -> str:
        params = urllib.parse.urlencode({"q": query, "s": str(offset)})
        url = f"{DDG_HTML_ENDPOINT}?{params}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) PulseGuardBot/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=8) as response:  # nosec B310
            return response.read().decode("utf-8", errors="ignore")

    def _parse_results(self, doc: str) -> list[SearchResult]:
        parsed: list[SearchResult] = []
        for match in RESULT_BLOCK_RE.finditer(doc):
            raw_title = TAG_RE.sub("", match.group("title")).strip()
            title = html.unescape(raw_title)
            url = html.unescape(match.group("href")).strip()
            if title and url:
                parsed.append(SearchResult(title=title, url=url))
        return parsed

    async def _search(self, query: str, target_count: int) -> list[SearchResult]:
        target_count = max(1, min(target_count, 1000))
        pages = min(50, (target_count // 25) + 2)
        offsets = [page * 25 for page in range(pages)]

        tasks = [asyncio.to_thread(self._fetch_page, query, offset) for offset in offsets]
        raw_pages = await asyncio.gather(*tasks, return_exceptions=True)

        unique: dict[str, SearchResult] = {}
        for page in raw_pages:
            if isinstance(page, Exception):
                continue
            for result in self._parse_results(page):
                unique.setdefault(result.url, result)
                if len(unique) >= target_count:
                    return list(unique.values())
        return list(unique.values())

    def _apply_filters(
        self,
        results: list[SearchResult],
        title_contains: str | None,
        domain_contains: str | None,
        url_contains: str | None,
    ) -> list[SearchResult]:
        filtered = results
        if title_contains:
            needle = title_contains.lower()
            filtered = [r for r in filtered if needle in r.title.lower()]
        if domain_contains:
            needle = domain_contains.lower()
            filtered = [
                r
                for r in filtered
                if needle in urllib.parse.urlparse(r.url).netloc.lower()
            ]
        if url_contains:
            needle = url_contains.lower()
            filtered = [r for r in filtered if needle in r.url.lower()]
        return filtered

    def _to_embed(self, title: str, results: list[SearchResult], elapsed_s: float) -> discord.Embed:
        embed = discord.Embed(title=title, color=discord.Color.blurple())
        embed.description = f"Found **{len(results)}** results in **{elapsed_s:.2f}s**."
        lines = [f"`{idx + 1:02}` [{r.title}]({r.url})" for idx, r in enumerate(results[:20])]
        embed.add_field(name="Top matches", value="\n".join(lines) if lines else "No results.", inline=False)
        if len(results) > 20:
            embed.set_footer(text=f"Showing first 20 of {len(results)}")
        return embed

    @app_commands.command(name="browser_search", description="Search the web fast and cache results for filtering.")
    async def browser_search(
        self,
        interaction: discord.Interaction,
        query: str,
        max_results: app_commands.Range[int, 10, 1000] = 1000,
    ) -> None:
        await interaction.response.defer(thinking=True)
        started = time.perf_counter()
        results = await self._search(query=query, target_count=max_results)
        elapsed = time.perf_counter() - started
        self.user_cache[interaction.user.id] = results

        embed = self._to_embed(
            title=f"Browser Engine Results for: {query}",
            results=results,
            elapsed_s=elapsed,
        )
        note = (
            "Use `/browser_filter` to filter cached results by title/domain/url. "
            "`1000 in 10s` is a best-effort target and depends on source rate limits/network latency."
        )
        await interaction.followup.send(content=note, embed=embed)

    @app_commands.command(name="browser_filter", description="Filter your latest browser_search results.")
    async def browser_filter(
        self,
        interaction: discord.Interaction,
        title_contains: str | None = None,
        domain_contains: str | None = None,
        url_contains: str | None = None,
    ) -> None:
        cached = self.user_cache.get(interaction.user.id)
        if not cached:
            await interaction.response.send_message(
                "Run `/browser_search` first so I have results to filter.",
                ephemeral=True,
            )
            return

        started = time.perf_counter()
        filtered = self._apply_filters(
            results=cached,
            title_contains=title_contains,
            domain_contains=domain_contains,
            url_contains=url_contains,
        )
        elapsed = time.perf_counter() - started
        await interaction.response.send_message(
            embed=self._to_embed("Filtered Browser Results", filtered, elapsed)
        )
