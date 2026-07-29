"""Целочисленный угловой сдвиг тела кадра MSOP между двумя захватами.

    python msop_body_shift_scan.py <эталонный_raw_dir> <проверяемый_raw_dir>

Перебирает сдвиг s в узлах сетки и ищет минимум медианы |d_test(L) - d_ref(L+s*res)|
по узлам, где в обоих захватах есть валидные точки. Шумовой пол определяется
повтором одного и того же сектора (в норме 1-3 мм).

Так измерялся дефект «сдвиг тела кадра = Δ mod point_count» (потерянный при полной
очереди дескриптор, см. local-gowin-lidar.md): до фикса свип секторов давал
ненулевые s, после — 0 везде.
"""
import os, sys, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from msop_angle_profile import load_dir, profile

ref_dir, test_dir = sys.argv[1], sys.argv[2]
pa_r, pi_r, hd_r = load_dir(ref_dir)
pa_t, pi_t, hd_t = load_dir(test_dir)
pr = profile(pa_r, pi_r)
pt = profile(pa_t, pi_t)
RES = hd_r[0]["angle_res"]
QUORUM = 12

ref = {a: v[0] for a, v in pr.items() if v[0] is not None and v[2] >= QUORUM}
tst = {a: v[0] for a, v in pt.items() if v[0] is not None and v[2] >= QUORUM}

rows = []
for s in range(-250, 251):
    diffs = []
    for a, d in tst.items():
        r = ref.get(a + s * RES)
        if r is not None:
            diffs.append(abs(d - r))
    if len(diffs) >= 80:
        rows.append((statistics.median(diffs), len(diffs), s))

rows.sort()
print(f"res={RES} mdeg; ref pts={len(ref)} test pts={len(tst)}")
print("best shifts (median |dd| mm, n, shift_nodes, shift_deg):")
for md, n, s in rows[:8]:
    print(f"  {md:8.1f}  n={n:3d}  s={s:+4d}  {s*RES/1000:+8.2f} deg")
# also show s=0 and the exact-30 candidates for contrast
byS = {s: (md, n) for md, n, s in rows}
for s in (0, 166, 167, -166, -167):
    if s in byS:
        print(f"  contrast s={s:+4d} ({s*RES/1000:+.2f} deg): median={byS[s][0]:.1f} n={byS[s][1]}")
