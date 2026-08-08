# Cue — script reader

Type or paste a script, set a pace, and read along. The current word is
highlighted and the page scrolls itself so you never lose your place. Turn on
**Read aloud** and the browser speaks it instead — with the highlight following
the voice.

Single self-contained HTML file. No build, no dependencies, no network calls.

## Run it

Open `index.html` in a browser — double-click it, or:

```bash
python3 -m http.server 8080 --directory script-reader
# then open http://localhost:8080
```

## Using it

1. Type or paste your script into the left pane. Blank lines become longer pauses.
2. Set the pace. 110 wpm is deliberate, 150 is conversational, 190 is a news
   read, 260 is drilling. The footer shows how long the script will take at the
   pace you picked.
3. Press **Start reading**.

While it's running:

| Key | Action |
| --- | --- |
| `Space` | Play / pause |
| `←` `→` | Jump back / forward one sentence |
| `↑` `↓` | Nudge the pace by 10 wpm |
| `Esc` | Back to the script to edit it |

You can also click any word to jump there, and drag the pace slider mid-read —
the voice picks up from the word you're on.

Your script and settings are kept in `localStorage`, so they're still there when
you come back. Nothing is uploaded anywhere.

## How the pacing works

Words per minute alone reads unnaturally, so each word gets a duration built
from the pace you set, then adjusted:

- **Word length** — scaled against the average word length of *your* script, so
  the total still lands on the wpm you asked for.
- **Punctuation** — a comma, semicolon, colon or dash adds a short beat; a
  period, question mark or ellipsis adds a longer one.
- **Line breaks** — a new line adds a beat, a blank line adds a full pause.

With **Read aloud** on, the browser's speech engine is the clock instead: word
boundary events from the utterance drive the highlight, so it stays on the word
actually being spoken. The pace slider maps to the speech rate. Long scripts are
spoken in sentence-sized chunks, which works around the utterance length limit
that otherwise cuts speech off mid-script in Chrome.

## Browser notes

- Highlight-and-scroll reading works everywhere.
- Read aloud uses the Web Speech API and the voices installed on your device, so
  the voice list differs by browser and OS. If no voice is available or speech
  fails to start, the reader says so and keeps going silently rather than
  stalling.
- Playback pauses when you switch tabs, since browsers throttle background
  timers and the speech would drift out of sync with the highlight.

## Relationship to the rest of this repo

Standalone and self-contained — it shares no code with the PlateMate capstone
app in the repository root.
