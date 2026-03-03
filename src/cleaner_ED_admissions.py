import pandas as pd

# --------------------------------------------------
# Loadthe cassise data (but EPIC puts trash above the real header so we fix that)
# --------------------------------------------------

file_path = "Original_Data/ED_Encounters_Admissions_Inpatient4to7.csv"

# load raw without assuming header row
df_raw = pd.read_csv(file_path, header=None, low_memory=False)

# find the actual header row that contains ED Disposition
header_row_index = None
for i in range(len(df_raw)):
    row_values = df_raw.iloc[i].astype(str).tolist()
    if "ED Disposition" in row_values:
        header_row_index = i
        break

if header_row_index is None:
    raise ValueError("Could not find header row containing 'ED Disposition' because EPIC SUCKS")

print(f"Detected real header row at index: {header_row_index}")

# now reload properly using correct header row
df = pd.read_csv(
    file_path,
    skiprows=header_row_index,
    low_memory=False
)

# Strip whitespace from column names because EPIC SUCKS
df.columns = df.columns.str.strip()

# actual columns named for identiying them
print("\nACTUAL COLUMN NAMES:\n")
for col in df.columns:
    print(repr(col))

print("Cleaned column names loaded.")
print("Total rows before filtering:", len(df))


# --------------------------------------------------
# FILTER TO CORRECT POPULATION
# --------------------------------------------------

# keep only patients that were admitted
df = df[df["ED Disposition"].str.contains("Admit", case=False, na=False)]

# keep only PH 4TH–7TH admitting departments
departments_to_keep = ["PH 4TH", "PH 5TH", "PH 6TH", "PH 7TH"]

df = df[df["Admitting Department"].str.contains(
    "|".join(departments_to_keep),
    case=False,
    na=False
)]

print("Filtered rows after admission + department filter:", len(df))


# --------------------------------------------------
# The timeopsans athat are actually in the scope
# find the 4 columns using partial matching
# --------------------------------------------------

minutes_to_keep = []

for col in df.columns:
    if "Dispo" in col and "Bed Assigned" in col:
        minutes_to_keep.append(col)
    elif "Disposition" in col and "Depart" in col:
        minutes_to_keep.append(col)
    elif "Bed Assigned" in col and "Admit" in col:
        minutes_to_keep.append(col)
    elif "Bed Request" in col and "Admit" in col:
        minutes_to_keep.append(col)

print("Columns detected for scope:")
print(minutes_to_keep)


# Identify all columns that are timespasns
all_minute_columns = [col for col in df.columns if "(minutes)" in col]

# take out the columns we awanan drop wagwan!
minutes_to_drop = [col for col in all_minute_columns if col not in minutes_to_keep]

# Drop em out
df_clean = df.drop(columns=minutes_to_drop)

# make em nurmeric for statistics, screw you dirty epic data you sucj
for col in minutes_to_keep:
    if col in df_clean.columns:   # safety check so it don’t crash
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# --------------------------------------------------
# Save the cleaned csv
# --------------------------------------------------

df_clean.to_csv("data/cleaned/ED_cleaned.csv", index=False)

print("CLEANED THAT HOE BBG!")
print("Columns kept:", len(df_clean.columns))
print("Rows:", len(df_clean))


