import pandas as pd

# Synthetic research-output data for portfolio demonstration only.
df = pd.DataFrame([
    ["R01", 125, 118, 7, 112],
    ["R02", 140, 132, 8, 126],
    ["R03", 110, 101, 9, 97],
    ["R04", 135, 130, 5, 128],
], columns=[
    "researcher", "records_built", "passed_initial_validation",
    "qa_exceptions", "campaign_ready"
])

df["initial_pass_rate"] = df["passed_initial_validation"] / df["records_built"]
df["campaign_ready_rate"] = df["campaign_ready"] / df["records_built"]
df["needs_review"] = df["qa_exceptions"] > 7

print("RESEARCH WORKFLOW SUMMARY")
print(df.to_string(index=False))

print("\nTOTALS")
print("Records built:", int(df["records_built"].sum()))
print("QA exceptions:", int(df["qa_exceptions"].sum()))
print("Campaign ready:", int(df["campaign_ready"].sum()))
print("Researchers flagged for review:", ", ".join(df.loc[df["needs_review"], "researcher"]))
