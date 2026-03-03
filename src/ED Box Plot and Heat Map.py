import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ── Try loading CSV; fall back to expected values ────────────────────────────
csv_path = "ED_cleaned.csv"
USE_FILE = os.path.exists(csv_path)

col_dispo = "Dispo to Bed Assigned (minutes)"
col_bed   = "Bed Assigned to Admit (minutes)"
col_floor = "Admitting Department"
col_day   = "Arrival Day of Week"

floor_order = [
    "PH 6TH FLR ACUTE CARE",
    "PH 5TH FLR ACUTE CARE",
    "PH 7TH FLR ACUTE CARE",
    "PH 4TH TELEMETRY",
    "PH 4TH FLOOR ICU",
]
short_names = {
    "PH 6TH FLR ACUTE CARE": "6th Floor\nAcute Care",
    "PH 5TH FLR ACUTE CARE": "5th Floor\nAcute Care",
    "PH 7TH FLR ACUTE CARE": "7th Floor\nAcute Care",
    "PH 4TH TELEMETRY":      "4th Floor\nTelemetry",
    "PH 4TH FLOOR ICU":      "4th Floor\nICU",
}
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

if USE_FILE:
    df = pd.read_csv(csv_path, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    df[col_dispo] = pd.to_numeric(df[col_dispo], errors="coerce")
    df[col_bed]   = pd.to_numeric(df[col_bed],   errors="coerce")

    medians_dispo = df.loc[df[col_dispo] > 0].groupby(col_floor)[col_dispo].median()
    medians_bed   = df.loc[df[col_bed]   > 0].groupby(col_floor)[col_bed].median()

    chart1_data = {}
    for f in floor_order:
        chart1_data[f] = {"dispo": medians_dispo.get(f, 0), "bed": medians_bed.get(f, 0)}

    df_pos = df.loc[df[col_dispo] > 0].copy()
    df_pos[col_day] = df_pos[col_day].str.strip()
    pivot = df_pos.groupby([col_floor, col_day])[col_dispo].median().unstack(fill_value=np.nan)
    pivot = pivot.reindex(index=floor_order, columns=day_order)
    print("Using actual CSV data.")
else:
    chart1_data = {
        "PH 6TH FLR ACUTE CARE": {"dispo": 646, "bed": 153},
        "PH 5TH FLR ACUTE CARE": {"dispo": 590, "bed": 147},
        "PH 7TH FLR ACUTE CARE": {"dispo": 386, "bed": 141},
        "PH 4TH TELEMETRY":      {"dispo": 104, "bed": 117},
        "PH 4TH FLOOR ICU":      {"dispo":  24, "bed":  51},
    }
    pivot_data = {
        "PH 6TH FLR ACUTE CARE": [720, 921, 680, 650, 420, 380, 540],
        "PH 5TH FLR ACUTE CARE": [660, 892, 620, 580, 350, 320, 500],
        "PH 7TH FLR ACUTE CARE": [440, 520, 400, 380, 220, 200, 310],
        "PH 4TH TELEMETRY":      [130, 160, 110, 100,  60,  55,  80],
        "PH 4TH FLOOR ICU":      [ 30,  40,  28,  25,  15,  12,  20],
    }
    pivot = pd.DataFrame(pivot_data, index=day_order).T
    pivot.columns = day_order
    pivot = pivot.reindex(index=floor_order)
    print("Using expected/approximate values (CSV not found).")

# ── Shared style ─────────────────────────────────────────────────────────────
BLUE   = "#2B6D9E"
ORANGE = "#D96A2B"
BG     = "#FFFFFF"
TEXT   = "#1E1E1E"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "text.color": TEXT,
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
})

# ═════════════════════════════════════════════════════════════════════════════
# CHART 1 — Horizontal stacked bar
# ═════════════════════════════════════════════════════════════════════════════
floors_plot = []
for f in reversed(floor_order):
    d = chart1_data[f]["dispo"]
    b = chart1_data[f]["bed"]
    floors_plot.append({"floor": f, "dispo": d, "bed": b, "total": d + b})

labels     = [short_names[r["floor"]] for r in floors_plot]
dispo_vals = [r["dispo"] for r in floors_plot]
bed_vals   = [r["bed"]   for r in floors_plot]
totals     = [r["total"] for r in floors_plot]
y_pos      = np.arange(len(labels))

fig1, ax1 = plt.subplots(figsize=(14, 5.8))

ax1.barh(y_pos, dispo_vals, height=0.52, color=BLUE,
         label="Waiting for Bed Assignment", zorder=3)
ax1.barh(y_pos, bed_vals, left=dispo_vals, height=0.52, color=ORANGE,
         label="Bed Assigned to Admitted", zorder=3)

for i in range(len(labels)):
    if dispo_vals[i] > 35:
        ax1.text(dispo_vals[i] / 2, y_pos[i],
                 f"{dispo_vals[i]/60:.1f} hrs",
                 va="center", ha="center", color="white",
                 fontsize=12.5, fontweight="bold")
    mid_o = dispo_vals[i] + bed_vals[i] / 2
    if bed_vals[i] > 35:
        ax1.text(mid_o, y_pos[i],
                 f"{bed_vals[i]/60:.1f} hrs",
                 va="center", ha="center", color="white",
                 fontsize=12.5, fontweight="bold")
    ax1.text(totals[i] + 14, y_pos[i],
             f"{totals[i]/60:.1f} hrs",
             va="center", ha="left", color=TEXT,
             fontsize=13, fontweight="bold")

ax1.set_yticks(y_pos)
ax1.set_yticklabels(labels, fontsize=13, linespacing=1.15)
ax1.set_title("Median Post-Disposition Wait by Inpatient Floor",
              fontsize=19, fontweight="bold", pad=22, loc="left")
ax1.legend(loc="lower right", fontsize=12.5, frameon=False,
           borderpad=1, handlelength=1.8)
ax1.set_xlim(0, max(totals) * 1.30)

for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.tick_params(left=False, bottom=False)
ax1.xaxis.set_visible(False)
ax1.grid(False)

fig1.tight_layout()
fig1.savefig("chart1_stacked_bar.png", dpi=300, bbox_inches="tight")
print("Chart 1 saved.")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 2 — Heatmap
# ═════════════════════════════════════════════════════════════════════════════
data = pivot.values.astype(float)
vmax = np.nanmax(data)

fig2, ax2 = plt.subplots(figsize=(14, 6.2))

cmap = plt.cm.RdYlGn_r
im = ax2.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=vmax)

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        val = data[i, j]
        if np.isnan(val):
            continue
        hrs = val / 60
        norm = val / vmax
        txt_c = "white" if norm > 0.6 or norm < 0.12 else TEXT
        ax2.text(j, i, f"{hrs:.1f}\nhrs",
                 va="center", ha="center",
                 fontsize=11, fontweight="bold", color=txt_c,
                 linespacing=1.15)

short_days = [d[:3] for d in day_order]
ax2.set_xticks(np.arange(len(day_order)))
ax2.set_xticklabels(short_days, fontsize=13, fontweight="bold")
ax2.xaxis.set_ticks_position("top")

short_floors = [short_names[f] for f in floor_order]
ax2.set_yticks(np.arange(len(floor_order)))
ax2.set_yticklabels(short_floors, fontsize=13, linespacing=1.15)

ax2.set_title("Median Hours Waiting for Bed Assignment by Floor and Day of Week",
              fontsize=17, fontweight="bold", pad=32, loc="left")

cbar = fig2.colorbar(im, ax=ax2, shrink=0.78, pad=0.025)
cbar.set_label("Minutes", fontsize=12, labelpad=10)
cbar.ax.tick_params(labelsize=11)
cbar.outline.set_visible(False)

for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.tick_params(left=False, top=False, bottom=False)
ax2.grid(False)

fig2.tight_layout()
fig2.savefig("chart2_heatmap.png", dpi=300, bbox_inches="tight")
print("Chart 2 saved.")

print("\n── Chart 1 values (minutes) ──")
for f in floor_order:
    d = chart1_data[f]["dispo"]
    b = chart1_data[f]["bed"]
    print(f"  {f}: dispo={d:.0f}  bed={b:.0f}  total={d+b:.0f}")

print("\n── Chart 2 pivot (minutes) ──")
print(pivot.to_string(float_format="{:.0f}".format))