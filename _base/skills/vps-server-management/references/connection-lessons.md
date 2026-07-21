# Connection Lessons (Windows + VPN)

Durable, reusable troubleshooting for connecting to VPS servers from this user's Windows + AmneziaWG VPN setup. No secrets, IPs, or passwords here — environment behavior only.

## Which path reaches the server? Diagnose BEFORE assuming

The user's traffic to a server can go two ways: through the VPN exit, or directly via the local ISP (when the IP is in the VPN's split-tunnel exclusion list). **Neither path is universally right — test both.**

- Через VPN: TCP may connect but SSH may be throttled (see port-22 lesson below).
- Напрямую: some servers are **not routable at all from the local ISP** — `tracert` shows `Request timed out` on every hop and TCP never establishes. For such servers the VPN is the ONLY working path; excluding the IP from the VPN makes things worse, not better.

Diagnostic pair, run per path:

```powershell
Test-NetConnection <ip> -Port 22   # TcpTestSucceeded?
tracert -d -h 5 -w 800 <ip>        # where do packets die?
```

`PingSucceeded: False` alone is normal (many VPS drop ICMP). TCP True + SSH banner timeout = mid-path filtering, NOT a dead server.

## Amnezia split tunneling: the list does nothing until the master toggle is ON

The split-tunnel address list is applied only when the **Split tunneling master switch** (top-right toggle) is enabled, and routes apply only after **reconnecting** the VPN. A filled list under a grey/off toggle silently changes nothing — symptoms then look "intermittent". When split-tunnel behavior seems inconsistent, screenshot-check the toggle state first.

## Port 22 is throttled on shared VPN exits — move SSH to a non-standard port

Symptom: TCP to :22 connects, but SSH dies with `Connection timed out during banner exchange`, while the provider's VNC console shows a healthy, idle server and `journalctl -u ssh` shows **no trace of our attempts** (packets filtered before sshd). Root cause: anti-brute-force filtering of port 22 traffic from shared/VPN IPs (server logs show constant bot password-guessing from the internet — that is what the filters exist for).

Fix: move sshd to a non-standard port (e.g. 2222). Bonus: the bot brute-force noise stops entirely. On **Ubuntu 24.04 the port lives behind socket activation** — editing `sshd_config` alone does nothing while `ssh.socket` holds :22 (`ss -tlnp` shows `("systemd",pid=1,...)` next to sshd). Required sequence:

1. In `/etc/ssh/sshd_config`: `#Port 22` → `Port 2222`.
2. `systemctl disable --now ssh.socket`
3. `systemctl restart ssh`
4. Verify with `ss -tln` → `0.0.0.0:2222`.

Client side afterwards: `ssh -p 2222 root@<ip>`.

## Do not hammer a throttled port

Retry loops against a filtered/throttled SSH port make the filtering worse and pollute the picture. After 2 failures, stop and change the diagnosis (path test, VNC console, different port) instead of retrying harder. One careful attempt per hypothesis.

## Provider VNC (noVNC) console quirks

- **Symbol mangling**: `|` comes out as `\`, `>` gets silently swallowed — both when typed and via the Paste clipboard button. Any command containing pipes or redirects will be corrupted. Compose console commands with NO `|`, `>`, `>>`.
- Workarounds: edit files with `nano` instead of `echo ... > file`; use **Tab completion** to avoid typing underscores in filenames (`nano /etc/ssh/sshd` + Tab → `sshd_config`); `sed -i` also works when quoting is simple.
- Password typing is blind and error-prone; the Paste clipboard button is more reliable for passwords than for commands.
- The console keeps working when SSH is dead — it is the recovery path; don't close it until SSH is confirmed working.
- Keep console commands single and short; verify results with `ss -tln`, `systemctl status`, `journalctl -u ssh --no-pager -n 20` (no pipes needed).

## plink fails, native ssh works

`plink.exe` (PuTTY) dies with `FATAL ERROR: Network error: Software caused connection abort` on every attempt in this environment, even on paths where native `C:\Windows\System32\OpenSSH\ssh.exe` completes the handshake. **Use native OpenSSH; do not use plink.** Consequence: no `-pw` scripted password login — the one-time public-key install must be run interactively by the user (native ssh reads the password from the console, not stdin).

## Non-interactive key auth for automation

After the public key is in `~/.ssh/authorized_keys`, background shells work:

```powershell
ssh -p <port> -o BatchMode=yes root@<ip> "<command>"
```

`BatchMode=yes` fails fast instead of hanging on a password prompt — good for verifying key install.

## Russian VPS + Ubuntu mirrors

- `security.ubuntu.com` / `archive.ubuntu.com` are often unreachable or crawling from Russian VPS: `apt-get update` warns `Connection failed`, `apt upgrade` hangs for many minutes, and boot-time `apt-daily`/unattended-upgrades can wedge a 1 GB box (SSH unresponsive while console works).
- Fix first thing on a new box: switch APT to a Russian mirror in `/etc/apt/sources.list.d/ubuntu.sources` (e.g. `http://mirror.yandex.ru/ubuntu`), and disable/mask `apt-daily.timer` + `apt-daily-upgrade.timer` until the mirror is set.
- `journalctl` line `User sessions running outdated binaries: ... sshd` after an upgrade → restart `ssh` service at a convenient moment.

## Server identity check

`ssh -v ... 2>&1` prints `remote software version OpenSSH_<x> Ubuntu-<y>` — quick confirmation of the actual Ubuntu release before running version-dependent setup.
