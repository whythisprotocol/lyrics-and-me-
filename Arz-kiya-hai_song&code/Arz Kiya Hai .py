import time
import sys
import pygame
import shutil
import os

# ─── ANSI Colors ───────────────────────────────────────────────
COLORS = [
    "\033[91m", "\033[92m", "\033[93m", "\033[94m",
    "\033[95m", "\033[96m", "\033[97m",
]
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
ITALIC = "\033[3m"

# ─── Tuning knobs ──────────────────────────────────────────────
AUTO_FIT    = True
TAIL_PAUSE  = 0.40
MIN_DELAY   = 0.32
BLOCK_SIZE  = 5
BLOCK_GAP   = 2

# ─── Audio buffer (smaller = less latency) ─────────────────────
AUDIO_FREQ     = 44100
AUDIO_SIZE     = -16
AUDIO_CHANNELS = 2
AUDIO_BUFFER   = 512   # ~11.6ms latency (default 1024 = ~23ms)


def term_width():
    return shutil.get_terminal_size((100, 20)).columns


def precise_wait(target_time, start_time):
    """High-resolution wait: sleeps while far, busy-waits near target."""
    while True:
        now = time.perf_counter() - start_time
        remaining = target_time - now
        if remaining <= 0:
            break
        if remaining > 0.005:
            time.sleep(0.001)
        # else: busy-wait for the last 5ms for sub-ms precision


def type_line(text, color, word_delay, width, special=False):
    words = text.split()
    buffer = ""
    for word in words:
        buffer += word + " "
        current = buffer.rstrip()
        if special:
            display = f"▌ {current}"
            sys.stdout.write("\r" + " " * width)
            sys.stdout.write("\r" + f"  {color}{BOLD}{ITALIC}{display}{RESET}")
        else:
            sys.stdout.write("\r" + " " * width)
            sys.stdout.write("\r" + f"  {color}{BOLD}{current}{RESET}")
        sys.stdout.flush()
        time.sleep(word_delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def play_tune(duration, width):
    bars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"]
    label = "♪  T U N E   P L A Y I N G  ♪"
    wave_len = 12
    total_visible = len(label) + 3 + wave_len
    pad = max((width - total_visible) // 2, 0)
    end_time = time.perf_counter() + duration
    frame = 0
    sys.stdout.write("\n")
    sys.stdout.flush()
    while time.perf_counter() < end_time:
        wave = "".join(bars[(frame + i * 2) % len(bars)] for i in range(wave_len))
        line = f"\033[95m{DIM}{label}\033[0m   \033[96m{wave}\033[0m"
        sys.stdout.write("\r" + " " * width + "\r" + " " * pad + line)
        sys.stdout.flush()
        frame += 1
        time.sleep(0.08)
    sys.stdout.write("\r" + " " * width + "\r\n")
    sys.stdout.flush()


def play_with_lyrics(audio_file, lyrics_data):
    # ── Pre-init with small buffer to minimize audio latency ──
    pygame.mixer.pre_init(AUDIO_FREQ, AUDIO_SIZE, AUDIO_CHANNELS, AUDIO_BUFFER)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    width = term_width()
    # ── High-resolution clock ──
    start_time = time.perf_counter()

    os.system("cls" if os.name == "nt" else "clear")
    title = "🎵  A R Z   K I Y A   H A I  🎵"
    print(" " * ((width - len(title)) // 2) + f"{BOLD}\033[95m{title}{RESET}")
    subtitle = "— Anuv Jain —"
    print(" " * ((width - len(subtitle)) // 2) + f"{DIM}{ITALIC}{subtitle}{RESET}")
    print("─" * width)

    lines_in_block = 0
    color_index = 0
    last_resync = 0.0

    SPECIAL_LINES = {
        "Doobe dilon ki kya nau banu",
        "Main khud tair paun na aankhon mein",
    }

    for i, (timestamp, line, word_delay) in enumerate(lyrics_data):
        # ── Optional drift correction against audio clock ──
        # If we've drifted more than 150ms from actual audio position, resync.
        audio_pos = pygame.mixer.music.get_pos() / 1000.0
        if audio_pos > 0:
            wall_elapsed = time.perf_counter() - start_time
            drift = wall_elapsed - audio_pos
            if abs(drift) > 0.15 and (wall_elapsed - last_resync) > 5.0:
                start_time = time.perf_counter() - audio_pos
                last_resync = wall_elapsed

        # ── Precise wait until timestamp ──
        precise_wait(timestamp, start_time)

        if line.strip().startswith(("🎵", "♪")):
            next_ts = lyrics_data[i + 1][0] if i + 1 < len(lyrics_data) else timestamp + 3
            play_tune(max(next_ts - timestamp, 1.0), width)
            lines_in_block = 0
            continue

        is_special = line.strip() in SPECIAL_LINES
        n_words = len(line.split())

        if AUTO_FIT and i + 1 < len(lyrics_data) and n_words > 0:
            next_ts   = lyrics_data[i + 1][0]
            available = next_ts - timestamp - TAIL_PAUSE
            if is_special:
                available -= 0.3
            if available > 0:
                fitted = max(min(word_delay, available / n_words), MIN_DELAY)
            else:
                fitted = MIN_DELAY
        else:
            fitted = word_delay

        if lines_in_block >= BLOCK_SIZE:
            print("\n" * BLOCK_GAP, end="")
            lines_in_block = 0

        color = COLORS[color_index % len(COLORS)]
        color_index += 1

        type_line(line, color, fitted, width, special=is_special)
        lines_in_block += 1

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    print("─" * width)
    end = "✨  Ishq mein tere hain faiz bane  ✨"
    print(" " * (width - len(end)) + f"{BOLD}\033[96m{end}{RESET}")


# ─── Lyrics ────────────────────────────────────────────────────
lyrics = [
    (0.0,    "🎵  Music is playing tune...  🎵", 0.10),

    (28.43,  "Kayar joh the woh shayar bane", 0.55),
    (33.00,  "Ab kya kya kare yeh ishq mein", 0.55),
    (38.00,  "Na kehte the kuch joh lage khoj mein", 0.50),
    (43.50,  "Kya lafz chune naye aashiq yeh", 0.55),
    (48.00,  "Ishq mein tere hai faiz bane", 0.55),

    (52.50,  "Arz kiya hai, humne bhi likha kuch tere baare mein", 0.48),
    (59.50,  "Aise tu lage ki gulaab hai", 0.55),
    (63.80,  "Aur aise tu lage ki gulaab hai", 0.55),
    (68.20,  "Baaghon mein dil ke khilke in fizaon mein chaaye ho, haaye", 0.45),
    (73.50,  "Aur vaise hum toh tere hi ghulam hai", 0.55),

    (79.50,  "Aur vaise hum toh tere hi ghulam hai", 0.55),
    (85.50,  "Badshah dil ke teri baazi mein joh tu chahe toh", 0.50),

    (91.00,  "Doobe dilon ki kya nau banu", 0.50),
    (95.00,  "Main khud tair paun na aankhon mein", 0.50),

    (99.50,  "Shayar ki fitrat mein hi doobna", 0.55),
    (104.00, "Main kya hi ladun toofano se", 0.55),
    (108.50, "Ishq mein tere hai faiz bane", 0.55),
    (113.00, "Arz kiya hai, humne bhi likha kuch tere baare mein", 0.48),
    (119.50, "Haathon ko sambhaale mere haathon mein", 0.55),

    (124.00, "Kaise haathon ko sambhaale mere haathon mein", 0.55),
    (128.50, "Jab tak neend na aaye in lakeeron mein baatein ho, haaye", 0.45),
    (134.50, "🎵  Sa Re Pa Ga Re Sa...  🎵", 0.10),

    (142.00, "Haan, sabne toh sab keh diya hai", 0.55),
    (146.50, "Kya hi kahun joh abhi bhi ankaha hai", 0.55),
    (151.00, "Main haaye na Mirza, na Mir", 0.55),
    (155.00, "Na mahir, na zahir, karun kuch naya main", 0.52),
    (159.50, "Haaye, par joh bhi likha hai, jiya hai", 0.55),

    (164.00, "Haan, jiya hai", 0.60),
    (167.00, "Aise, aise, aise, kaise, vaise, jaise", 0.50),
    (171.00, "Jaise main padhun mere dil mein joh", 0.55),
    (175.00, "Meri aankhen bhi padhein teri aankhon ko", 0.55),
    (179.00, "Kya yeh mehfil mein baithe? Ya uthe daud jaane ko? Haaye", 0.45),

    (184.00, "Teri aankhon mein taarifon ki talaash hai", 0.55),
    (188.50, "Meri mehfil tere jaane se veeraan hai", 0.55),
    (193.00, "Main bas shayar bana hoon", 0.55),
    (196.50, "Sirf tu sunne aaye to...", 0.60),
    (200.50, "Shayad shayar bana hoon", 0.55),
    (204.00, "Sirf tu sunne aaye to", 0.60),
]

play_with_lyrics("Arz Kiya Hai .mp3", lyrics)