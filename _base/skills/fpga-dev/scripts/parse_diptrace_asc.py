# -*- coding: utf-8 -*-
"""Извлечение pin map из DipTrace ASCII (.asc): pin -> net для заданных RefDes."""
import re
import sys

ASC = sys.argv[1]
WANT = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'D7'}

re_part = re.compile(r'^\s{4}\(Part "([^"]*)" "([^"]*)"')
re_pin = re.compile(r'^\s+\(Pin \d+ ')
re_num = re.compile(r'^\s+\(Number (-?\d+)\)')
re_netnum = re.compile(r'^\s+\(NetNumber (-?\d+)\)')
re_name = re.compile(r'^\s+\(Name "([^"]*)"\)')
re_strnum = re.compile(r'^\s+\(StringNumber "([^"]*)"\)')
re_noconn = re.compile(r'^\s+\(NoConnect "([YN])"\)')
re_net = re.compile(r'^\s{4}\(Net "([^"]*)"')

nets = {}          # net number -> name
pins = {}          # refdes -> list of dicts
parts_seen = {}    # refdes -> part name

cur_part = None    # (name, refdes)
in_pin = False
pin = None
cur_net = None     # net name awaiting its Number

with open(ASC, encoding='cp1251', errors='replace') as f:
    for line in f:
        m = re_part.match(line)
        if m:
            cur_part = (m.group(1), m.group(2))
            parts_seen.setdefault(m.group(2), m.group(1))
            cur_net = None
            continue
        m = re_net.match(line)
        if m:
            cur_net = m.group(1)
            cur_part = None
            continue
        if cur_net is not None:
            m = re_num.match(line)
            if m:
                nets[int(m.group(1))] = cur_net
                cur_net = None
            continue
        if cur_part and cur_part[1] in WANT:
            if re_pin.match(line):
                in_pin = True
                pin = {'net': None, 'name': '', 'ball': '', 'nc': 'N'}
                continue
            if in_pin:
                m = re_netnum.match(line)
                if m:
                    pin['net'] = int(m.group(1))
                    continue
                m = re_name.match(line)
                if m:
                    pin['name'] = m.group(1)
                    continue
                m = re_strnum.match(line)
                if m:
                    pin['ball'] = m.group(1)
                    continue
                m = re_noconn.match(line)
                if m:
                    pin['nc'] = m.group(1)
                    continue
                if re.match(r'^\s+\(PinNumRotate ', line):
                    pins.setdefault(cur_part[1], []).append(pin)
                    in_pin = False

for refdes in sorted(WANT):
    plist = pins.get(refdes, [])
    print(f'=== {refdes} ({parts_seen.get(refdes, "?")}): {len(plist)} pins ===')
    for p in sorted(plist, key=lambda x: x['ball']):
        net = nets.get(p['net'], f"<net#{p['net']}>") if p['net'] is not None else '<none>'
        if p['net'] in (-1, None):
            net = '(nc)'
        print(f"{p['ball']:6} {net:40} {p['name']}")
