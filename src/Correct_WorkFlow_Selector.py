#suarezz codeeeee 
#lfg
import pandas as pd

# paths
input_path = "/Users/jorgesuarez/Desktop/SENIOR DESIGN GIT/data/cleaned/ED_workflows_separated.csv"
output_path = "/Users/jorgesuarez/Desktop/SENIOR DESIGN GIT/data/cleaned/ED_correct_flow_only.csv"

#load that rame up boiiii
df = pd.read_csv(input_path)

print("\nLoaded ED_workflows_separated.csv")
print("Total rows:", len(df))


#selecting the correct workflow(waiitng approval
# from ragini on if true but 99.99% sure bc i like now th system atp)
correct_workflow = (
    "Disposition Before Request | "
    "Disposition Before Assigned | "
    "Assigned Before Admit"
)

#filter the dadddyframe
df_correct = df[df["Workflow_Type"] == correct_workflow]

print("\nCorrect workflow rows:", len(df_correct))

if len(df) > 0:
    print("Percentage of total:",
          round((len(df_correct) / len(df)) * 100, 2), "%")

#save to scv
df_correct.to_csv(output_path, index=False)

print("\nSaved file:")
print(output_path)
print("\nDone.\n")
