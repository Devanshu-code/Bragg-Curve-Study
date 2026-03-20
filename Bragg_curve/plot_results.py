#!/usr/bin/env python3
"""
plot_results.py
---------------
Runs the Geant4 Bragg curve simulation and plots energy deposition vs depth.
Annotates the Bragg peak position automatically.

Usage:
    python3 plot_results.py

Must be run from the project root directory (not from build/).
Requires: matplotlib
"""

import subprocess
import re
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def run_simulation():
    """Run Geant4 simulation and parse depth/edep output."""
    exe = "./build/bragg_curve"
    mac = "run1.mac"

    if not os.path.exists(exe):
        print(f"ERROR: {exe} not found. Build first:\n  cd build && cmake .. && make -j4")
        raise SystemExit(1)

    print(f"Running simulation: {exe} {mac} ...")
    process = subprocess.Popen(
        [exe, mac],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    depths, edeps = [], []
    for line in process.stdout:
        match = re.search(r'depth: ([\d\.]+) mm, edep: ([\d\.eE\+\-]+) keV/event', line)
        if match:
            depths.append(float(match.group(1)))
            edeps.append(float(match.group(2)))

    process.wait()
    print(f"Simulation complete. {len(depths)} depth bins recorded.")
    return depths, edeps


def plot(depths, edeps):
    """Plot the Bragg curve with peak annotation."""
    if not depths:
        print("No data to plot.")
        return

    # Find Bragg peak
    peak_idx   = edeps.index(max(edeps))
    peak_depth = depths[peak_idx]
    peak_edep  = edeps[peak_idx]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Fill under curve
    ax.fill_between(depths, edeps, alpha=0.15, color='royalblue')
    ax.plot(depths, edeps, 'royalblue', linewidth=2, label='Simulated energy deposition')

    # Annotate Bragg peak
    ax.axvline(peak_depth, color='crimson', linestyle='--', linewidth=1.5,
               label=f'Bragg peak: {peak_depth:.1f} mm')
    ax.annotate(f'Bragg Peak\n{peak_depth:.1f} mm\n{peak_edep:.2f} keV/event',
                xy=(peak_depth, peak_edep),
                xytext=(peak_depth - 60, peak_edep * 0.75),
                arrowprops=dict(arrowstyle='->', color='crimson'),
                color='crimson', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

    ax.set_xlabel("Depth in Argon Gas (mm)", fontsize=13)
    ax.set_ylabel("Energy Deposition (keV / event)", fontsize=13)
    ax.set_title("Bragg Curve — 4 MeV Protons in Argon Gas\n(Geant4 Simulation, 10,000 events)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, max(depths) * 1.05)
    ax.set_ylim(bottom=0)

    # Add physics note
    ax.text(0.02, 0.96,
            "Proton loses energy slowly at first\nthen deposits maximum energy\nat the Bragg peak before stopping",
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/bragg_curve.png", dpi=150)
    # Also save to root for README
    plt.savefig("bragg_curve.png", dpi=150)
    print("Saved: results/bragg_curve.png")
    plt.show()

    # Summary
    print(f"\n{'='*45}")
    print(f"  Bragg peak depth    : {peak_depth:.1f} mm")
    print(f"  Peak energy deposit : {peak_edep:.3f} keV/event")
    print(f"  Plateau avg (first 10 bins): "
          f"{sum(edeps[:10])/10:.3f} keV/event")
    print(f"  Peak / Plateau ratio: {peak_edep / (sum(edeps[:10])/10):.1f}×")
    print(f"{'='*45}")


if __name__ == "__main__":
    depths, edeps = run_simulation()
    plot(depths, edeps)
