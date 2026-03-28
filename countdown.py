#!/usr/bin/env python3
"""countdown - CLI countdown timer with large display."""
import sys, time, os
DIGITS={
"0":["███","█ █","█ █","█ █","███"],"1":["  █","  █","  █","  █","  █"],
"2":["███","  █","███","█  ","███"],"3":["███","  █","███","  █","███"],
"4":["█ █","█ █","███","  █","  █"],"5":["███","█  ","███","  █","███"],
"6":["███","█  ","███","█ █","███"],"7":["███","  █","  █","  █","  █"],
"8":["███","█ █","███","█ █","███"],"9":["███","█ █","███","  █","███"],
":":["   "," █ ","   "," █ ","   "]
}
def big_time(seconds):
    m,s=divmod(seconds,60); h,m=divmod(m,60)
    text=f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
    for row in range(5):
        print("  ".join(DIGITS.get(c,DIGITS["0"])[row] for c in text))
def countdown(seconds):
    while seconds>=0:
        os.system("clear" if os.name!="nt" else "cls")
        big_time(seconds)
        if seconds==0: print("\n⏰ TIME'S UP!"); break
        time.sleep(1); seconds-=1
def parse_time(s):
    parts=s.split(":")
    if len(parts)==3: return int(parts[0])*3600+int(parts[1])*60+int(parts[2])
    if len(parts)==2: return int(parts[0])*60+int(parts[1])
    v=s.lower()
    if v.endswith("h"): return int(v[:-1])*3600
    if v.endswith("m"): return int(v[:-1])*60
    if v.endswith("s"): return int(v[:-1])
    return int(v)
if __name__=="__main__":
    if len(sys.argv)<2: print("Usage: countdown <time> (e.g., 5m, 1:30, 90s)"); sys.exit(1)
    countdown(parse_time(sys.argv[1]))
