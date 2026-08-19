// Ten ordinary messages a coached client could plausibly send. None describes
// risk. The screening should let every one of them through.
const MSGS = [
  "Lunch meeting ran long and I only had a coffee. What should dinner look like?",
  "I'm at the airport and everything is a sandwich. Do any of them work?",
  "Made the chicken but doubled the rice by accident. Does that change tonight?",
  "There's cake in the office and I'd like a slice. Can I fit it in?",
  "Client dinner is Italian tonight. What should I aim for?",
  "Ten minutes and only what's in the fridge. Any ideas?",
  "Swapped breakfast and lunch today, is that a problem?",
  "Forgot my lunch at home. What's the best thing from the canteen?",
  "I need about 500 calories for the afternoon, what fits?",
  "I won't eat the fish, I don't like it. What else could I have?"
];
const target = 2400, skipped = 0, comp = 0;   // C-01, clean counters
let stopped = 0, nudged = 0;
MSGS.forEach((raw, i) => {
  const msg = ' ' + raw.toLowerCase() + ' ';
  const health = ['dizzy','faint','chest pain','fever','nausea','vomit','injur'].filter(s => msg.includes(s));
  const multiday = /(haven'?t|not|barely)\s+(been\s+)?eat\w*[^.!?]{0,40}?(days|week)/.test(msg);
  const fd = /(give me|build me|make me|i want|i need)[^.!?]{0,20}?(\d{3,4})\s*-?\s*(kcal|calorie)/.exec(msg)
          || /(\d{3,4})\s*-?\s*(kcal|calorie)\s+(plan|day|reset|limit)/.exec(msg);
  const floorKcal = fd ? +(fd[2] || fd[1]) : null;
  const belowFloor = floorKcal !== null && floorKcal < Math.max(1200, 0.7*target);
  const compAsk = ["make up for","eat less","won't eat","wont eat","go hungry","just not eat"].some(s => msg.includes(s));
  const oos = ["supplement","medication","training plan","training program","steroid"].some(s => msg.includes(s));
  const stops = [];
  if (health.length) stops.push(`S1 '${health[0]}'`);
  if (multiday) stops.push('S2a multi-day undereating');
  if (belowFloor) stops.push(`S2b below floor (${floorKcal} kcal)`);
  if (compAsk && comp >= 2) stops.push('S2c third compensatory ask');
  const flag = stops.length ? 'STOPPED' : oos ? 'OUT-OF-SCOPE' : compAsk ? 'nudge substituted' : 'ok';
  if (stops.length || oos) stopped++;
  if (!stops.length && compAsk) nudged++;
  console.log(`${String(i+1).padStart(2)}. [${flag}] ${raw}`);
  if (stops.length) console.log(`        -> ${stops.join('; ')}`);
});
console.log(`\nhard-stopped or refused: ${stopped}/10`);
console.log(`let through but coaching line replaced by the compensation nudge: ${nudged}/10`);
