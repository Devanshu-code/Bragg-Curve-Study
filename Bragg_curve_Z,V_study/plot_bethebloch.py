#!/usr/bin/env python3
"""
plot_bethebloch.py
------------------
Runs all Bethe-Bloch study simulations and produces two plots:

  Plot 1 — Velocity (v) study:
      Proton at 2 MeV, 4 MeV, 8 MeV → same z, different v
      Shows: higher v → smaller dE/dx → deeper, lower Bragg peak

  Plot 2 — Charge (z) study:
      Proton (z=1) vs Alpha (z=2) at same energy per nucleon
      Shows: higher z → much larger dE/dx ∝ z²

Usage (run from project root):
    python3 plot_bethebloch.py

Requires: matplotlib
"""

import subprocess, re, os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

EXE = "./build/bragg_curve"

def run_sim(mac_file):
    """Run simulation and return (label, depths, edeps)."""
    if not os.path.exists(EXE):
        print(f"ERROR: {EXE} not found. Build first:\n  cd build && cmake .. && make -j4")
        raise SystemExit(1)

    print(f"  Running {mac_file} ...")
    proc = subprocess.Popen([EXE, mac_file],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True)

    label, depths, edeps = "unknown", [], []
    for line in proc.stdout:
        # Parse header
        m = re.search(r'BRAGG DATA: particle=(\S+) energy=([\d\.]+)MeV z=(\d+)', line)
        if m:
            pname  = m.group(1)
            energy = m.group(2)
            z      = m.group(3)
            label  = f"{pname} {energy} MeV (z={z})"
            continue
        # Parse data
        m2 = re.search(r'depth: ([\d\.]+) mm, edep: ([\d\.eE\+\-]+) keV/event', line)
        if m2:
            depths.append(float(m2.group(1)))
            edeps.append(float(m2.group(2)))

    proc.wait()
    # Fallback label from filename
    if label == "unknown":
        label = os.path.basename(mac_file).replace("run_","").replace(".mac","")
    return label, depths, edeps


# ── Run all simulations ───────────────────────────────────────────────────────

print("=== Velocity (v) Study: Proton at 2, 4, 8 MeV ===")
v_runs = [
    ("run_proton_2MeV.mac", "#e74c3c"),
    ("run_proton_4MeV.mac", "#2980b9"),
    ("run_proton_8MeV.mac", "#27ae60"),
]

print("\n=== Charge (z) Study: Proton vs Alpha ===")
z_runs = [
    ("run_proton_4MeV.mac",  "#2980b9"),   # z=1, 4 MeV
    ("run_proton_8MeV.mac",  "#27ae60"),   # z=1, 8 MeV
    ("run_alpha_4MeV.mac",   "#e74c3c"),   # z=2, 4 MeV (same E, higher z)
    ("run_alpha_8MeV.mac",   "#e67e22"),   # z=2, 8 MeV
]

# Collect all unique macs to avoid running twice
all_macs = list(dict.fromkeys([m for m,_ in v_runs] + [m for m,_ in z_runs]))
cache = {}
for mac in all_macs:
    label, depths, edeps = run_sim(mac)
    cache[mac] = (label, depths, edeps)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Bethe-Bloch Theorem Verification — Bragg Curve in Argon Gas\n"
             r"$-dE/dx \propto z^2/v^2$    (Geant4 Simulation, 10,000 events)",
             fontsize=13, fontweight='bold')

# ── Plot 1: Velocity study ────────────────────────────────────────────────────
ax1 = axes[0]
ax1.set_title(r"Effect of Velocity (v):  same $z=1$ (proton), different $E$",
              fontsize=11)

for mac, col in v_runs:
    label, depths, edeps = cache[mac]
    ax1.plot(depths, edeps, color=col, linewidth=2, label=label)
    # Mark peak
    if edeps:
        pk_i = edeps.index(max(edeps))
        ax1.axvline(depths[pk_i], color=col, linestyle=':', alpha=0.5, linewidth=1)
        ax1.annotate(f"{depths[pk_i]:.0f} mm",
                     xy=(depths[pk_i], max(edeps)),
                     xytext=(depths[pk_i]+5, max(edeps)*0.9),
                     fontsize=8, color=col)

ax1.fill_between([], [], alpha=0)   # dummy
ax1.set_xlabel("Depth in Argon Gas (mm)", fontsize=12)
ax1.set_ylabel("Energy Deposition (keV / event)", fontsize=12)
ax1.legend(fontsize=9, loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)

# Add theory note
ax1.text(0.97, 0.97,
         "Higher v (E) →\nlower dE/dx\n→ deeper peak",
         transform=ax1.transAxes, ha='right', va='top',
         fontsize=9, style='italic',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# ── Plot 2: Charge study ──────────────────────────────────────────────────────
ax2 = axes[1]
ax2.set_title(r"Effect of Charge (z):  proton ($z=1$) vs alpha ($z=2$)",
              fontsize=11)

for mac, col in z_runs:
    label, depths, edeps = cache[mac]
    ls = '-' if 'proton' in mac else '--'
    ax2.plot(depths, edeps, color=col, linewidth=2, linestyle=ls, label=label)
    if edeps:
        pk_i = edeps.index(max(edeps))
        ax2.axvline(depths[pk_i], color=col, linestyle=':', alpha=0.4, linewidth=1)

ax2.set_xlabel("Depth in Argon Gas (mm)", fontsize=12)
ax2.set_ylabel("Energy Deposition (keV / event)", fontsize=12)
ax2.legend(fontsize=9, loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(left=0)
ax2.set_ylim(bottom=0)

ax2.text(0.97, 0.97,
         r"Higher $z$ →" + "\nmuch larger dE/dx\n" + r"(scales as $z^2$)",
         transform=ax2.transAxes, ha='right', va='top',
         fontsize=9, style='italic',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
os.makedirs("results", exist_ok=True)
plt.savefig("results/bethebloch_study.png", dpi=150)
print("\nSaved: results/bethebloch_study.png")
plt.show()

# ── Summary table ─────────────────────────────────────────────────────────────
print("\n" + "="*65)
print(f"  {'Run':<30} {'Peak depth (mm)':>16} {'Peak dE/dx':>12}")
print("  " + "-"*58)
for mac in all_macs:
    label, depths, edeps = cache[mac]
    if edeps and max(edeps) > 0:
        pk_i = edeps.index(max(edeps))
        print(f"  {label:<30} {depths[pk_i]:>16.1f} {max(edeps):>10.2f} keV/ev")
print("="*65)
