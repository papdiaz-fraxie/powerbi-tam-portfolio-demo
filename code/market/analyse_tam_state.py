import pandas as pd

# Source-derived aggregate counts from the original client TAM report.
# No client company/contact-level records are included.
state_counts = pd.DataFrame([
    ["NSW", 12953],
    ["VIC", 11240],
    ["QLD", 6530],
    ["WA", 3724],
    ["SA", 2264],
    ["TAS", 597],
    ["ACT", 470],
    ["NT", 215],
], columns=["state", "companies"])

TOTAL_TAM = 37993

# Validate that the state breakdown reconciles to the reported total.
assert state_counts["companies"].sum() == TOTAL_TAM

state_counts["share_of_tam"] = state_counts["companies"] / TOTAL_TAM
state_counts = state_counts.sort_values("companies", ascending=False).reset_index(drop=True)
state_counts["cumulative_companies"] = state_counts["companies"].cumsum()
state_counts["cumulative_share"] = state_counts["cumulative_companies"] / TOTAL_TAM

nsw_vic = state_counts.loc[state_counts["state"].isin(["NSW", "VIC"]), "companies"].sum()
top_three = state_counts.head(3)["companies"].sum()

print("AUSTRALIAN TAM BY STATE")
print(
    state_counts.assign(
        share_of_tam=lambda d: (d["share_of_tam"] * 100).round(1).astype(str) + "%",
        cumulative_share=lambda d: (d["cumulative_share"] * 100).round(1).astype(str) + "%",
    )[["state", "companies", "share_of_tam", "cumulative_share"]].to_string(index=False)
)

print("\nKEY FINDINGS")
print(f"Total addressable companies: {TOTAL_TAM:,}")
print(f"NSW + VIC: {nsw_vic:,} ({nsw_vic / TOTAL_TAM:.1%})")
print(f"NSW + VIC + QLD: {top_three:,} ({top_three / TOTAL_TAM:.1%})")

print("\nINTERPRETATION")
print(
    "More than four-fifths of the identified national TAM sits in NSW, Victoria "
    "and Queensland. Geography therefore provides an immediate first layer for "
    "campaign prioritisation before narrower industry, employee-size or other "
    "targeting criteria are applied."
)
