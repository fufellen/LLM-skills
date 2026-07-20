# Connection Lessons (Windows + VPN)

Durable, reusable troubleshooting for connecting to VPS servers from this user's Windows + AmneziaWG VPN setup. No secrets, IPs, or passwords here — environment behavior only.

## plink fails, native ssh works

Symptom: `plink.exe -pw <pw> ...` dies immediately with `FATAL ERROR: Network error: Software caused connection abort`, on every attempt, even right after the VPN split tunnel is configured.

Meanwhile `C:\Windows\System32\OpenSSH\ssh.exe` to the same host completes the handshake normally (verbose log reaches `Authenticating to <ip>:22 as 'root'` and identifies the server, e.g. `OpenSSH_9.6p1 Ubuntu-3ubuntu13` = Ubuntu 24.04).

Conclusion: **use native OpenSSH; do not use plink** in this environment. Consequence: no `-pw` scripted password login is available, so the one-time public-key install must be run interactively by the user (native `ssh` reads the password from the console, not stdin).

## VPN split tunnel for Russian IPs

Symptom: `plink`/`ssh` abort, or TCP never establishes, when the VPN is on and the target is a Russian VPS.

Fix: the user adds the server IP to the VPN client's split tunnel ("Addresses from the list should not be accessed via VPN"). After that, native `ssh` connects.

Diagnostic before blaming SSH: `Test-NetConnection <ip> -Port 22`. `TcpTestSucceeded: True` = route is clean (the problem is elsewhere, e.g. plink). `PingSucceeded: False` is normal and not a problem — many VPS drop ICMP echo while allowing TCP/22.

## Non-interactive key auth for automation

After the public key is in the server's `~/.ssh/authorized_keys`, background/non-interactive shells work:

```powershell
ssh -o BatchMode=yes root@<ip> "<command>"
```

`BatchMode=yes` makes ssh fail fast instead of hanging on a password prompt if key auth is not yet set up — useful to verify the key install succeeded.

## Server identity check

`ssh -v ... 2>&1` prints `Remote protocol version 2.0, remote software version OpenSSH_<x> Ubuntu-<y>` — a quick way to confirm which Ubuntu the provider actually gave you before running setup steps that assume a version.
