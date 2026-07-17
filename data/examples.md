# Examples — what good looks like (synthetic)

Few-shot context for the two LLM language jobs (`parse_situation`,
`coaching_line`). Teaches tone and card format by demonstration. Three
model outputs, per DESIGN.md §4 file 10.

## Example 1 — happy-path options card

BUDGET
Daily target: 2400 kcal / 160 g protein
Already consumed: 1350 kcal / 90 g
Reserved (team dinner): 1000 kcal / 40 g
Remaining for this meal: 50 kcal / 30 g

OPTIONS
1. Skyr, plain, big cup — 170 kcal, 28 g protein, 1 min, home — day-end 2520 kcal (+120 ✓), 158 g (−2 ✓)
2. Protein shake, water — 160 kcal, 30 g protein, 1 min, home — day-end 2510 kcal (+110 ✓), 160 g (0 ✓)

BRIDGE
Protein bar from your bag — 210 kcal, 20 g protein — if nothing above works, take this instead of skipping.

COACHING LINE
Nice catch flagging the dinner early — grab the skyr and tonight is already handled.

## Example 2 — imperfect-day card

BUDGET
Daily target: 2400 kcal / 160 g protein
Already consumed: 1850 kcal / 95 g
Reserved (client dinner): 900 kcal / 40 g
Remaining for this meal: −350 kcal / 25 g

OPTIONS (closest possible — no option lands in the band today)
1. Cottage cheese bowl — 180 kcal, 22 g protein — day-end +530 kcal, protein −3 ✓
2. Miso soup with tofu — 120 kcal, 12 g protein — day-end +470 kcal, protein −13

STRATEGY
Today won't balance perfectly, and that is fine: calories average over a
3-7 day window — trim roughly 150 kcal/day over the next few days. Protein
stays the daily anchor: pick the highest-protein option and don't skip.

COACHING LINE
The day still counts — land the protein tonight and let the week absorb the rest.

## Example 3 — stop message

I'm stepping in instead of answering, because what you wrote tells me food
math is not what you need right now.

Safe default: eat your planned meal as written. No adjustments today.

One rough day changes almost nothing across a week — calories average out
over 3-7 days, and your plan already accounts for that.

Your coach has been sent an urgent flag about this (delivery 07:00 at
window-open). You see exactly what they see: the reason codes and this
conversation's trigger, once, per your agreement.
