#!/usr/bin/env python3
"""Countdown timer with progress bar and sound."""
import sys, time, re
def parse_duration(s):
    m = re.match(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", s)
    if m: return int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
    return int(s)
def cli():
    if len(sys.argv) < 2: print("Usage: countdown <duration> [label]"); print("  e.g. 5m, 1h30m, 90s, 300"); sys.exit(1)
    total = parse_duration(sys.argv[1]); label = " ".join(sys.argv[2:]) or "Timer"
    start = time.time()
    try:
        while True:
            elapsed = time.time() - start; remaining = max(0, total - elapsed)
            pct = min(1, elapsed / total); bar = "█" * int(pct*30) + "░" * (30-int(pct*30))
            m, s = divmod(int(remaining), 60); h, m = divmod(m, 60)
            ts = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
            print(f"\r  {label} [{bar}] {ts} remaining  ", end="", flush=True)
            if remaining <= 0: print("\n  ⏰ Done!"); break
            time.sleep(0.5)
    except KeyboardInterrupt: print("\n  Cancelled")
if __name__ == "__main__": cli()
