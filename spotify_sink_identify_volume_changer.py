#!/usr/bin/env python3
#
# Author: Marcin Kocur, attribution license: https://creativecommons.org/licenses/by/4.0/
#
# Modifications: Jaxx Armstrong (2021-01-17)
#

import subprocess
import os
import sys

x=0
y=0
env = os.environ
env['LANG'] = 'en_US'
app = '"Spotify"'

if len(sys.argv) > 1 and sys.argv[1] in ['up', 'UP', 'down', 'DOWN']:
    volchange = sys.argv[1]
else:
    print("Use 'up' or 'down' as argument. Exiting.")
    sys.exit(2)

pactl = subprocess.check_output(['pactl', 'list', 'sink-inputs'], env=env).decode().strip().split()

if app in pactl:
    for e in pactl:
        x += 1
        if e == app:
            break
    for i in pactl[0 : x -1 ]:
        y += 1
        if i == 'Sink' and pactl[y] == 'Input' and '#' in pactl[y + 1]:
            sink_id = pactl[y+1]
        if i == 'Volume:' and '%' in pactl[y + 3]:
            volume = pactl[y + 3]
    sink_id = sink_id[1: ]
    volume = volume[ : -1 ]

    if volchange == "up" or volchange == "UP":
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '+1%'])
    else:
        subprocess.run(['pactl', 'set-sink-input-volume', sink_id, '-1%'])
