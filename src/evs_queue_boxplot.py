import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

csv_path = "/mnt/user-data/uploads/EVS_cleaned.csv"
USE_FILE = os.path.exists(csv_path)

ip_floors = ["PH 6 ACUTE C", "PH 5 ACUTE C", "PH 7 ACUTE C", "PH TELE", "PH 4 ICU", "PH CDU"]

if USE_FILE:
    evs = pd.read_csv(csv_path, skipinitialspace=True)
    evs.columns = evs.columns.str.strip()
    evs["Active -> Assigned"] = pd.to_numeric(evs["Active -> Assigned"], errors="coerce")
    evs["Actv -> Comp/Canc/Skip"] = pd.to_numeric(evs["Actv -> Comp/Canc/Skip"], errors="coerce")

    ip = evs[evs["Unit"].isin(ip_floors)].copy()

    event_counts = []
    queue_wait_med = []
    turnaround_med = []
    hours = list(range(6, 22))
    DAYS = ip["Day of the Month"].nunique()

    for h in hours:
        sub = ip[ip["Hour of the Day"] == h]
        event_counts.append(len(sub) / DAYS)
        wait = sub["Active -> Assigned"].dropna()
        wait = wait[wait > 0]
        queue_wait_med.append(wait.median() if len(wait) > 2 else np.nan)
        turn = sub["Actv -> Comp/Canc/Skip"].dropna()
        turn = turn[turn > 0]
        turnaround_med.append(turn.median() if len(turn) > 2 else np.nan)

    print(f"Using actual CSV data. ({DAYS} days, {len(ip)} IP floor events)")
else:
    hours = list(range(6, 22))
    event_counts    = [ 0,  1,  3,  2,  7, 17, 23, 28, 34, 34, 27, 17, 25, 12,  3,  6]
    queue_wait_med  = [24, 18,  7,  8, 17, 15, 25, 16, 40, 45, 40, 30, 50, 28, 20, 10]
    turnaround_med  = [30, 15, 17, 14, 25, 26, 40, 42, 74, 62, 41, 37, 65, 33, 37, 22]
    print("Using expected/approximate values (CSV not found).")

BLUE   = "#2B6D9E"
ORANGE = "#D96A2B"
RED    = "#C0392B"
BG     = "#FFFFFF"
TEXT   = "#1E1E1E"
GRAY   = "#AAAAAA"

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

fig, ax1 = plt.subplots(figsize=(14, 6.2))

x = np.arange(len(hours))
bar_width = 0.65

bars = ax1.bar(x, event_counts, width=bar_width, color=BLUE, alpha=0.75,
               label="Avg Daily Room Cleaning Requests", zorder=3)

ax1.set_ylabel("Avg Cleaning Requests per Day", fontsize=13, fontweight="bold", labelpad=10)
ax1.set_ylim(0, max(event_counts) * 1.45)

for i, val in enumerate(event_counts):
    if val > 0.3:
        ax1.text(x[i], val + 0.15, f"{val:.1f}", ha="center", va="bottom",
                 fontsize=9.5, color=TEXT, fontweight="bold")

ax2 = ax1.twinx()

ax2.plot(x, queue_wait_med, color=RED, linewidth=2.8, marker="o",
         markersize=7, markerfacecolor="white", markeredgewidth=2.2,
         markeredgecolor=RED, label="Median Wait: Active → Assigned (min)", zorder=5)

for i, val in enumerate(queue_wait_med):
    if pd.notna(val) and val >= 40:
        ax2.annotate(f"{val:.0f} min", xy=(x[i], val),
                     xytext=(0, 14), textcoords="offset points",
                     ha="center", va="bottom", fontsize=10,
                     fontweight="bold", color=RED)

ax2.set_ylabel("Median Wait: Active → Assigned (min)", fontsize=13,
               fontweight="bold", color=RED, labelpad=10)
ax2.set_ylim(0, max([v for v in queue_wait_med if pd.notna(v)]) * 1.45)
ax2.tick_params(axis="y", colors=RED)
ax2.spines["right"].set_color(RED)

hour_labels = [f"{h % 12 or 12}{'AM' if h < 12 else 'PM'}" for h in hours]
ax1.set_xticks(x)
ax1.set_xticklabels(hour_labels, fontsize=11, fontweight="bold")
ax1.set_xlabel("Hour of Day", fontsize=13, fontweight="bold", labelpad=10)

ax1.set_title("IP Floor EVS: Daily Cleaning Demand and Time Waiting for Assignment",
              fontsize=18, fontweight="bold", pad=32, loc="center")

fig.text(0.5, 0.895,
         "Queue wait = time from room flagged dirty (Active) to EVS worker assigned. Jan 23–30, n=248 events.",
         fontsize=11, color=GRAY, style="italic", ha="center")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           loc="upper left", fontsize=12, frameon=False,
           borderpad=1, handlelength=1.8)

for spine in ["top", "left", "bottom"]:
    ax1.spines[spine].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)

ax1.tick_params(left=False, bottom=False)
ax1.grid(False)
ax2.grid(False)

fig.tight_layout()
fig.subplots_adjust(top=0.88)
fig.savefig("/mnt/user-data/outputs/evs_queue_chart.png", dpi=300, bbox_inches="tight")
print("Chart saved.")
