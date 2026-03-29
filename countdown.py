#!/usr/bin/env python3
"""countdown - Countdown timer."""
import sys,argparse,json,time,re
def parse_time(s):
    total=0
    for m in re.finditer(r"(\d+)(h|m|s)",s):
        n=int(m.group(1));u=m.group(2)
        total+=n*{"h":3600,"m":60,"s":1}[u]
    if not total:total=int(s)
    return total
def main():
    p=argparse.ArgumentParser(description="Countdown timer")
    p.add_argument("duration",help="Duration (e.g. 5m30s, 300)")
    p.add_argument("--json",action="store_true")
    args=p.parse_args()
    secs=parse_time(args.duration)
    if args.json:print(json.dumps({"duration_seconds":secs,"formatted":f"{secs//3600}h{(secs%3600)//60}m{secs%60}s"}));return
    start=time.time()
    while True:
        elapsed=time.time()-start;remaining=max(0,secs-elapsed)
        m,s=divmod(int(remaining),60);h,m=divmod(m,60)
        print(f"\r{h:02d}:{m:02d}:{s:02d}",end="",flush=True)
        if remaining<=0:print("\nDone!");break
        time.sleep(0.1)
if __name__=="__main__":main()
