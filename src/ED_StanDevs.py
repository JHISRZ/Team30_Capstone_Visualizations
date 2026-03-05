# IM COOOOKING BUT STATISTICALLY

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#where are we going?
input_path = "/Users/jorgesuarez/Desktop/SENIOR DESIGN GIT/data/cleaned/ED_correct_flow_only.csv"


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