"""Профиль дистанции/интенсивности по угловой метке из сырых кадров MSOP.

Вход — каталоги `frame_*.bin`, сохранённые `msop_tcp_sniff.py --raw-dir`.
Для каждого каталога считает медиану дистанции и интенсивности на каждом узле
сетки по всем кадрам и печатает сводку + таблицу через ~4 градуса.

    python msop_angle_profile.py <raw_dir> [<raw_dir2> ...]

Нужен как эталон сцены: сравнение двух профилей даёт угловой сдвиг тела кадра
(см. msop_body_shift_scan.py).
"""
import sys, os, glob, statistics, importlib.util

spec = importlib.util.spec_from_file_location(
    "sniff", r"C:\workspace\verilog\.agents\skills\fpga-dev\scripts\msop_tcp_sniff.py")
sniff = importlib.util.module_from_spec(spec)
sys.modules["sniff"] = sniff
spec.loader.exec_module(sniff)

def load_dir(d):
    per_angle = {}          # mdeg -> list of dst
    per_angle_int = {}      # mdeg -> list of intensity
    headers = []
    for f in sorted(glob.glob(os.path.join(d, "frame_*.bin"))):
        pkt = open(f, "rb").read()
        hdr = sniff.parse_header(pkt) if hasattr(sniff, "parse_header") else None
        if hdr is None:
            vals = sniff.TCP_HEADER_V1.unpack_from(pkt, len(sniff.START))
            hdr = dict(zip(sniff.HEADER_FIELDS, vals))
        pts = sniff.parse_points(pkt, hdr)
        headers.append(hdr)
        fa = hdr["first_point_angle"]; res = hdr["angle_res"]
        for k, p in enumerate(pts):
            a = fa + k * res
            per_angle.setdefault(a, []).append(p["distance"])
            per_angle_int.setdefault(a, []).append(p["intensity"])
    return per_angle, per_angle_int, headers

def profile(per_angle, per_angle_int):
    prof = {}
    for a, ds in per_angle.items():
        nz = [d for d in ds if d not in (0, 0xFFFF, 0xFFFFFF)]
        ints = [i for d, i in zip(ds, per_angle_int[a]) if d not in (0, 0xFFFF, 0xFFFFFF)]
        prof[a] = (statistics.median(nz) if nz else None,
                   statistics.median(ints) if ints else None,
                   len(nz), len(ds))
    return prof

results = {}
for d in sys.argv[1:]:
    per_angle, per_angle_int, headers = load_dir(d)
    prof = profile(per_angle, per_angle_int)
    results[d] = prof
    fas = sorted({h["first_point_angle"] for h in headers})
    pcs = sorted({h["point_count"] for h in headers})
    frame_nums = [h["frame_number"] if "frame_number" in h else h.get("frame_num") for h in headers]
    all_int = [i for a in per_angle_int for i in per_angle_int[a]]
    nz_int = [i for i in all_int if i]
    print(f"== {d}: frames={len(headers)} fa={fas} pc={pcs} "
          f"int_median={statistics.median(nz_int) if nz_int else None} "
          f"int_min/max={min(nz_int) if nz_int else None}/{max(nz_int) if nz_int else None}")

# side-by-side profile on 2-deg grid
dirs = list(results)
grid = sorted({a for d in dirs for a in results[d]})
print("\nangle_deg | " + " | ".join(f"{os.path.basename(d)} d_mm(int)[n]" for d in dirs))
step = 4000
next_a = None
for a in grid:
    if next_a is not None and a < next_a:
        continue
    next_a = a + step
    row = [f"{a/1000:8.2f}"]
    for d in dirs:
        v = results[d].get(a)
        row.append(f"{v[0]:6.0f}({v[1]:3.0f})[{v[2]:2d}]" if v and v[0] is not None
                   else ("   -   " if v else "  n/a  "))
    print(" | ".join(row))
