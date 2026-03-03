# i want to yse pandas and re
#this is suarez code
import pandas as pd
import re
#forgot i need os
import os


# naming the file path exactly
FILE_PATH = "/Users/jorgesuarez/Desktop/SENIOR DESIGN GIT/Original_Data/EVS_20260130_1639.csv"

# loading the csv into dataframr
#this is what i mentioned as a baseball card
#from cs 2316
df = pd.read_csv(FILE_PATH)

print("Original Shape:", df.shape)

# separate the duration columns 
duration_cols = [
    "Active -> Assigned",
    "Actv -> Comp/Canc/Skip",
    "Ack -> Comp",
    "Effective -> Entry"
]

#alright lets clean the hour and minutes with the durations
def parse_duration(value):
    if pd.isna(value):
        return None
    
    value = str(value).lower().strip()

    hours = 0
    minutes = 0

    # Extract hours
    hour_match = re.search(r"(\d+)\s*h", value)
    if hour_match:
        hours = int(hour_match.group(1))

    # Extract minutes
    minute_match = re.search(r"(\d+)\s*m", value)
    if minute_match:
        minutes = int(minute_match.group(1))

    # If it’s just a number like "23"
    if not hour_match and not minute_match:
        digits = re.search(r"\d+", value)
        if digits:
            minutes = int(digits.group(0))

    total_minutes = hours * 60 + minutes
    return total_minutes if total_minutes != 0 else None


for col in duration_cols:
    df[col] = df[col].apply(parse_duration)


# === Ensure Clean Folder Exists ===
os.makedirs("data/cleaned", exist_ok=True)

# === Save Clean Version ===
df.to_csv("data/cleaned/EVS_cleaned.csv", index=False)

print("\nCleaned file saved to data/cleaned/EVS_cleaned.csv")