# Coaching Agreement — Alex × Coach Dana (synthetic)

Package: Standard. Configuration consumed by the escalation path when a
stop fires (DESIGN.md §4, file 9). Key-value block is machine-read.

```
channel: in-app coach inbox
response_window_hours: 24
quiet_hours: 21:00-07:00
flag_scope: all
hard_stop_override: none
```

Plain-language summary (what the client agreed to at onboarding): urgent
flags are delivered immediately during waking hours and at window-open
(07:00) if they fire during quiet hours; normal flags go with the daily
digest; the coach sees counts and reason codes, and the triggering message
itself is shared once per this agreement. The client sees every flag the
coach sees, including its delivery time.
