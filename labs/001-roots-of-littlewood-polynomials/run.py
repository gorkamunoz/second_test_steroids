"""Density of the complex roots of every degree-n polynomial with ±1 coefficients.

Usage: python run.py [config.yaml]
Writes figures/littlewood_roots.png, results.json, and the raw roots to outputs/roots.npy.
"""
import json
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.colors import LinearSegmentedColormap, LogNorm

HERE = Path(__file__).parent
cfg = yaml.safe_load(open(sys.argv[1] if len(sys.argv) > 1 else HERE / "config.yaml"))
n, chunk = cfg["degree"], cfg["chunk"]
(HERE / "outputs").mkdir(exist_ok=True)
(HERE / "figures").mkdir(exist_ok=True)

# --- roots: eigenvalues of companion matrices, batched ---
# p(z) = z^n + a_{n-1} z^{n-1} + ... + a_0 with a_k in {-1,+1}; bit k of the index sets a_k.
t0 = time.time()
N = 2 ** n
roots = np.empty((N, n), dtype=np.complex128)
for start in range(0, N, chunk):
    idx = np.arange(start, min(start + chunk, N))
    coeffs = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)  # (B, n): a_0..a_{n-1}
    C = np.zeros((len(idx), n, n))
    C[:, 1:, :-1] = np.eye(n - 1)       # sub-diagonal ones
    C[:, :, -1] = -coeffs               # last column: -a_0 ... -a_{n-1}
    roots[idx] = np.linalg.eigvals(C)
z = roots.ravel()
np.save(HERE / "outputs" / "roots.npy", roots.astype(np.complex64))  # ~170 MB, git-ignored
elapsed = time.time() - t0

# --- summary numbers ---
r = np.abs(z)
n_real = (np.abs(roots.imag) < 1e-9).sum(axis=1)
results = {
    "degree": n,
    "n_polynomials": N,
    "n_roots": int(z.size),
    "min_abs_root": float(r.min()),
    "max_abs_root": float(r.max()),
    "frac_within_0.1_of_unit_circle": float(np.mean(np.abs(r - 1) < 0.1)),
    "frac_within_0.05_of_unit_circle": float(np.mean(np.abs(r - 1) < 0.05)),
    "mean_real_roots_per_poly": float(n_real.mean()),
    "min_dist_to_z=1": float(np.abs(z - 1).min()),
    "min_dist_to_z=i": float(np.abs(z - 1j).min()),
    "compute_seconds": round(elapsed, 1),
}
json.dump(results, open(HERE / "results.json", "w"), indent=2)
print(json.dumps(results, indent=2))

# --- figure ---
# Sequential single-hue ramp (blue, light -> dark) on a white surface; log density.
cmap = LinearSegmentedColormap.from_list(
    "blue_seq", ["#ffffff", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#104281", "#0d366b", "#06182f"])

def density(ax, g, title):
    H, xe, ye = np.histogram2d(z.real, z.imag, bins=g["bins"], range=[g["xlim"], g["ylim"]])
    H = np.where(H > 0, H, np.nan)
    im = ax.imshow(H.T, origin="lower", extent=[*g["xlim"], *g["ylim"]], cmap=cmap,
                   norm=LogNorm(vmin=1, vmax=np.nanmax(H)), interpolation="nearest", aspect="equal")
    ax.set_title(title, fontsize=11, loc="left", color="#222222")
    ax.set_xlabel("Re z", color="#555555"); ax.set_ylabel("Im z", color="#555555")
    ax.tick_params(colors="#555555", labelsize=8)
    for s in ax.spines.values():
        s.set_color("#bbbbbb")
    return im

fig, axes = plt.subplots(1, 2, figsize=(14, 7.2), constrained_layout=True)
gf, gz = cfg["grid"]["full"], cfg["grid"]["zoom"]
density(axes[0], gf, f"All {z.size/1e6:.1f}M roots of the {N:,} degree-{n} ±1 polynomials")
axes[0].add_patch(plt.Rectangle((gz["xlim"][0], gz["ylim"][0]), np.ptp(gz["xlim"]), np.ptp(gz["ylim"]),
                                fill=False, ec="#c0392b", lw=1.2))
im = density(axes[1], gz, "Zoom (red box): self-similar fractal \"dragons\" on the inner edge")
cb = fig.colorbar(im, ax=axes, shrink=0.8, pad=0.01)
cb.set_label("roots per pixel (log scale)", color="#555555")
cb.ax.tick_params(colors="#555555", labelsize=8)
fig.savefig(HERE / "figures" / "littlewood_roots.png", dpi=130, facecolor="white")
print("figure written")
