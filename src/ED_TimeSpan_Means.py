# IM COOOOKINGGGG

import pandas as pd
import matplotlib.pyplot as plt
import os


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

means = {}

#fill up our lil means
for label, column in steps.items():
    if column in df.columns:
        means[label] = df[column].abs().mean()


#plottttyyyyy
plt.figure()

plt.bar(means.keys(), means.values())

plt.xticks(rotation=45, ha="right")
plt.ylabel("Mean Minutes")
plt.title("Mean Time in Minutes per EPIC Time Span Type")

plt.tight_layout()

#pop it up on my screen so I can manually save it
plt.show()


print("\nMean Step Times:")
for k, v in means.items():
    print(f"{k}: {round(v,2)} minutes")

print("\nChart displayed — save manually as PNG.")
print("\nDone.\n")