#!/usr/bin/env python3
"""countdown - Date countdown and deadline tracker.

Single-file, zero-dependency CLI.
"""

import sys
import argparse
import json
import os
from datetime import datetime, date, timedelta

DATA_FILE = os.path.expanduser("~/.countdown.json")


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def parse_date(s):
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%dT%H:%M"]:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Can't parse date: {s}")


def cmd_until(args):
    target = parse_date(args.date)
    now = datetime.now()
    delta = target - now
    days = delta.days
    hours = delta.seconds // 3600
    if days < 0:
        print(f"  {abs(days)}d {hours}h ago")
    elif days == 0:
        print(f"  Today! ({hours}h remaining)")
    else:
        weeks = days // 7
        print(f"  {days}d {hours}h remaining")
        if weeks:
            print(f"  ({weeks} weeks, {days % 7} days)")


def cmd_add(args):
    data = load()
    data[args.name] = {"date": args.date, "note": args.note or ""}
    save(data)
    print(f"  Added: {args.name} → {args.date}")


def cmd_list(args):
    data = load()
    if not data:
        print("  No countdowns. Use 'add' to create one.")
        return
    now = datetime.now()
    items = []
    for name, info in data.items():
        try:
            target = parse_date(info["date"])
            days = (target - now).days
            items.append((days, name, info))
        except ValueError:
            items.append((99999, name, info))
    items.sort()
    for days, name, info in items:
        if days < 0:
            emoji = "✅" if days < -1 else "🔴"
            label = f"{abs(days)}d ago"
        elif days == 0:
            emoji = "🔥"
            label = "TODAY"
        elif days <= 7:
            emoji = "⏰"
            label = f"{days}d"
        else:
            emoji = "📅"
            label = f"{days}d"
        note = f" — {info['note']}" if info.get("note") else ""
        print(f"  {emoji} {label:>8s}  {name}{note}")


def cmd_remove(args):
    data = load()
    if args.name in data:
        del data[args.name]
        save(data)
        print(f"  Removed: {args.name}")
    else:
        print(f"  Not found: {args.name}")
        return 1


def cmd_between(args):
    d1 = parse_date(args.date1)
    d2 = parse_date(args.date2)
    delta = abs((d2 - d1).days)
    weeks = delta // 7
    print(f"  {delta} days ({weeks} weeks, {delta % 7} days)")
    print(f"  {delta * 24} hours")
    print(f"  {delta / 30.44:.1f} months")
    print(f"  {delta / 365.25:.2f} years")


def main():
    p = argparse.ArgumentParser(prog="countdown", description="Date countdown tracker")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("until", aliases=["u"], help="Time until date")
    s.add_argument("date")
    s = sub.add_parser("add", help="Add countdown")
    s.add_argument("name"); s.add_argument("date"); s.add_argument("-n", "--note")
    s = sub.add_parser("list", aliases=["ls"], help="List countdowns")
    s = sub.add_parser("remove", aliases=["rm"], help="Remove countdown")
    s.add_argument("name")
    s = sub.add_parser("between", help="Days between dates")
    s.add_argument("date1"); s.add_argument("date2")
    args = p.parse_args()
    if not args.cmd: p.print_help(); return 1
    cmds = {"until": cmd_until, "u": cmd_until, "add": cmd_add, "list": cmd_list,
            "ls": cmd_list, "remove": cmd_remove, "rm": cmd_remove, "between": cmd_between}
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
