import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/cleaned/ED_correct_flow_only.csv")

# Stage duration columns
stages = [
    "Bed Assigned to Admit (minutes)",
    "Bed Request to Admit (minutes)",
    "Dispo to Bed Assigned (minutes)",
    "Disposition to Depart (minutes)"
]

# Friendly labels
friendly_labels = [
    "Bed Assigned → Admit",
    "Bed Request → Admit",
    "Disposition → Bed Assigned",
    "Disposition → Depart"
]

bins = [0,60,180,600,1200,float("inf")]

bucket_labels = [
    "0–60",
    "60–180",
    "180–600",
    "600–1200",
    "1200+"
]

stage_labels = {
    "Bed Assigned to Admit (minutes)": [
        "0–60",
        "60–120",
        "120–180",
        "180–300",
        "300+"
    ],
    "Bed Request to Admit (minutes)": [
        "0–300",
        "300–600",
        "600–1200",
        "1200–1800",
        "1800+"
    ],
    "Dispo to Bed Assigned (minutes)": [
        "0–60",
        "60–300",
        "300–900",
        "900–1500",
        "1500+"
    ],
    "Disposition to Depart (minutes)": [
        "0–180",
        "180–450",
        "450–1000",
        "1000–1600",
        "1600+"
    ]
}

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

# Pivot table for heatmap
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

plt.title("ED Workflow Duration Buckets by Stage")
plt.xlabel("Time Bucket")
plt.ylabel("Workflow Stage")

plt.tight_layout()
plt.show()

print("\n==============================")
print("TIMESPAN DISTRIBUTION SUMMARY")
print("==============================\n")

for stage, label in zip(stages, friendly_labels):
    
    data = pd.to_numeric(df[stage], errors="coerce").dropna()
    
    if len(data) == 0:
        print(f"{label}: No data available\n")
        continue

    print(f"--- {label} ---")
    
    # Basic descriptive statistics
    print("Basic Stats (minutes):")
    print(data.describe())

    # Quantiles useful for bucket design
    print("\nKey Percentiles:")
    percentiles = data.quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    print(percentiles)

    print("\n------------------------------\n")