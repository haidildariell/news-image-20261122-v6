[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v6/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/haidildariell/news-image-20261122-v6/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — The World in One Day (v6)

One image summing up the world's news of Sunday 22 November 2026, drawn
as a one-page newspaper front page: the date itself is the masthead,
followed by a six-number stat strip, a region bar, a UTC timeline, three
illustrated lead stories, ten more illustrated stories, 23 further stories,
a numbered world map, and a date check that names what was left out because
it happened on an earlier day.

## Layout

- Masthead: `Sunday 22 November 2026` in full width — the day the page sums up.
- Leads: COP31 ends with no deal (Antalya); Russia fires 186 drones at
  Ukraine in one night, 161 downed; Iran claims two US radars hit in
  Bahrain, Bahrain denies it.
- 36 stories across 7 regions, each tagged CONFIRMED / REPORTED / CLAIM
  and sourced (Reuters, BBC, Al Jazeera, The Guardian, AP, SCMP, and more).

## Files

- `main.py` — the entry program (stdlib only): copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.
- `render.py` — the build-time renderer (Pillow). Run `python3 render.py`
  in this directory to regenerate `entry.png` byte-identically.
- `entry.png` — the 1024x1024 front page (under 1 MiB).

## Build

```sh
python3 render.py          # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
