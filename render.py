#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page (1024x1024).

Build-time only: run `python3 render.py` here to produce entry.png.
The shipped program (main.py) is a stdlib-only copy stub; it never runs this file.
Deterministic: no network, no clock, no randomness -- same bytes every run.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (16, 34, 64)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GOLD = (176, 132, 40)
TEAL = (14, 92, 92)
GREY = (96, 96, 96)
LIGHT = (232, 226, 214)
SEA = (214, 230, 238)
LAND = (216, 200, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def fit_font(draw, text, path, max_w, start, minimum=10):
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def wrap(draw, text, f, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, f, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def chip(draw, x, y, label, bg, fg=(255, 255, 255), size=11):
    f = font(SANS_B, size)
    w = int(draw.textlength(label, font=f)) + 12
    h = size + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + 6, y + 4), label, font=f, fill=fg)
    return w


def rule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# tag: CONFIRMED = officials / several outlets; REPORTED = attributed, single
# source; CLAIM = one side's claim, contested. region counts (must sum 36):
# EUROPE 9, MIDDLE EAST 3, ASIA-PACIFIC 7, AMERICAS 7, AFRICA 4, OCEANIA 2, WORLD 4.

LEADS = [
    dict(num=1, region="WORLD", beat="CLIMATE", tag="CONFIRMED", tag_bg=DARKRED,
         chip_text="COP31 \u00b7 NO DEAL",
         head="COP31 collapses: no deal in Antalya",
         body=("The EU, Britain and Panama reject a final text that never mentions "
               "fossil fuels. The longest climate summit on record ends with no pact."),
         src="Reuters \u00b7 BBC \u00b7 The Guardian"),
    dict(num=2, region="EUROPE", beat="WAR", tag="REPORTED", tag_bg=TEAL,
         chip_text="186 DRONES OVERNIGHT",
         head="Russia fires 186 drones in one night; 161 downed",
         body=("Air defences down or jam 161 of 186 strike drones overnight. A block of "
               "flats is hit in Dymer; 14 people are feared trapped."),
         src="Ukrainian Air Force \u00b7 Kyiv Independent"),
    dict(num=3, region="MIDDLE EAST", beat="WAR", tag="CLAIM", tag_bg=GOLD,
         chip_text="CLAIM VS DENIAL",
         head="Iran claims two US radars hit; Bahrain denies it",
         body=("Tehran says it destroyed two Patriot radars at Al-Riffa and Awali. "
               "Bahrain says its defences intercepted the attack; a civilian site burned."),
         src="Al Jazeera \u00b7 Reuters"),
]

TEN = [
    dict(num=4, region="ASIA-PACIFIC", beat="ELECTION", tag="REPORTED",
         head="Hong Kong elects its Election Committee",
         body="723 seats filled; turnout 98.79%, a record. 5,640 voters cast ballots.",
         src="SCMP", scene="ballot"),
    dict(num=5, region="OCEANIA", beat="CRICKET", tag="CONFIRMED",
         head="India declare 720/9, a record in New Zealand",
         body="Rahul 136, Pant 128; India lead by 352 on day four in Wellington.",
         src="Cricbuzz \u00b7 ESPNcricinfo", scene="cricket"),
    dict(num=6, region="AMERICAS", beat="FORMULA 1", tag="CONFIRMED",
         head="Verstappen wins the Las Vegas GP",
         body="35 lead changes; Norris 2nd, Piastri 3rd. His 75th win.",
         src="F1.com", scene="racecar"),
    dict(num=7, region="AMERICAS", beat="BASKETBALL", tag="CONFIRMED",
         head="Wembanyama scores 50 as the Spurs roll on",
         body="50 points, 19 rebounds, 5 blocks; Spurs beat Pelicans 114\u201391.",
         src="AP \u00b7 NBA", scene="hoops"),
    dict(num=8, region="EUROPE", beat="SEA", tag="REPORTED",
         head="Russian cargo ship Sparta II still burning",
         body="Hit by drones off Finland; towed out of Finnish waters, 16 crew safe.",
         src="Reuters \u00b7 Yle", scene="ship"),
    dict(num=9, region="ASIA-PACIFIC", beat="DISASTER", tag="REPORTED",
         head="Candy-factory fire: 3 dead, 36 missing",
         body="24 body bags recovered in Cikande; the search goes on.",
         src="Reuters \u00b7 AP", scene="fire"),
    dict(num=10, region="ASIA-PACIFIC", beat="HEALTH", tag="REPORTED",
         head="Toxic-liquor toll in Manipur climbs to 19",
         body="600 in hospital after drinking spurious liquor; six held.",
         src="AP", scene="hospital"),
    dict(num=11, region="MIDDLE EAST", beat="CONFLICT", tag="REPORTED",
         head="Gaza peace plan on the brink",
         body="Israeli fire kills four in Gaza; Hamas seeks urgent talks.",
         src="Al Jazeera \u00b7 AFP", scene="dove"),
    dict(num=12, region="AMERICAS", beat="QUAKE", tag="CONFIRMED",
         head="Peru quakes again in Jun\u00edn",
         body="M5.4 and M5.0 aftershocks on Sunday; 1 dead, 16 hurt, 170 homes damaged.",
         src="USGS \u00b7 IGP", scene="quake"),
    dict(num=13, region="EUROPE", beat="STRIKES", tag="REPORTED",
         head="France strikes enter a sixth week",
         body="Nationwide wage strikes; the government intervenes.",
         src="Reuters", scene="crowd"),
]

ALSO = [
    (14, "Estonia to shut five Russia border crossings from 1 Dec", "Reuters"),
    (15, "Denmark expels Russian attach\u00e9 over an alleged plot", "Guardian"),
    (16, "Nepal PM Balen Shah lands in Delhi on his first visit", "IANS"),
    (17, "World court rules on the Rohingya genocide", "Guardian"),
    (18, "EU and Indonesia sign a big trade deal", "DW"),
    (19, "Drones strike homes near Khartoum", "AP"),
    (20, "Kenya discharges its last Ebola patient", "Wires"),
    (21, "FBI probes a hack of its crime database", "AP"),
    (22, "Nigeria boat toll rises to 26", "AFP"),
    (23, "Violent pro-Hasina protests shake Dhaka", "AP"),
    (24, "South Korea AI cheating scandal forces minister out", "Yonhap"),
    (25, "Pope Leo XIV hosts 1,300 poor guests", "Vatican News"),
    (26, "BepiColombo enters Mercury orbit", "ESA"),
    (27, "Nvidia faces an SEC probe as AI shares slide", "CNBC"),
    (28, "Spain heads for a 29 November election", "Reuters"),
    (29, "Britain opens its gates to 100,000 young Europeans a year", "BBC"),
    (30, "Trump works on a wider Ukraine-Russia ceasefire", "AP"),
    (31, "Delta flights delayed after Atlanta hub trouble", "AP"),
    (32, "Landmine kills four children in north-west Syria", "UN"),
    (33, "Sudan war displaces 700,000 in Kordofan", "UN"),
    (34, "Melbourne marks 70 years since the 1956 Olympics", "ABC"),
    (35, "Alcaraz beats Zverev, reaches the ATP Finals decider", "ATP"),
    (36, "Lahore tops the world air-pollution ranking", "Reuters"),
]

STATS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or jammed by air defence"),
    ("35%", "clean-power goal in the rejected draft"),
    ("$120bn", "adaptation target dropped"),
    ("720/9", "India's record Test total in NZ"),
    ("723", "seats filled in Hong Kong"),
]

REGIONS = [
    ("EUROPE", 9, (30, 80, 160)),
    ("MIDDLE EAST", 3, (178, 34, 34)),
    ("ASIA-PACIFIC", 7, (14, 120, 110)),
    ("AMERICAS", 6, (196, 120, 30)),
    ("AFRICA", 4, (40, 130, 70)),
    ("OCEANIA", 2, (120, 70, 170)),
    ("WORLD", 4, (90, 90, 90)),
]

TIMELINE = ("01:00 HK polls open \u00b7 03:00 COP31 objections close \u00b7 05:30 Las Vegas GP ends \u00b7 "
            "06:00 COP31 approval session \u00b7 08:00 161 of 186 drones downed \u00b7 "
            "18:00 HK polls close")

DATE_CHECK = ("Left out on purpose \u2014 they happened on earlier days: Peru\u2019s M6.7 quake "
              "(Fri 20 Nov) \u00b7 Russia\u2019s 400-drone barrage (Thu 19\u2013Fri 20 Nov) \u00b7 "
              "\u2018El Chapo Isidro\u2019 captured (Fri 21 Nov) \u00b7 Bayelsa boat sinking (Fri 21 Nov).")

# map pins: (story number, x, y) in the 460x114 map panel
PINS = [(1, 277, 39), (2, 268, 22), (3, 295, 43), (4, 375, 46), (5, 448, 100),
        (6, 82, 34), (7, 104, 40), (8, 262, 13), (9, 365, 71), (10, 350, 44),
        (11, 274, 38), (12, 134, 76), (13, 233, 23), (14, 270, 8), (15, 246, 17),
        (16, 329, 41), (17, 360, 52), (18, 372, 78), (19, 272, 52), (20, 277, 65),
        (21, 132, 32), (22, 234, 60), (23, 340, 50), (24, 392, 33), (25, 252, 33),
        (26, 170, 8), (27, 66, 40), (28, 225, 30), (29, 224, 14), (30, 140, 38),
        (31, 122, 36), (32, 284, 30), (33, 260, 58), (34, 415, 99), (35, 244, 36),
        (36, 320, 34)]

# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    """Conference hall at dusk: long table, delegates, flags, wall clock."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 214, 180))
    d.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(214, 178, 130))
    # sun low over the hall windows
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(232, 150, 60))
    # wall clock
    cx, cy, r = x + 34, y + 26, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=2)
    d.line([(cx, cy), (cx, cy - 9)], fill=INK, width=2)
    d.line([(cx, cy), (cx + 7, cy + 3)], fill=INK, width=2)
    # flags along the back wall
    flag_cols = [(178, 34, 34), (30, 80, 160), (14, 120, 110), (196, 120, 30),
                 (120, 70, 170), (40, 130, 70)]
    for i, c in enumerate(flag_cols):
        fx = x + 78 + i * 34
        d.line([(fx, y + 12), (fx, y + 40)], fill=(90, 70, 50), width=2)
        d.polygon([(fx, y + 12), (fx + 22, y + 17), (fx, y + 23)], fill=c)
    # long table
    d.rectangle([x + 8, y + int(h * 0.62), x + w - 8, y + h - 8], fill=(122, 84, 52))
    d.rectangle([x + 8, y + int(h * 0.62), x + w - 8, y + int(h * 0.62) + 6],
                fill=(150, 108, 66))
    # paper + gavel on the table
    d.rectangle([x + w // 2 - 26, y + int(h * 0.62) - 12, x + w // 2 + 26,
                 y + int(h * 0.62) + 2], fill=(255, 255, 255), outline=(150, 150, 150))
    d.line([(x + w // 2 - 18, y + int(h * 0.62) - 7), (x + w // 2 + 18, y + int(h * 0.62) - 7)],
           fill=(120, 120, 120), width=1)
    # delegates: heads + shoulders behind the table
    skin = [(232, 190, 150), (190, 140, 100), (240, 205, 170), (160, 115, 85)]
    suits = [(40, 50, 90), (70, 70, 70), (90, 40, 40), (30, 70, 60),
             (60, 60, 110), (100, 60, 30)]
    for i in range(6):
        hx = x + 30 + i * 46
        hy = y + int(h * 0.52)
        d.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=skin[i % len(skin)])
        d.pieslice([hx - 14, hy + 6, hx + 14, hy + 26], 180, 360, fill=suits[i])
        d.rectangle([hx - 2, hy + 6, hx + 2, hy + 12], fill=(255, 255, 255))


def scene_kyiv(d, x, y, w, h):
    """Night skyline under a drone swarm: searchlights, lit windows, blasts."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 48))
    # stars
    for sx, sy in [(18, 12), (52, 22), (96, 8), (140, 16), (180, 10), (220, 20),
                   (255, 9), (285, 18), (40, 34), (160, 30), (240, 32)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(220, 220, 200))
    # moon
    d.ellipse([x + w - 42, y + 8, x + w - 18, y + 32], fill=(235, 230, 205))
    # searchlight beams from the ground
    for bx, tx in [(40, 120), (150, 90), (250, 170)]:
        d.polygon([(x + bx, y + h), (x + bx + 14, y + h), (x + tx, y + 6)],
                  fill=(250, 240, 180))
    # drones: small dark crosses with a red eye
    for dx, dy in [(70, 30), (130, 18), (190, 34), (230, 22), (100, 44), (265, 40)]:
        d.line([(x + dx - 7, y + dy), (x + dx + 7, y + dy)], fill=(10, 10, 14), width=3)
        d.line([(x + dx, y + dy - 5), (x + dx, y + dy + 5)], fill=(10, 10, 14), width=3)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=(255, 60, 40))
    # explosion glow
    ex, ey = x + w - 78, y + int(h * 0.52)
    for r, c in [(26, (255, 190, 80)), (17, (255, 130, 40)), (9, (255, 220, 130))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    # skyline with lit windows
    base = y + h
    for bx, bw, bh in [(0, 44, 52), (46, 30, 70), (78, 38, 44), (118, 34, 78),
                       (154, 42, 56), (198, 30, 66), (230, 36, 48), (268, 40, 60)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 12, 26))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                if (wx + wy) % 3:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 90))


def scene_bahrain(d, x, y, w, h):
    """Night base under missile arcs: radar dishes, explosion, sea below."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    for sx, sy in [(20, 10), (70, 20), (150, 8), (210, 14), (260, 10)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(220, 220, 200))
    d.ellipse([x + 24, y + 12, x + 44, y + 32], fill=(235, 230, 205))
    # missile arcs (orange parabolas) with fireballs
    for x0, x1, peak in [(30, 150, 26), (120, 250, 18), (200, 295, 34)]:
        pts = []
        for t in range(21):
            px = x + x0 + (x1 - x0) * t / 20
            py = y + h - 34 - (h - 34 - peak) * 4 * (t / 20) * (1 - t / 20)
            pts.append((px, py))
        d.line(pts, fill=(255, 150, 50), width=3)
        d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
                  fill=(255, 190, 80))
    # explosion at the base
    ex, ey = x + 150, y + h - 44
    for r, c in [(24, (255, 180, 70)), (15, (255, 120, 30)), (8, (255, 220, 130))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    # radar dishes
    for rx in [52, 235]:
        d.line([(x + rx, y + h - 34), (x + rx, y + h - 14)], fill=(180, 180, 180), width=3)
        d.pieslice([x + rx - 16, y + h - 52, x + rx + 16, y + h - 20], 180, 360,
                   fill=(225, 225, 225))
    # base buildings + sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(24, 40, 66))
    d.rectangle([x + 90, y + h - 52, x + 130, y + h - 34], fill=(40, 52, 74))
    d.rectangle([x + 250, y + h - 48, x + 292, y + h - 34], fill=(40, 52, 74))
    for wx in range(x + 96, x + 126, 10):
        d.rectangle([wx, y + h - 46, wx + 4, y + h - 40], fill=(255, 205, 90))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(28, 68, 96))
    for sx in range(x + 8, x + w - 8, 26):
        d.line([(sx, y + h - 5), (sx + 12, y + h - 5)], fill=(120, 180, 210), width=1)


def small_scene(d, x, y, w, h, kind):
    """One small literal scene (~190x58) for a TEN story."""
    if kind == "ballot":
        d.rectangle([x, y, x + w, y + h], fill=(196, 32, 32))
        d.rectangle([x + 18, y + 22, x + 78, y + h - 6], fill=(255, 255, 255))
        d.rectangle([x + 34, y + 14, x + 62, y + 24], fill=(255, 255, 255))
        d.rectangle([x + 40, y + 30, x + 56, y + 44], fill=(196, 32, 32))
        d.text((x + 100, y + 16), "VOTE", font=font(SANS_B, 20), fill=(255, 255, 255))
        d.text((x + 100, y + 38), "723 SEATS", font=font(SANS_B, 11), fill=(255, 220, 220))
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(56, 130, 70))
        d.rectangle([x + 70, y + 6, x + 120, y + h - 6], fill=(140, 190, 110))
        d.line([(x + 82, y + 12), (x + 82, y + h - 12)], fill=(255, 255, 255), width=2)
        d.line([(x + 108, y + 12), (x + 108, y + h - 12)], fill=(255, 255, 255), width=2)
        # stumps + bat + ball
        d.line([(x + 30, y + 30), (x + 30, y + 46)], fill=(255, 220, 90), width=3)
        d.line([(x + 36, y + 30), (x + 36, y + 46)], fill=(255, 220, 90), width=3)
        d.line([(x + 42, y + 30), (x + 42, y + 46)], fill=(255, 220, 90), width=3)
        d.polygon([(x + 52, y + 44), (x + 66, y + 20), (x + 72, y + 23), (x + 58, y + 47)],
                  fill=(190, 150, 90))
        d.ellipse([x + 150, y + 30, x + 160, y + 40], fill=(200, 40, 40))
        d.text((x + 8, y + 4), "720/9", font=font(SANS_B, 15), fill=(255, 255, 255))
    elif kind == "racecar":
        d.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
        for i in range(8):
            c = (255, 255, 255) if i % 2 == 0 else (20, 20, 20)
            d.rectangle([x + i * 12, y + 4, x + i * 12 + 12, y + 14], fill=c)
        d.polygon([(x + 30, y + 40), (x + 60, y + 28), (x + 130, y + 28),
                   (x + 160, y + 40), (x + 160, y + 48), (x + 30, y + 48)], fill=(200, 30, 30))
        d.ellipse([x + 48, y + 42, x + 66, y + 54], fill=(15, 15, 15))
        d.ellipse([x + 128, y + 42, x + 146, y + 54], fill=(15, 15, 15))
        d.rectangle([x + 66, y + 30, x + 96, y + 38], fill=(160, 210, 235))
    elif kind == "hoops":
        d.rectangle([x, y, x + w, y + h], fill=(214, 132, 44))
        d.rectangle([x + 120, y + 6, x + 132, y + h - 6], fill=(255, 255, 255))
        d.rectangle([x + 132, y + 8, x + 156, y + 26], fill=(255, 255, 255),
                    outline=(200, 60, 30), width=2)
        d.ellipse([x + 132, y + 26, x + 150, y + 34], fill=(200, 60, 30))
        d.ellipse([x + 30, y + 8, x + 70, y + 48], fill=(232, 110, 40))
        d.arc([x + 30, y + 8, x + 70, y + 48], 0, 360, fill=(255, 255, 255), width=2)
        d.text((x + 74, y + 42), "50 PTS", font=font(SANS_B, 12), fill=(255, 255, 255))
    elif kind == "ship":
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 90))
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(28, 90, 120))
        d.polygon([(x + 40, y + 34), (x + 150, y + 34), (x + 138, y + 48),
                   (x + 52, y + 48)], fill=(140, 40, 40))
        d.rectangle([x + 70, y + 18, x + 110, y + 34], fill=(200, 200, 200))
        d.ellipse([x + 118, y + 6, x + 142, y + 22], fill=(120, 120, 120))
        d.ellipse([x + 124, y + 2, x + 136, y + 12], fill=(160, 160, 160))
        d.text((x + 6, y + 4), "SPARTA II", font=font(SANS_B, 10), fill=(255, 220, 150))
    elif kind == "fire":
        d.rectangle([x, y, x + w, y + h], fill=(40, 32, 28))
        d.rectangle([x + 20, y + 26, x + 120, y + h - 6], fill=(120, 90, 70))
        d.rectangle([x + 20, y + 26, x + 120, y + 32], fill=(90, 65, 50))
        for fx, fh in [(40, 26), (62, 34), (86, 28), (106, 22)]:
            d.polygon([(x + fx - 9, y + 30), (x + fx, y + 30 - fh), (x + fx + 9, y + 30)],
                      fill=(255, 150, 40))
            d.polygon([(x + fx - 4, y + 30), (x + fx, y + 30 - fh + 12), (x + fx + 4, y + 30)],
                      fill=(255, 220, 90))
        d.ellipse([x + 140, y + 6, x + 170, y + 26], fill=(120, 120, 120))
    elif kind == "hospital":
        d.rectangle([x, y, x + w, y + h], fill=(235, 235, 230))
        d.rectangle([x + 14, y + 12, x + 90, y + h - 8], fill=(255, 255, 255),
                    outline=(180, 180, 180))
        d.rectangle([x + 44, y + 18, x + 60, y + 44], fill=(200, 40, 40))
        d.rectangle([x + 34, y + 26, x + 70, y + 36], fill=(200, 40, 40))
        d.text((x + 104, y + 12), "19 DEAD", font=font(SANS_B, 15), fill=(178, 34, 34))
        d.text((x + 104, y + 32), "600 IN HOSPITAL", font=font(SANS_B, 10), fill=INK)
    elif kind == "dove":
        d.rectangle([x, y, x + w, y + h], fill=(150, 190, 205))
        d.ellipse([x + 60, y + 16, x + 130, y + 44], fill=(255, 255, 255))
        d.ellipse([x + 118, y + 10, x + 140, y + 26], fill=(255, 255, 255))
        d.polygon([(x + 138, y + 16), (x + 152, y + 20), (x + 138, y + 22)], fill=(230, 160, 40))
        d.polygon([(x + 70, y + 18), (x + 40, y + 6), (x + 52, y + 26)], fill=(245, 245, 245))
        d.polygon([(x + 76, y + 40), (x + 52, y + 52), (x + 84, y + 48)], fill=(245, 245, 245))
        d.ellipse([x + 128, y + 16, x + 132, y + 20], fill=INK)
        d.text((x + 8, y + 2), "TALKS?", font=font(SANS_B, 12), fill=(255, 255, 255))
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(110, 120, 130))
        d.polygon([(x, y + h), (x + 50, y + 8), (x + 100, y + h)], fill=(90, 80, 70))
        d.polygon([(x + 90, y + h), (x + 140, y + 18), (x + 190, y + h)], fill=(70, 62, 54))
        d.polygon([(x + 42, y + 16), (x + 50, y + 8), (x + 58, y + 16)], fill=(255, 255, 255))
        d.line([(x + 60, y + 40), (x + 90, y + 30), (x + 110, y + 44), (x + 130, y + 28)],
               fill=(255, 60, 40), width=3)
        d.text((x + 8, y + 4), "M5.4", font=font(SANS_B, 14), fill=(255, 255, 255))
    elif kind == "crowd":
        d.rectangle([x, y, x + w, y + h], fill=(70, 90, 130))
        d.polygon([(x + 150, y + 6), (x + 158, y + 6), (x + 158, y + 40),
                   (x + 150, y + 40)], fill=(60, 60, 60))
        d.polygon([(x + 142, y + 6), (x + 166, y + 14), (x + 150, y + 22)], fill=(200, 60, 60))
        for i, (px, c) in enumerate([(30, (220, 60, 60)), (70, (255, 255, 255)),
                                     (110, (60, 160, 90))]):
            d.rectangle([x + px, y + 18, x + px + 26, y + 34], fill=c)
            d.line([(x + px + 13, y + 34), (x + px + 13, y + 48)], fill=(90, 70, 50), width=2)
        for i in range(7):
            hx = x + 16 + i * 24
            d.ellipse([hx - 8, y + 38, hx + 8, y + 54], fill=(232, 190, 150))
        d.text((x + 8, y + 4), "WEEK 6", font=font(SANS_B, 12), fill=(255, 255, 255))
    else:
        d.rectangle([x, y, x + w, y + h], fill=LIGHT)

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(28, 18), (60, 8), (105, 10), (130, 20), (118, 34), (95, 40), (70, 48),
     (45, 42), (25, 30)],  # North America
    [(128, 6), (142, 4), (146, 12), (134, 14)],  # Greenland
    [(105, 58), (125, 56), (138, 68), (128, 92), (112, 100), (100, 78)],  # S America
    [(215, 18), (240, 10), (258, 16), (250, 30), (228, 32), (214, 26)],  # Europe
    [(218, 42), (245, 38), (262, 48), (258, 72), (240, 88), (226, 74), (214, 56)],  # Africa
    [(260, 12), (330, 6), (400, 10), (430, 22), (415, 38), (380, 44), (340, 40),
     (300, 44), (268, 32)],  # Asia
    [(360, 52), (378, 50), (384, 58), (366, 60)],  # SE Asia islands
    [(375, 78), (405, 74), (420, 84), (400, 96), (378, 90)],  # Australia
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    for poly in CONTINENTS:
        pts = [(x + px, y + py) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(170, 150, 110))
    f = font(SANS_B, 7)
    for num, px, py in PINS:
        cx, cy = x + px, y + py
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=(255, 255, 255))
        t = str(num)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 4), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    CW = W - 2 * M  # 976

    # --- kicker bar
    y = 10
    d.text((M, y), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    f_small = font(SANS_B, 11)
    d.text((W - M - d.textlength(right, font=f_small), y + 1), right,
           font=f_small, fill=INK)
    rule(d, M, 30, CW, width=2)

    # --- GAP A: the DATE is the masthead (criterion 1, first-weighed)
    date_text = "Sunday 22 November 2026"
    f_date = fit_font(d, date_text, DISPLAY, CW, 80)
    y = 34
    d.text(((W - d.textlength(date_text, font=f_date)) / 2, y), date_text,
           font=f_date, fill=NAVY)
    y += 78

    # --- red italic deck
    deck = ("COP31 ends with no deal \u00b7 186 drones over Ukraine in the night \u00b7 "
            "Iran\u2019s radar claim meets Bahrain\u2019s denial")
    f_deck = fit_font(d, deck, SERIF_I, CW, 20)
    d.text(((W - d.textlength(deck, font=f_deck)) / 2, y), deck, font=f_deck, fill=RED)
    y += 24
    rule(d, M, y, CW, width=1)
    y += 5

    # --- stat strip: six big numbers
    cell = CW // 6
    f_num = font(SERIF_B, 28)
    f_cap = font(SANS, 10)
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cell
        tw = d.textlength(num, font=f_num)
        d.text((cx + (cell - tw) / 2, y), num, font=f_num, fill=RED)
        for j, ln in enumerate(wrap(d, cap, f_cap, cell - 10)):
            lw = d.textlength(ln, font=f_cap)
            d.text((cx + (cell - lw) / 2, y + 33 + j * 12), ln, font=f_cap, fill=INK)
        if i:
            d.line([(cx, y + 2), (cx, y + 52)], fill=(200, 190, 170), width=1)
    y += 56

    # --- region bar with counts
    bar_h = 18
    bx = M
    f_reg = font(SANS_B, 11)
    for name, count, col in REGIONS:
        label = "%s %d" % (name, count)
        wch = int(d.textlength(label, font=f_reg)) + 14
        d.rectangle([bx, y, bx + wch, y + bar_h], fill=col)
        d.text((bx + 7, y + 3), label, font=f_reg, fill=(255, 255, 255))
        bx += wch + 3
    y += bar_h + 4

    # --- UTC timeline strip
    d.rectangle([M, y, M + CW, y + 18], fill=NAVY)
    f_tl = font(SANS_B, 11)
    tl = "THE DAY IN UTC   " + TIMELINE
    while d.textlength(tl, font=f_tl) > CW - 8 and f_tl.size > 9:
        f_tl = font(SANS_B, f_tl.size - 1)
    d.text((M + 6, y + 3), tl, font=f_tl, fill=(255, 255, 255))
    y += 22

    # --- GAP B: three leads with literal scenes
    lead_w = (CW - 2 * 12) // 3
    lead_y = y
    illo_h = 112
    scenes = [scene_cop31, scene_kyiv, scene_bahrain]
    lead_end = lead_y
    for i, lead in enumerate(LEADS):
        lx = M + i * (lead_w + 12)
        scenes[i](d, lx, lead_y, lead_w, illo_h)
        ty = lead_y + illo_h + 6
        chip(d, lx, ty, lead["chip_text"], lead["tag_bg"], size=10)
        tag = lead["tag"]
        tw = d.textlength(tag, font=font(SANS_B, 10))
        d.text((lx + lead_w - tw, ty + 2), tag, font=font(SANS_B, 10), fill=GREY)
        ty += 22
        f_head = font(SERIF_B, 21)
        ty = text_block(d, lx, ty, lead["head"], f_head, lead_w, leading=24, max_lines=2)
        ty += 2
        f_body = font(SERIF, 13)
        ty = text_block(d, lx, ty, lead["body"], f_body, lead_w, leading=16, max_lines=3)
        ty += 2
        d.text((lx, ty), "%d \u00b7 %s \u00b7 %s \u00b7 %s" % (
            lead["num"], lead["region"], lead["beat"], lead["src"]),
            font=font(SANS, 10), fill=GREY)
        lead_end = max(lead_end, ty + 12)
    y = lead_end
    rule(d, M, y, CW, width=1)
    y += 5

    # --- GAP C: THE DAY IN TEN, ten literal mid-size scenes
    d.text((M, y), "THE DAY IN TEN", font=font(SANS_B, 13), fill=RED)
    right = "THE STORIES THAT MOVED THE WORLD TODAY"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 11)), y + 1), right,
           font=font(SANS_B, 11), fill=INK)
    y += 17
    ten_w = (CW - 4 * 8) // 5
    ten_h = 116
    for row in range(2):
        for col in range(5):
            s = TEN[row * 5 + col]
            cx = M + col * (ten_w + 8)
            cy = y + row * (ten_h + 4)
            small_scene(d, cx, cy, ten_w, 48, s["scene"])
            ty = cy + 51
            d.text((cx, ty), "%d \u00b7 %s" % (s["num"], s["region"]),
                   font=font(SANS_B, 9), fill=RED)
            ty += 11
            ty = text_block(d, cx, ty, s["head"], font(SERIF_B, 12), ten_w,
                            leading=13, max_lines=2)
            ty = text_block(d, cx, ty, s["body"], font(SERIF, 10), ten_w,
                            leading=11, max_lines=2)
            if ty + 8 <= cy + ten_h:
                d.text((cx, ty), s["src"], font=font(SANS, 8), fill=GREY)
    y += 2 * ten_h + 8 + 2

    # --- ALSO: 23 more stories, 3 columns
    d.text((M, y), "ALSO ON SUNDAY 22 NOVEMBER \u2014 23 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    y += 15
    col_w = (CW - 2 * 16) // 3
    f_also = font(SERIF, 10)
    rows = 8
    for i, (num, title, src) in enumerate(ALSO):
        col = i // rows
        r = i % rows
        ax = M + col * (col_w + 16)
        ay = y + r * 12
        line = "%d %s (%s)" % (num, title, src)
        while d.textlength(line, font=f_also) > col_w and len(title) > 12:
            title = title[:-1].rstrip()
            line = "%d %s\u2026 (%s)" % (num, title, src)
        d.text((ax, ay), line, font=f_also, fill=INK)
    y += rows * 12 + 5
    rule(d, M, y, CW, width=1)
    y += 5

    # --- bottom band: map + date check
    band_h = H - M - y - 13
    map_w = 440
    d.text((M, y), "WHERE IT HAPPENED \u2014 PINS MATCH STORY NUMBERS",
           font=font(SANS_B, 11), fill=INK)
    draw_map(d, M, y + 15, map_w, band_h - 15)
    dx = M + map_w + 16
    dw = W - M - dx
    d.rectangle([dx, y, dx + dw, y + band_h], outline=RED, width=2)
    d.text((dx + 10, y + 6), "DATE CHECK \u2014 READ THIS FIRST",
           font=font(SANS_B, 12), fill=RED)
    ty = text_block(d, dx + 10, y + 25, DATE_CHECK, font(SERIF, 11), dw - 20,
                    leading=13)
    ty += 5
    rule(d, dx + 10, ty, dw - 20, fill=(200, 190, 170), width=1)
    ty += 5
    text_block(d, dx + 10, ty,
               "TAGS \u2014 CONFIRMED: officials or several outlets. REPORTED: attributed, "
               "single source. CLAIM: one side\u2019s claim, contested.",
               font(SANS, 10), dw - 20, fill=INK, leading=12)

    # --- footer
    fy = H - 14
    d.text((M, fy), "Sources: Reuters, BBC, Al Jazeera, The Guardian, AP, SCMP, Cricbuzz, "
                    "F1.com, NBA, USGS.",
           font=font(SANS, 9), fill=GREY)
    foot_r = "ALL 36 STORIES DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - M - d.textlength(foot_r, font=font(SANS_B, 9)), fy), foot_r,
           font=font(SANS_B, 9), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    render()
