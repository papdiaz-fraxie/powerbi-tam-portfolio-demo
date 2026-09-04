import pandas as pd

# Synthetic campaign data for portfolio demonstration only.
df = pd.DataFrame([
    ["Job Ads ANZ", 1265, 243, 37, 20, 4],
    ["Competitor Takeout ANZ", 1287, 307, 24, 11, 2],
    ["General Outbound ANZ", 1330, 283, 18, 36, 6],
    ["Partners ANZ", 1273, 285, 28, 25, 13],
    ["Scale Up ANZ", 1275, 285, 25, 19, 2],
], columns=["campaign", "delivered", "opens", "clicks", "replies", "qualified"])

df["open_rate"] = df["opens"] / df["delivered"]
df["click_rate"] = df["clicks"] / df["delivered"]
df["reply_rate"] = df["replies"] / df["delivered"]
df["reply_to_qualified_rate"] = df["qualified"] / df["replies"]

summary = df.sort_values(["qualified", "replies"], ascending=False)

print(summary[[
    "campaign", "delivered", "replies", "qualified",
    "reply_rate", "reply_to_qualified_rate"
]].to_string(index=False))

print("\nHighest reply rate:", df.loc[df["reply_rate"].idxmax(), "campaign"])
print("Highest reply-to-qualified rate:", df.loc[df["reply_to_qualified_rate"].idxmax(), "campaign"])
