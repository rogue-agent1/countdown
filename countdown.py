#!/usr/bin/env python3
"""Terminal countdown timer with progress bar."""
import sys, time, re

def parse_duration(s):
    m = re.match(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not m or not any(m.groups()): return int(s)
    h, mn, sc = (int(x) if x else 0 for x in m.groups())
    return h*3600 + mn*60 + sc

def countdown(total):
    start = time.time()
    try:
        while True:
            elapsed = time.time() - start
            remaining = max(0, total - elapsed)
            if remaining <= 0: break
            pct = elapsed / total
            bar_w = 30
            filled = int(bar_w * pct)
            bar = '█' * filled + '░' * (bar_w - filled)
            m, s = divmod(int(remaining), 60)
            h, m = divmod(m, 60)
            t = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            sys.stdout.write(f"\r  {bar} {t} remaining ")
            sys.stdout.flush()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    print(f"\r  {'█'*30} Done!{'':20}")
    print("\a", end='')  # bell

if __name__ == '__main__':
    if len(sys.argv) < 2: print("Usage: countdown.py <duration> (e.g. 5m, 1h30m, 90s, 60)"); sys.exit(1)
    countdown(parse_duration(sys.argv[1]))
