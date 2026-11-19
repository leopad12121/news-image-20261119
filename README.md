# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/leopad12121/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/leopad12121/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

An entry for the [news-image-20261119 bounty on make.fun](https://make.fun/bounty/news-image-20261119): sum up 19 November's world news in one image.

A single 1024×1024 newspaper front page that sums up the world's news on
Thursday 19 November 2026. One image, five stories, drawn entirely with
Python and PIL — no photos, no network calls.

## The five stories

1. **Trump, Xi and Putin issue joint declaration** — the three leaders hold
   their first-ever three-way summit in Shenzhen at APEC and pledge dialogue
   on nuclear risks.
2. **UN top court: Myanmar committed genocide** — the International Court of
   Justice rules Myanmar committed genocide against the Rohingya.
3. **Houthi missile damages Riyadh's tower** — a Riyadh skyscraper housing
   the sovereign wealth fund is damaged in a Houthi attack.
4. **Cyclone Akvan nears India's east coast** — landfall due Friday on the
   Andhra Pradesh–Odisha coast, winds 90–100 km/h.
5. **GTA VI launches after a 13-year wait** — Grand Theft Auto VI launches
   to global fanfare.

A short "Also" strip at the bottom notes four more items from the day.

## How to run

```bash
python3 draw_news.py   # draws the front page into entry.png
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR
```

`main.py` copies the image to the directory named by the
`MAKEFUN_OUTPUT_DIR` environment variable, or to the current directory
when that variable is unset.

## Deterministic

`draw_news.py` uses fixed text, fixed colours and fixed geometry — no
random numbers, no timestamps, no network. Running it twice produces a
byte-identical `entry.png` (same SHA-256 every time).
