---<img width="2560" height="1440" alt="banner yt (2)" src="https://github.com/user-attachments/assets/8c281b2a-557c-4228-b134-4f13dd5c7e7e" />


<div align="center">

# 🎵 Lyrics & Me




</div>

---

## ✨ What is Lyrics & Me?

**Lyrics & Me** is a terminal-based lyrics player that syncs **word-by-word** with your music. No GUI, no browser, no clutter — just you, the song, and the words lighting up in color as they're sung.

> *"Terminal lyrics player: synced word-by-word lyrics for any song, in your terminal, in color."*

Perfect for:
- 🎧 Late-night music sessions
- 💻 Coding while vibing to lyrics
- 📼 Reliving that one song you can't stop playing
- 🎨 Showing off your terminal to friends

---

## 📸 Preview

<div align="center">

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c0fef945-80ee-4766-badc-350acacd219d" />


</div>

> 💡 *Replace the image URLs above with your own screenshots or GIFs.*

---

## 🚀 Features

| | Feature | Description |
|---|---------|-------------|
| 🎤 | **Word-by-word sync** | Lyrics type out in perfect rhythm with the audio |
| 🎨 | **ANSI color magic** | Every line gets its own color, special lines pop with italics |
| ⏱️ | **Auto-fit timing** | Typing speed adjusts per line — no lag, no rush |
| 🎧 | **Low-latency audio** | Tuned pygame buffer (512 samples) for tight sync |
| 🔁 | **Drift correction** | Re-syncs against the audio clock if timing ever slips |
| 🎼 | **Multi-song support** | Add any song with a simple timestamp list |
| 🎹 | **Tune interludes** | Animated equalizer bars during instrumental breaks |
| 🌈 | **Zero dependencies bloat** | Just Python + pygame |



## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/whythisprotocol/lyrics-and-me-.git
cd lyrics-and-me-
```

### 2. Install dependencies

```bash
pip install pygame
```

### 3. Add your song

Drop your `.mp3` file into the project folder.

### 4. Run it

```bash
python player.py
```

---

## 🎼 Adding a New Song

Adding a song takes **30 seconds**. Just create a list of `(timestamp, line, word_delay)` tuples:

```python
my_song = [
    (0.0,   "🎵  Music is playing...  🎵", 0.10),
    (12.5,  "First line of the song",       0.55),
    (16.2,  "Second line here",             0.55),
    (20.8,  "You get the idea",             0.55),
    (25.0,  "♪  Instrumental break  ♪",     0.10),
    (32.4,  "Back to the lyrics now",       0.55),
]

play_with_lyrics("My Song.mp3", my_song)
```

**Pro tip:** Use a tool like [lyricstimestamp.com](https://lyricstimestamp.com) to grab timestamps quickly, or tap along in your music player to find them.

---

## 🎶 Songs Included

| 🎵 Song | 🎤 Artist | 📁 File |
|---------|-----------|---------|
| **Arz Kiya Hai** | Anuv Jain | `Arz Kiya Hai .mp3` |
| *(your next song)* | — | — |

> Want your song featured here? Open a PR! 🎉

---

## 🛠️ Configuration

Tune the experience to your taste — all knobs live at the top of `player.py`:

| ⚙️ Knob | Default | What it does |
|---------|---------|--------------|
| `AUTO_FIT` | `True` | Auto-adjust typing speed per line |
| `MIN_DELAY` | `0.32` | Fastest allowed per-word delay |
| `TAIL_PAUSE` | `0.40` | Pause before next line starts |
| `AUDIO_BUFFER` | `512` | Audio latency (lower = tighter sync) |
| `BLOCK_SIZE` | `5` | Lines per visual block before gap |
| `BLOCK_GAP` | `2` | Blank lines between lyric blocks |

### 🎯 Sync feels off?

- **Lyrics appear late?** → Lower `MIN_DELAY` to `0.28`
- **Lyrics appear early?** → Raise it to `0.35`
- **Audio sounds choppy?** → Raise `AUDIO_BUFFER` to `1024`

---

## 📁 Project Structure

```
lyrics-and-me-/
├── Arz-kiya-hai_song&code/
│   ├── Arz Kiya Hai .m4a     # Audio file
│   └── Arz Kiya Hai .py      # Lyrics + player script
├── LICENSE                    # MIT License
└── README.md                  # You're reading it
```



## 🤝 Contributing

Contributions make the open-source world beautiful. Here's how you can help:

1. 🍴 **Fork** the repo
2. 🌿 **Create** your branch: `git checkout -b feature/NewSong`
3. ✏️ **Add** your song + timestamps
4. 💾 **Commit**: `git commit -m "Add: Song Name by Artist"`
5. 🚀 **Push**: `git push origin feature/NewSong`
6. 🎉 **Open** a Pull Request

Have an idea for a feature? Open an issue — let's talk.

---

## 📜 License

Released under the **MIT License** — free to use, remix, and add your own songs.

See [LICENSE](LICENSE) for details.

---

## ⭐ Show Your Support

If this project made your terminal a little more magical:

- ⭐ **Star** this repo
- 🐦 **Share** it with a friend
- 🎵 **Add** your favorite song and open a PR

---

<div align="center">

### 💖 Made for people who love lyrics more than GUIs.

**— whythisprotocol —**

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,24&height=120&section=footer" width="100%" />

</div>
```

---

## 🖼️ How to Add Your Images

Replace these placeholders in the README:

| Placeholder | What to put there |
|-------------|-------------------|
| `YOUR_BANNER_IMAGE_URL_HERE` | A wide banner (e.g., 1280×320) — try [Capsule Render](https://capsule-render.vercel.app/) to auto-generate |
| `YOUR_SCREENSHOT_1_URL_HERE` | A screenshot of the player mid-song |
| `YOUR_SCREENSHOT_2_URL_HERE` | Another angle / a different song |
| `YOUR_DEMO_GIF_URL_HERE` | A short GIF showing it in action |

### 💡 Easiest way to host images

1. **Create an `assets/` folder** in your repo
2. Drop your images/GIFs inside
3. Reference them like:
   ```markdown
   <img src="assets/banner.png" width="100%" />
   <img src="assets/screenshot1.png" width="80%" />
   <img src="assets/demo.gif" width="80%" />
   ```
4. Commit and push — GitHub serves them automatically.

### 🎨 Auto-generate a banner

Use this URL (no upload needed) — it renders live:

```markdown
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,24&height=200&section=header&text=Lyrics%20%26%20Me&fontSize=70&fontAlignY=35&desc=Watch%20your%20songs%20sing%20themselves&descAlignY=55&descSize=20" width="100%" />
```

Replace `YOUR_BANNER_IMAGE_URL_HERE` with that line and you'll have a gorgeous animated header **instantly**.

---

## ✅ Quick Push Checklist

```bash
# Save README.md, then:
git add README.md assets/
git commit -m "Add beautiful README with preview images"
git push
```

---

Want me to also create:
- 📄 a **`LICENSE`** file (MIT) ready to paste?
- 🚫 a **`.gitignore`** tuned for Python + audio?
- 🏷️ **GitHub Topics/Tags** (like `python`, `lyrics`, `terminal`, `pygame`, `music`, `ansi`)?

Just say the word and I'll generate them.
