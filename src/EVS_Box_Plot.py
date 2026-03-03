import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading my cleaned csv babyt :3
df = pd.read_csv("data/cleaned/EVS_cleaned.csv")

# lets find druation columns
duration_cols = [
    "Active -> Assigned",
    "Actv -> Comp/Canc/Skip",
    "Ack -> Comp",
    "Effective -> Entry"
]
# make em a little more understandable labels for plots
friendly_labels = [
    "Active → Assigned",
    "Active → Completed/Canceled/Skipped",
    "Acknowledged → Completed",
    "Effective → Entry"]

#make some boxplotzzzzzz
plt.figure(figsize=(10,6))
#not outlier bc they really crowd the graph
sns.boxplot(data=df[duration_cols], showfliers=False)
plt.xticks(ticks=range(len(friendly_labels)), labels=friendly_labels, rotation=20)
plt.ylabel("Minutes")
plt.title("Distribution of Durations (Outliers Removed)")
plt.tight_layout()
plt.show()



