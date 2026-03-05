import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv("data/cleaned/ED_cleaned.csv")

print("Loaded cleaned dataset.")
print("Rows:", len(df))

# we want to classify the work flows based on the signs of the timespans

# If Bed Request to Admit is negative,
# Bed Request happened BEFORE Disposition

df["Disposition_vs_Bed_Request"] = np.where(
    df["Bed Request to Admit (minutes)"] < 0,
    "Request Before Disposition",
    "Disposition Before Request"
)


# Bed Request vs Bed Assigned
df["Request_vs_Assigned"] = np.where(
    df["Dispo to Bed Assigned (minutes)"] < 0,
    "Assigned Before Disposition",
    "Disposition Before Assigned"
)


# Bed Assigned vs Admit
df["Assigned_vs_Admit"] = np.where(
    df["Bed Assigned to Admit (minutes)"] < 0,
    "Admit Before Assigned",
    "Assigned Before Admit"
)

# Creating labels for the work flow type

df["Workflow_Type"] = (
    df["Disposition_vs_Bed_Request"] + " | " +
    df["Request_vs_Assigned"] + " | " +
    df["Assigned_vs_Admit"]
)



# Total scope defined as Disposition to Depart
# Keep raw but create absolute version for analysis

df["Total_Time_In_Scope_Abs"] = df["Disposition to Depart (minutes)"].abs()


# SAVE SEGMENTED FILE

df.to_csv("data/cleaned/ED_workflows_separated.csv", index=False)

print("Workflow segmentation complete.")
print("Unique workflow types:")
print(df["Workflow_Type"].value_counts())

print("\nWorkflow Distribution (%):")
print(
    (df["Workflow_Type"].value_counts(normalize=True) * 100)
    .round(2)
)

