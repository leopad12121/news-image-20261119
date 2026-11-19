# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/leopad12121/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/leopad12121/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Wednesday 19 November 2026: Xi
greets Trump on the tarmac in Shenzhen ahead of the first-ever three-way
summit with Putin, Iran hits back at US bases in Kuwait and Bahrain, Israel
opens a new operation in central Gaza, Democrat Mary Peltola flips the
Alaska Senate seat, and Cyclone Akvan bears down on India.

`draw_news.py` draws the front page (`entry.png`, 1024×1024) from the day's
reported stories; `main.py` is the entrypoint the grader runs — it copies
`entry.png` to the output directory. Standard library only, no network,
deterministic.

## Run it

```sh
python3 draw_news.py        # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261119)</sub>
