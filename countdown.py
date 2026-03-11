#!/usr/bin/env python3
"""countdown - Countdown timer with display. Zero deps."""
import sys, time, re

def parse_duration(s):
    m = re.match(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$', s)
    if not m or not any(m.groups()): 
        try: return int(s)
        except: print(f"Bad duration: {s}"); sys.exit(1)
    h, mi, sec = (int(x) if x else 0 for x in m.groups())
    return h*3600 + mi*60 + sec

def fmt_time(secs):
    h, r = divmod(int(secs), 3600)
    m, s = divmod(r, 60)
    if h: return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def main():
    if len(sys.argv) < 2:
        print("Usage: countdown.py <duration> [message]"); print("  countdown.py 5m 'Tea time!'"); sys.exit(1)
    total = parse_duration(sys.argv[1])
    msg = sys.argv[2] if len(sys.argv) > 2 else "Time's up!"
    end = time.time() + total
    try:
        while True:
            left = end - time.time()
            if left <= 0: break
            sys.stdout.write(f"\r  ⏳ {fmt_time(left)}  ")
            sys.stdout.flush()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCancelled")
        return
    print(f"\r  🔔 {msg}{'':20s}")

if __name__ == "__main__":
    main()
