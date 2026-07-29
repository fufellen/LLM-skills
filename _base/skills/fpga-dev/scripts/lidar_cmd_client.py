"""Raw lidar command client (port 50101): VIEW_SECTOR 0x53 and ECHO/format 0x54.

Frame (FixedLen): FF FE <ver=12> <A0> <cnt> <cmd> <rw> + data[16] + FF 9B
"""
import argparse, socket, time

def build(cmd, rw, data16, cnt=1, ver=12):
    return bytes([0xFF, 0xFE, ver, 0xA0, cnt, cmd, rw]) + bytes(data16) + bytes([0xFF, 0x9B])

class Ldr:
    def __init__(self, host, local, port=50101):
        self.s = socket.create_connection((host, port), timeout=5,
                                          source_address=(local, 0) if local else None)
        self.s.settimeout(2.0)
        self.cnt = 1

    def tx(self, cmd, rw, data16, label):
        self.cnt = (self.cnt + 1) & 0xFF
        self.s.sendall(build(cmd, rw, data16, self.cnt))
        try:
            r = self.s.recv(256)
        except socket.timeout:
            r = b""
        if len(r) >= 14 and r[5] == cmd:
            if cmd == 0x53:
                print(f"{label}: enable={r[7]} start={int.from_bytes(r[8:11],'little')} "
                      f"end={int.from_bytes(r[11:14],'little')}")
            elif cmd == 0x54:
                print(f"{label}: echo_count={r[7]} dbc={r[8]} echo_mode={r[9]}")
        else:
            print(f"{label}: rx={r.hex(' ') if r else '<none>'}")
        return r

    def sector(self, start=None, end=None):
        if start is not None:
            d = [0] * 16
            d[0] = 1
            d[1:4] = list(int(start).to_bytes(3, "little"))
            d[4:7] = list(int(end).to_bytes(3, "little"))
            self.tx(0x53, 1, d, f"sector<-{start}..{end}")
            time.sleep(0.3)
        return self.tx(0x53, 0, [0] * 16, "sector?")

    def fmt(self, echo_count=None, dbc=None, echo_mode=None):
        if dbc is not None:
            d = [0] * 16
            d[0] = echo_count
            d[1] = dbc
            d[2] = echo_mode
            self.tx(0x54, 1, d, f"fmt<-ec={echo_count} dbc={dbc} em={echo_mode}")
            time.sleep(0.3)
        return self.tx(0x54, 0, [0] * 16, "fmt?")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--local-host", default=None)
    ap.add_argument("--sector", nargs=2, type=int, metavar=("START", "END"))
    ap.add_argument("--dbc", type=int)
    ap.add_argument("--echo-count", type=int, default=1)
    ap.add_argument("--echo-mode", type=int, default=1)
    ap.add_argument("--read", action="store_true")
    a = ap.parse_args()
    l = Ldr(a.host, a.local_host)
    if a.sector:
        l.sector(a.sector[0], a.sector[1])
    if a.dbc:
        l.fmt(a.echo_count, a.dbc, a.echo_mode)
    if a.read or (not a.sector and not a.dbc):
        l.sector()
        l.fmt()
