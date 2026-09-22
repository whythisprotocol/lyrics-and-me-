import time
import sys
import pygame
import shutil
import os

# ─── Force a low-latency audio driver on Windows ──────────────
# Must be set BEFORE pygame.mixer.init()
if os.name == "nt":
    os.environ["SDL_AUDIODRIVER"] = "wasapi"

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
AUTO_FIT      = True
TAIL_PAUSE    = 0.40
MIN_DELAY     = 0.32
BLOCK_SIZE    = 5
BLOCK_GAP     = 2
GLOBAL_OFFSET = 0.0     # + = lyrics later, − = lyrics earlier (±0.2 steps)

# ─── Audio buffer (larger = no cracking, smaller = less lag) ──
AUDIO_FREQ     = 44100
AUDIO_SIZE     = -16
AUDIO_CHANNELS = 2
AUDIO_BUFFER   = 1024   # ~23ms — safe, no crack


def term_width():
    return shutil.get_terminal_size((100, 20)).columns


def precise_wait(target_time, start_time):
    """High-resolution wait: sleeps while far, busy-waits near target."""
    while True:
        now = time.perf_counter() - start_time
        remaining = target_time - now
        if remaining <= 0:
            break
        if remaining > 0.015:
            time.sleep(0.001)
        # else: busy-wait for the last 15ms for sub-ms precision


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
    title = "🎵  S I T A A R E  🎵"
    print(" " * ((width - len(title)) // 2) + f"{BOLD}\033[95m{title}{RESET}")
    subtitle = "— Arijit Singh —"
    print(" " * ((width - len(subtitle)) // 2) + f"{DIM}{ITALIC}{subtitle}{RESET}")
    print("─" * width)

    lines_in_block = 0
    color_index = 0
    last_resync = 0.0

    SPECIAL_LINES = {
        "Sitaare, sitaare",
        "Adhoore adhoore",
    }

    for i, (timestamp, line, word_delay) in enumerate(lyrics_data):
        # ── Optional drift correction against audio clock ──
        audio_pos = pygame.mixer.music.get_pos() / 1000.0
        if audio_pos > 0:
            wall_elapsed = time.perf_counter() - start_time
            drift = wall_elapsed - audio_pos
            if abs(drift) > 0.15 and (wall_elapsed - last_resync) > 5.0:
                start_time = time.perf_counter() - audio_pos
                last_resync = wall_elapsed

        # ── Precise wait until timestamp (+ user offset) ──
        precise_wait(timestamp + GLOBAL_OFFSET, start_time)

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
    end = "✨  Bas tum se milne ki der thi  ✨"
    print(" " * (width - len(end)) + f"{BOLD}\033[96m{end}{RESET}")


# ─── Lyrics ────────────────────────────────────────────────────
# Timestamps taken from SRT, matched to English lyrics.
# 🎵 = instrumental section → animated tune bars play for the whole gap.
lyrics = [
    # ── Intro (instrumental) ──
    (0.0,    "🎵  Music is playing tune...  🎵", 0.10),

    # ── Opening refrain ──
    (14.58,  "Bas tum se milne ki", 0.85),
    (17.25,  "Der thi", 0.90),
    (21.16,  "Bas tum se milne ki", 0.85),
    (23.70,  "Der thi", 0.90),
    (27.89,  "Bas tum se milne ki", 0.85),
    (30.59,  "Der thi", 0.90),
    (33.72,  "Vo bas tum se milne", 0.80),
    (36.24,  "Ki der thi", 0.85),

    # ── Sitaare refrain ──
    (40.84,  "Sitaare, sitaare", 0.75),
    (44.39,  "Mile hain sitaare", 0.75),
    (46.77,  "Tabhi toh huye hain", 0.70),
    (50.15,  "Nazaare tumhare", 0.75),
    (54.42,  "Sitaare, sitaare", 0.75),
    (56.55,  "Mile hain sitaare", 0.75),
    (58.68,  "Tabhi toh huye hain", 0.70),
    (60.81,  "Nazaare tumhare", 0.75),

    # ── Second round of title line ──
    (65.13,  "Bas tum se milne ki der thi", 0.80),
    (70.66,  "Tum se milne ki der thi", 0.80),
    (73.20,  "Tum se milne ki der thi", 0.80),

    (76.02,  "Bas tum se milne ki der thi", 0.80),
    (81.28,  "Tum se milne ki der thi", 0.80),
    (85.69,  "Tum se milne ki der thi", 0.80),

    # ── Instrumental break 1 (92.6s → 121.3s) ──
    (92.61,  "🎵  Music is playing tune...  🎵", 0.10),

    # ── Verse 1 ──
    (121.26, "Jis pe rakhe tum ne kadam", 0.75),
    (124.07, "Ab se mera bhi raasta hai", 0.75),
    (126.88, "Jaise mera tum se koi", 0.75),
    (129.68, "Pichhle janam ka vaasta hai", 0.75),

    (135.30, "Jis pe rakhe tum ne kadam", 0.75),
    (138.10, "Ab se mera bhi raasta hai", 0.75),
    (140.91, "Jaise mera tum se koi", 0.75),
    (143.72, "Pichhle janam ka vaasta hai", 0.75),

    # ── Adhoore adhoore (bridge) ──
    (152.66, "Adhoore adhoore", 0.80),
    (155.15, "Thhe vo din humare", 0.75),
    (157.82, "Tumhare bina jo", 0.75),
    (160.49, "Guzaare thhe saare", 0.75),

    # ── Sitaare refrain (2nd) ──
    (162.90, "Sitaare, sitaare", 0.75),
    (165.00, "Mile hain sitaare", 0.75),
    (167.65, "Tabhi toh huye hain", 0.70),
    (170.00, "Nazaare tumhare", 0.75),

    # ── Final title repeats ──
    (175.58, "Tum se milne ki der thi", 0.80),
    (181.15, "Bas tum se milne ki der thi", 0.80),
    (183.68, "Bas tum se milne ki der thi", 0.80),

    (192.27, "Tum se milne ki der thi", 0.80),
    (194.63, "Tum se milne ki der thi", 0.80),
    (197.22, "Tum se milne ki der thi", 0.80),

    # ── Instrumental break 2 (203.2s → 232.0s) ──
    (203.24, "🎵  Music is playing tune...  🎵", 0.10),

    # ── Outro (instrumental till end) ──
    (231.99, "🎵  Music is playing tune...  🎵", 0.10),
]
# ─── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    audio_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Sithaare .mp3"
    )
    if not os.path.isfile(audio_path):
        print(f"❌ Audio file not found:\n   {audio_path}")
        sys.exit(1)
    print(f"🎧 Loading: {audio_path}")
    play_with_lyrics(audio_path, lyrics)