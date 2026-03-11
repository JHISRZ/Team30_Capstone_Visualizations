import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/cleaned/EVS_cleaned.csv")

# EVS workflow stages
stages = [
    "Active -> Assigned",
    "Actv -> Comp/Canc/Skip",
    "Ack -> Comp",
    "Effective -> Entry"
]

# Friendly labels
friendly_labels = [
    "Active → Assigned",
    "Active → Completed",
    "Acknowledged → Completed",
    "Effective → Entry"
]

bins = [0,10,25,50,100,float("inf")]

bucket_labels = [
    "0–10",
    "10–25",
    "25–50",
    "50–100",
    "100+"
]

bucket_data = []

for stage, label in zip(stages, friendly_labels):

    temp = df[[stage]].copy()

    # Convert to numeric
    temp[stage] = pd.to_numeric(temp[stage], errors="coerce")

    # Remove missing and negative values
    temp = temp.dropna()
    temp = temp[temp[stage] >= 0]

    temp["Time_Bucket"] = pd.cut(
        temp[stage],
        bins=bins,
        labels=bucket_labels,
    right=False
    )

    temp["Stage"] = label
    temp["Count"] = 1

    bucket_data.append(temp)

bucket_df = pd.concat(bucket_data)

# Pivot for heatmap
pivot = bucket_df.pivot_table(
    index="Stage",
    columns="Time_Bucket",
    values="Count",
    aggfunc="sum",
    fill_value=0
)

# Plot heatmap
plt.figure(figsize=(12,6))

sns.heatmap(
    pivot,
    annot=True,
    fmt="d",
    cmap="YlOrRd",
    cbar_kws={'label': 'Number of Events'}
)

plt.title("EVS Workflow Duration Buckets by Stage")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Workflow Stage")

plt.tight_layout()
plt.show()
print("\n==============================")
print("EVS TIMESPAN DISTRIBUTION SUMMARY")
print("==============================\n")

for stage, label in zip(stages, friendly_labels):

    data = pd.to_numeric(df[stage], errors="coerce").dropna()

    if len(data) == 0:
        print(f"{label}: No data available\n")
        continue

    print(f"--- {label} ---")

    # Basic descriptive stats
    print("Basic Stats (minutes):")
    print(data.describe())

    # Percentiles useful for bucket design
    print("\nKey Percentiles:")
    percentiles = data.quantile([0.25,0.5,0.75,0.9,0.95,0.99])
    print(percentiles)

    print("\n------------------------------\n")