import pandas as pd
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

records = [
    [1, "Alex", "Smith", "Northstar Tech", "alex.smith@example.com", "Australia"],
    [2, "Jordan", "Lee", "Harbour Systems", "jordan.lee@example.com", "AU"],
    [3, "Taylor", "Brown", "Vector Labs", "bad-email", "AUS"],
    [4, "", "Wilson", "Summit Digital", "morgan.wilson@example.com", "Australia"],
    [5, "Sam", "Martin", "Northstar Tech", "", "NZ"],
    [6, "Jordan", "Lee", "Harbour Systems", "jordan.lee@example.com", "AU"],
]

df = pd.DataFrame(records, columns=["contact_id", "first_name", "last_name", "company", "email", "country"])

df["email_clean"] = df["email"].fillna("").str.strip().str.lower()
df["valid_email"] = df["email_clean"].apply(lambda x: bool(EMAIL_RE.match(x)) if x else False)
df["missing_name"] = df["first_name"].fillna("").str.strip().eq("") | df["last_name"].fillna("").str.strip().eq("")
df["duplicate_email"] = df["email_clean"].replace("", pd.NA).duplicated(keep=False)

summary = {
    "total_records": len(df),
    "invalid_or_missing_email": int((~df["valid_email"]).sum()),
    "missing_name": int(df["missing_name"].sum()),
    "duplicate_email_rows": int(df["duplicate_email"].sum()),
}

print("DATA QUALITY SUMMARY")
for key, value in summary.items():
    print(f"{key:26} {value}")
