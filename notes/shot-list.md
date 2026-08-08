# Shot list — two-pass recording

Pairs with the FINAL SCRIPT in [`video-beats.md`](video-beats.md). Script cues
below are the first words of each paragraph, so you can follow both at once.

Screen names are the app's own: tabs are **Console**, **Evals**, **Memory**,
**Settings**. Stages inside a run are **1 INPUT**, **2 CONTEXT**, **3 DECISION**,
**4 OUTPUT**, **5 REVIEW**. The Evals table columns, left to right, are **Case**,
**Expected behavior (PRD)**, **Actual**, **Verdict (human)**.

## The method

**Pass 1 is you.** Camera on your face, script beside the lens, no app, no
clicking. One clean read, paced to hit four minutes.

**Pass 2 is the screen.** Play the pass-1 audio back in headphones and click
along with it while capturing the screen. The layers then line up on the
timeline with almost no work, and every cue lands on the field you are naming.

**Pass 3 is the edit.** Screen capture over the voice, cutting to your face for
beats 1, 2 and 5.

Recording them separately is not a shortcut and nothing about it is dishonest.
The model call in pass 2 is a real call, captured, and that is the same evidence
it would be live.

## What the timing looks like now

719 words. With no clicks to talk over, the whole four minutes is speech.

| Pace | Runtime |
|---|---|
| 170 wpm (your casual read) | 4:14 |
| 175 wpm | 4:07 |
| **180 wpm** | **4:00** |
| 185 wpm | 3:53 |

Aim for 180 and leave two seconds of silence at the very end. If a take comes
in at 4:05 that is a fine take; the penalty is for four-minute-plus
presentations, and nobody stopwatches to the second.

---

# Pass 1 — the voice and face take

- **Script beside the lens, not below it.** Eyeline dropping to a desk reads as
  reading; eyeline just off the lens reads as thinking.
- **Do the whole thing in one take** even if you fluff a line. Pause, breathe,
  say the sentence again, and keep going. Fixing one sentence in the edit is
  easy; matching energy across two takes is not.
- **Three places to slow down, everywhere else keep moving:**
  - "So what do most people do? Buy nothing." Beat 1's landing.
  - "The model broke my rule. The architecture held." Beat 4's landing.
  - "...and so are you." Then stop, and hold two seconds of silence.
- **Do not read the beat headings.** They are not in the script text.

---

# Pass 2 — the screen capture

## Before you hit record

1. **Incognito window.** No bookmarks bar, no other tabs, no extensions.
2. **Key saved** in Settings, then confirm the status chip reads
   `live · claude-sonnet-4-5-...`. If it says `key saved · runs use ...` the key
   is unproven, so do one throwaway run and reload.
3. **Console tab open, D-1001 selected, not yet run.**
4. **Window sized so the status chip is in frame.** It is the proof the model is
   available, and beat 3's closing line depends on it being visible.
5. **Zoom to about 125%** so reason codes and citation chips are legible at
   1080p.
6. **Notifications off.**
7. **Headphones in, pass-1 audio queued.**

## The capture, in order

| Script cue in your ear | On screen | What you do |
|---|---|---|
| "So I built PlateMate for the days a plan wasn't written for." | Console, D-1001 selected, unrun | Screen starts here. Nothing before this needs capture. |
| "Let's run that afternoon again..." | stage **1 INPUT**, the client's message | **Click Run on the last word of the sentence.** |
| "The day is already at 1350 calories..." | stage **4 OUTPUT**, the Budget line | The run lands during this sentence |
| "The AI's job is reading and writing..." | stage **3 DECISION** | Hover the **Why** field, then the **Citations** chips, then the **Language screen** line. One per clause. |
| "Three options ranked..." | stage **4 OUTPUT**, options | Hover the **bottom row**, the never-skip fallback |
| "Pick one and a portion..." | options + stage **5 REVIEW** | Click an option and a portion so the numbers move. **Do not click Approve.** |
| "Now a different case..." | Click **D-1005** in the case list | Click on the word *case* |
| "It stops, and names three reasons..." | stage **3 DECISION** codes, then stage **4** | Reason codes first, then the stop message, GET HELP NOW, the Coach flag and its delivery time |
| "And this label..." | stage 3's metaline *safety screening — stopped before any model call* | Hover the label, then the **status chip** top right |
| "That's two of six cases..." | switch to **Evals** | Switch on the word *six*. Let the four headers sit still for a beat. |
| "I ran all six against the live model..." | the **model-on check** line above the table | It reads *the same six cases re-run with live model ... 5 matched; E-3 diverged* |
| "This one..." | scroll to the **E-3** row | The **Actual** column carries the warn-coloured *DIFFERS* line |
| "It names the rule..." | E-3's **Verdict (human)** cell, model-on block at the bottom | The note quotes the model's own reasoning |
| "The model broke my rule..." | hold on the row | Mouse still |
| "The goal is a plan you can stay on..." | the live site with the **URL visible** | Hold the URL through the whole close, then two seconds after |

## Moments that need a tight crop in the edit

The script uses pointing words, and with no live cursor the crop has to do the
pointing. Zoom or highlight these five, or the words float:

1. "**Here is why**, in its own words" → the Why field
2. "and it passed the **banned word check**" → the Language screen line
3. "**The bottom row** is a fallback" → the fallback row
4. "And **this label**" → *stopped before any model call*
5. "**This one.**" → the E-3 row

## Things that will cost you if you forget

- **Do not click Approve.** Nothing in the script claims anything was saved, and
  the demo is stronger with the gate unclicked.
- **Do not re-run the evals.** The model-on check is shipped in the file and
  displays without a key. Re-running risks a different result on camera.
- **Do not open Memory or Settings.** Neither is in the script.
- **Check the status chip between takes.** If a call 401s it flips to
  `key rejected (401) — running offline rules`, and beat 3's closing line
  becomes false.
- **Capture more than you need.** Let each screen sit for a few extra seconds
  either side. Trimming in the edit is free; a re-shoot is not.
