# Shot list — what is on screen, line by line

Pairs with the FINAL SCRIPT in [`video-beats.md`](video-beats.md). Script cues
below are the first few words of each paragraph, so you can follow both at once.

Screen names are the app's own: tabs are **Console**, **Evals**, **Memory**,
**Settings**. Stages inside a run are **1 INPUT**, **2 CONTEXT**, **3 DECISION**,
**4 OUTPUT**, **5 REVIEW**. The Evals table columns, left to right, are **Case**,
**Expected behavior (PRD)**, **Actual**, **Verdict (human)**.

---

## Before you hit record

1. **Incognito window.** No bookmarks bar, no other tabs, no extensions.
2. **Key saved** in Settings, then confirm the status chip at the top reads
   `live · claude-sonnet-4-5-...`. If it says `key saved · runs use ...` the key
   has not been proven yet, so do one throwaway run first and then reload.
3. **Console tab open, D-1001 selected, not yet run.**
4. **Window sized so the status chip is in frame.** It is the proof the model is
   available, and beat 3's last line depends on it being visible.
5. **Zoom to about 125%** so the reason codes and citation chips are legible at
   1080p. Check by squinting at the Actual column in the Evals tab.
6. **Notifications off.** Do Not Disturb on the machine.
7. **Open the Evals tab once and scroll to E-3**, then come back to Console. You
   want to know how far that scroll is before you are live.

---

## Beats 1 and 2 — you, not the screen

Roughly 0:00 to 1:50. Nothing in the app is worth looking at yet, and cutting to
a product screen while describing a person in a store undercuts the story.

Camera on you, or a single static frame. Do not put the app up behind you.

The one screen move is at the end of beat 2:

| Script cue | Screen | Action |
|---|---|---|
| "So I built PlateMate for the days a plan wasn't written for." | Cut to the app, Console tab, D-1001 selected, unrun | Cut on the word *PlateMate*, not after the sentence |

---

## Beat 3 — the demo

| Script cue | On screen | What you do |
|---|---|---|
| "Let's run that afternoon again..." | Console, D-1001, stage **1 INPUT** with the client's message visible | Read the message off the screen. **Click Run on the last word.** |
| "The day is already at 1350 calories..." | stage **4 OUTPUT**, the Budget line | The run lands during this sentence. If it is still thinking, slow down; do not stop talking. |
| "The AI's job is reading and writing..." | stage **3 DECISION** | Three things in order: the **Why** field, the **Citations** chips, then the **Language screen** line. One per clause. |
| "Three options ranked..." | stage **4 OUTPUT**, the options list | Point at the **bottom row**, the never-skip fallback. That is the payoff of beat 1. |
| "Pick one and a portion..." | options + stage **5 REVIEW** | Actually click an option and a portion so the numbers move. Do **not** click Approve. |
| "Now a different case..." | Click **D-1005** in the case list | Click on "Now a different case", then read the message off stage **1 INPUT** |
| "It stops, and names three reasons..." | stage **3 DECISION** reason codes, then stage **4 OUTPUT** | Reason codes first, then the stop message, GET HELP NOW, and the Coach flag with its delivery time |
| "And this label..." | stage 3's metaline: *safety screening — stopped before any model call* | Point at the label, then glance at the **status chip** top right. The chip is the whole argument. |

**The only dead-air risk is the D-1001 run.** D-1005 stops before any model call,
so it renders instantly. Start the run early and keep talking through it.

---

## Beat 4 — the evidence

| Script cue | On screen | What you do |
|---|---|---|
| "That's two of six cases..." | **Evals** tab | Switch tabs on the word *six*. Let the four column headers be readable for a beat. |
| "I wrote what should happen before running it..." | the **Expected behavior (PRD)** column | Left to right across the header as you say the three parts |
| "I ran all six against the live model..." | the **model-on check** line above the table | It reads *the same six cases re-run with live model ... 5 matched; E-3 diverged*. That sentence is the claim you just made. |
| "This one..." | scroll to the **E-3** row | The **Actual** column carries a warn-coloured line: *model-on check · 2026-08-06 · DIFFERS* |
| "It names the rule, says the counter it depends on is at zero..." | E-3's **Verdict (human)** cell, the model-on block at the bottom | The note quotes the model's own reasoning. Hold long enough to read a line of it. |
| "Nothing reached the client..." | same cell | Stay put |
| "The model broke my rule. The architecture held." | hold on the row | Do not move the mouse. Say it and stop. |

---

## Beats 5 and 6 — you again, then the link

| Script cue | Screen | Action |
|---|---|---|
| "The pilot is three clients, four weeks..." | Camera, or hold the Evals tab | Camera is better. It is a commitment, not a feature. |
| "The goal is a plan you can stay on..." | The live site with the **URL visible** | Cut here, not at the end. The link should be on screen for the whole close. |
| after "...and so are you." | hold the URL | **Two full seconds of silence, then stop recording.** Do not narrate the link. |

---

## Things that will cost you if you forget

- **Do not click Approve.** Nothing in the script claims anything was saved, and
  the demo is stronger with the gate unclicked.
- **Do not re-run the evals live.** The model-on check is shipped in the file and
  displays without a key. Re-running risks a different result on camera.
- **Do not open Memory or Settings.** Neither is in the script.
- **Check the status chip once before each take.** If a call 401s mid-recording
  it flips to `key rejected (401) — running offline rules`, and beat 3's closing
  line becomes false.
- **Watch the mouse.** During the two lines that land, "the answer is never
  nothing" and "the architecture held", the cursor should be still.
