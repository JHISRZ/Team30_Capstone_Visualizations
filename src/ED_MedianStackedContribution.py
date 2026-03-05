# WE ARE NOW COOKING FOR THE BOARDROOM

import pandas as pd
import matplotlib.pyplot as plt


#where are we going?
input_path = "/Users/jorgesuarez/Desktop/SENIOR DESIGN GIT/data/cleaned/ED_correct_flow_only.csv"


#load csv into daddyframr
df = pd.read_csv(input_path)


#define ONLY true sequential steps (no double counting)
steps = {
    "Disposition → Bed Request": "Dispo to Bed Assigned (minutes)",
    "Bed Request → Admit": "Bed Request to Admit (minutes)",
    "Bed Assigned → Admit": "Bed Assigned to Admit (minutes)"
}


medians = {}
total_median = 0


#calculate medians
for label, column in steps.items():
    if column in df.columns:
        value = df[column].abs().median()
        medians[label] = value
        total_median += value


#prepare stacked values
values = list(medians.values())
labels = list(medians.keys())


#plottttt
plt.figure()

bottom = 0

purple_shades = [
    "#E6E0F8",  # light
    "#7E57C2",  # medium
    "#4A148C"   # dark
]

for value, label, color in zip(values, labels, purple_shades):
    plt.bar("Median Total Admission Time", value, bottom=bottom, label=label, color=color)
    bottom += value


plt.ylabel("Minutes")
plt.title("Median Admission Time Breakdown")
plt.legend(loc="lower right", frameon=True)
plt.tight_layout()

#pop it up so I can save manually
plt.show()


print("\nMedian Contribution Breakdown:")
for k, v in medians.items():
    percent = (v / total_median) * 100
    print(f"{k}: {round(v,2)} min ({round(percent,1)}%)")

print(f"\nTotal Median Admission Time: {round(total_median,2)} minutes")
print("\nThis shows which stage consumes the largest share of total time.\n")