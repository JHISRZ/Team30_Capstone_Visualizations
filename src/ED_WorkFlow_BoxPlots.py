# CONTNUING TO COOK IN FULL SPEED BABY

import pandas as pd
import matplotlib.pyplot as plt


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


data_to_plot = []
labels = []


#collect clean absolute values
for label, column in steps.items():
    if column in df.columns:
        clean_data = df[column].abs().dropna()
        data_to_plot.append(clean_data)
        labels.append(label)


#plotttttt
plt.figure()

box = plt.boxplot(
    data_to_plot,
    labels=labels,
    showfliers=False,
    patch_artist=True   # THIS lets us color the boxes
)

#different shades of purple (professional gradient vibes)
purple_shades = [
    "#E6E0F8",  # very light lavender
    "#B39DDB",  # soft purple
    "#7E57C2",  # medium purple
    "#4A148C"   # deep royal purple
]

for patch, color in zip(box['boxes'], purple_shades):
    patch.set_facecolor(color)

plt.xticks(rotation=45, ha="right")
plt.ylabel("Minutes")
plt.title("EPIC Time Span Distributions")

plt.tight_layout()

#pop it up so I can save manually
plt.show()


print("\nBoxplot displayed.")
print("Purple gradient applied.")
print("Look at IQR height + whisker length.")
print("That is your real bottleneck signature.\n")

for label, column in steps.items():
    data = df[column].abs().dropna()
    print(label)
    print("Median:", data.median())
    print("IQR:", data.quantile(0.75) - data.quantile(0.25))
    print()
    