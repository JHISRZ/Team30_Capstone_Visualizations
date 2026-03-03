import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Loading my cleaned csv babyt :3
df = pd.read_csv("data/cleaned/EVS_cleaned.csv")

# lets find duration columns
stages = [
    "Active -> Assigned",
    "Actv -> Comp/Canc/Skip",
    "Ack -> Comp",
    "Effective -> Entry"
]

# make friendly labels for plots
friendly_labels = [
    "Active → Assigned",
    "Active → Completed/Canceled/Skipped",
    "Acknowledged → Completed",
    "Effective → Entry"
]

# filter for discharges from the data frame
df_discharge = df[df["Event Type"].str.lower() == "discharge"].copy()

# make a Pivot table: rows=Hour, cols=Event Type, values= Effective -> Entry (mean duration)
# Since we only have discharge, it will just show one column
pivot = df_discharge.pivot_table(
    index="Hour of the Day",
    columns="Event Type",
    values="Effective -> Entry",
    aggfunc="mean"
)

# find em in 24 hour time format
# when each timespan is actually happening if we add tem up
for i, stage in enumerate(stages):
    if i == 0:
        df[f"{stage}_hour"] = df["Hour of the Day"] + df[stage]/60  # convert minutes to hours
    else:
        prev_stage = stages[i-1]
        df[f"{stage}_hour"] = df[f"{prev_stage}_hour"] + df[stage]/60

# Convert to 0-23 hour scale military time type shi
for stage in stages:
    df[f"{stage}_hour"] = df[f"{stage}_hour"] % 24

# Melt the dataframe to make the plotting easier
melt_df = df.melt(
    id_vars=["Hour of the Day"], 
    value_vars=[f"{s}_hour" for s in stages], 
    var_name="Stage", 
    value_name="Clock_Hour"
)

# Drop rows where Clock_Hour is NaN,
# then round hours to nearest integer 
melt_df = melt_df.dropna(subset=["Clock_Hour"])
melt_df["Clock_Hour_Rounded"] = melt_df["Clock_Hour"].round().astype(int)

# Pivot table: rows = clock hour, columns = stage
# , value are just a raw count
pivot = melt_df.pivot_table(
    index="Clock_Hour_Rounded",
    columns="Stage",
    values="Hour of the Day",  # just need a dummy column
    aggfunc="count",
    fill_value=0
)

#renaming with da friendly labels
pivot = pivot[ [f"{s}_hour" for s in stages] ]  # ensures column order
pivot.columns = friendly_labels

# Plot heatmap
#IM FOOKING COOKING
plt.figure(figsize=(12,6))
sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd", cbar_kws={'label': 'Number of Events'})
plt.title("Number of Discharge Events per Stage by Hour of Day")
plt.ylabel("Hour of Day (0-23)")
plt.xlabel("Time Stamp(+/- 59 minutes)")
plt.yticks(rotation=0)
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

