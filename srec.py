#!/usr/bin/env python3
"""
SREC Launcher — one app, three independent blades
"""

import argparse
from modes import solar_system, catastrophe_clock, full_lifecycle

parser = argparse.ArgumentParser(description="SREC Cosmic Clockwork")
parser.add_argument('--mode', choices=['solar', 'catastrophe', 'full'], default='solar',
                    help='Which blade to run (default: solar)')
args = parser.parse_args()

print(f"\nRunning SREC in mode: {args.mode.upper()}\n")

if args.mode == 'solar':
    solar_system.run()
elif args.mode == 'catastrophe':
    catastrophe_clock.run()
else:
    full_lifecycle.run()      # not written yet — will be the combination
