# IM COOOOKING BUT STATISTICALLY

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#where are we going?
input_path = "ED_correct_flow_only.csv"


#load csv into daddyframr
df = pd.read_csv(input_path)


#define the steps
steps = {
    "Disposition → Bed Request": "Dispo to Bed Assigned (minutes)",
    "Disposition → Depart": "Disposition to Depart (minutes)",
    "Bed Assigned → Admit": "Bed Assigned to Admit (minutes)",
    "Bed Request → Admit": "Bed Request to Admit (minutes)"
}


stds = {}
ranges = {}


#fill up our lil variability stats
for label, column in steps.items():
    if column in df.columns:
        data = df[column].abs().dropna()
        stds[label] = data.std()
        ranges[label] = data.max() - data.min()


#plottttyyyyy
plt.figure()

plt.bar(stds.keys(), stds.values())

plt.xticks(rotation=45, ha="right")
plt.ylabel("Standard Deviation (Minutes)")
plt.title("Process Time Variability by EPIC Time Span")

plt.tight_layout()

#pop it up on my screen so I can manually save it
plt.show()


print("\nStandard Deviation by Step:")
for k, v in stds.items():
    print(f"{k}: {round(v,2)} minutes")

print("\nRange by Step (Max - Min):")
for k, v in ranges.items():
    print(f"{k}: {round(v,2)} minutes")

print("\nIf one bar is dramatically larger — that is your instability bottleneck.")
print("\nDone.\n")

print(df["Disposition to Depart (minutes)"].abs().describe())

print("Columns in CSV:")
for col in df.columns:
    print(col)

print("\nColumns being used:")
for label, column in steps.items():
    print(column, "→", column in df.columns)



# ── SEGMENT BREAKDOWN ────────────────────────────────────────────────────────
df["dispo_bed"]   = pd.to_numeric(df["Dispo to Bed Assigned (minutes)"], errors="coerce")
df["bed_admit"]   = pd.to_numeric(df["Bed Assigned to Admit (minutes)"], errors="coerce")
df["req_admit"]   = pd.to_numeric(df["Bed Request to Admit (minutes)"], errors="coerce")
df["req_to_assigned"]  = df["req_admit"] - df["bed_admit"]
df["dispo_to_request"] = df["dispo_bed"] - df["req_to_assigned"]

total_med = df["Disposition to Depart (minutes)"].abs().dropna().median()

print("\n\nSEGMENT STATS FOR PROCESS MAP")
print(f"{'Step':<32} {'Median':>8} {'SD':>8} {'P25':>8} {'P75':>8} {'% Tot':>7}")
print("-" * 75)
for label, col in [("Dispo → Bed Request", "dispo_to_request"),
                    ("Bed Request → Bed Assigned", "req_to_assigned"),
                    ("Bed Assigned → Admitted", "bed_admit"),
                    ("TOTAL: Dispo → Admitted", "Disposition to Depart (minutes)")]:
    v = pd.to_numeric(df[col], errors="coerce").dropna()
    v = v[v >= 0]
    print(f"{label:<32} {v.median():>7.0f}m {v.std():>7.0f}m {v.quantile(.25):>7.0f}m {v.quantile(.75):>7.0f}m {v.median()/total_med*100:>6.0f}%")
